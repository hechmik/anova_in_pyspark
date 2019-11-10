# One-way ANOVA in PySpark
***If you think this repository was useful for solving your problem please leave a Star!***

This is my one-way ANOVA implementation from scratch using PySpark. The reason why I did it is that at this moment neither Spark's library MLLib either Spark 2.4.4 itself have a function that allows to perform One-Way ANOVA.

## Information returned by the function

The following values are returned by this function:

* sswg: Sum Of Squares withing groups
* ssbg: Sum of Squares between groups
* f_statistic: The F-statistic computed for the given variables
* df_1: Degrees of freedom 1, equal to *m - 1* where *m* is the number of levels (i.e. number of distinct categorical values in the grouping variables)
* df_2: Deegrees of freedom 2, equal to *n - m* where *n* is the number of observations and *m* is the number of levels (as specified in the previous point)

## How to import and use one-way ANOVA

### (Optional): install libraries

The *requirements.txt* file is related to the "Demo notebook" setup: however you can use it for reference, removing *pandas* and *scipy* libraries if not needed.

```bash
pip install -r requirements.txt
```

### Import the function in your code or notebook

```python
from anova_in_spark import one_way_anova
sswg, ssbg, f_statistic, df_1, df_2 = one_way_anova(df_of_anova, 'categorical_variable_column_name','continuous_variable_column_name')
```

## How to run the example

For helping the users familiarise with this function and see how it works I included a small Jupyter Notebook where I will apply one-way ANOVA to the test dataset and compare its results with the ones obtained by the function *stats.f_oneway(...)* contained in the *SciPy* package.

### Instructions for running the example notebook

#### Load the required libraries for running the Jupyer Notebook

``` bash
pip install -r requirements.txt
```

#### (Optional but recommended if you are using a virtual environment)

```bash
ipython kernel install --user --name=anova_spark'
```

#### Start Jupyter notebook (and have fun!)

```bash
jupyter notebook
```

# How to collaborate
If you find any error or have any suggestion on how to improve this function please feel free to open a Pull Request or an Issue!
