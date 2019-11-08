from pyspark.sql.functions import lit, avg, count, udf, struct, sum
from pyspark.sql.types import DoubleType


def anova_in_spark(df, categorical_var, continuous_var):
    """
    Given a Spark Dataframe, compute the one-way ANOVA using the given categorical and continuous variables.
    :param df: Spark Dataframe
    :param categorical_var: Name of the column that represents the grouping variable to use
    :param continuous_var: Name of the column corresponding the continuous variable to analyse
    :return: Sum of squares within groups, Sum of squares between groups, F-statistic, degrees of freedom 1, degrees of freedom 2
    """

    global_avg = df.select(avg(continuous_var)).take(1)[0][0]

    avg_in_groups = df.groupby(categorical_var).agg(avg(continuous_var).alias("Group_avg"),
                                                    count("*").alias("N_of_records_per_group"))
    avg_in_groups = avg_in_groups.withColumn("Global_avg",
                                             lit(global_avg))

    udf_between_ss = udf(lambda x: x[0] * (x[1] - x[2]) ** 2,
                         DoubleType())
    between_df = avg_in_groups.withColumn("squared_diff",
                                          udf_between_ss(struct('N_of_records_per_group',
                                                                'Global_avg',
                                                                'Group_avg')))
    ssbg = between_df.select(sum('squared_diff')).take(1)[0][0]

    within_df_joined = avg_in_groups \
        .join(df,
              df.algorithm == avg_in_groups.algorithm) \
        .drop(avg_in_groups.algorithm)

    udf_within_ss = udf(lambda x: (x[0] - x[1]) ** 2, DoubleType())
    within_df_joined = within_df_joined.withColumn("squared_diff",
                                                   udf_within_ss(struct(continuous_var,
                                                                        'Group_avg')))
    sswg = within_df_joined \
        .groupby("algorithm") \
        .agg(sum("squared_diff").alias("sum_of_squares_within_gropus")) \
        .select(sum('sum_of_squares_within_gropus')).take(1)[0][0]
    m = df.groupby('algorithm') \
        .agg(count("*")) \
        .count()  # number of levels
    n = df.count()  # number of observations
    df1 = m - 1
    df2 = n - m
    f_statistic = (ssbg / df1) / (sswg / df2)
    return sswg, ssbg, f_statistic, df1, df2
