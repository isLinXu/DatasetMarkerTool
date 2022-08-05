import altair as alt
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numbers
import numpy as np


def imputer(df, strategy="mean", fill_value=None):
    """
    A function to implement imputation functionality for completing missing values.
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        a dataframe that might contain missing data
    strategy : string, default="mean"
        The imputation strategy.
            - If "mean", then replace missing values using the mean along each column. Can only be used with numeric data.
            - If "median", then replace missing values using the median along each column. Can only be used with numeric data.
            - If "most_frequent", then replace missing using the most frequent value along each column. Can be used with strings or numeric data. If there is more than one such value, only the smallest is returned.
            - If "constant", then replace missing values with fill_value. Can be used with strings or numeric data.
    fill_value : numerical value, default=None
        When strategy == "constant", fill_value is used to replace all occurrences of missing_values. If left to the default, fill_value will be 0 when imputing numerical data.
    Returns
    -------
    pandas.core.frame.DataFrame
        a dataframe that contains no missing data
    Examples
    ---------
    >>> import pandas as pd
    >>> from eda_utils_py import cor_map
    >>> data = pd.DataFrame({
    >>>     'SepalLengthCm':[5.1, 4.9, 4.7],
    >>>     'SepalWidthCm':[1.4, 1.4, 1.3],
    >>>     'PetalWidthCm':[0.2, None, 0.2]
    >>> })
    >>> imputer(data, numerical_columns)
       SepalLengthCm  SepalWidthCm  PetalWidthCm
    0            5.1           1.4           0.2
    1            4.9           1.4           0.2
    2            4.7           1.3           0.2
    """

    # Tests whether input data is of pd.DataFrame type
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The input dataframe must be of pd.DataFrame type")

    # Tests whether input strategy is of type str
    if not isinstance(strategy, str):
        raise TypeError("strategy must be of type str")

    # Tests whether input fill_value is of type numbers or None
    if not isinstance(fill_value, type(None)) and not isinstance(
            fill_value, numbers.Number
    ):
        raise TypeError("fill_value must be of type None or numeric type")

    # Tests whether the inputs for strategy and fill_value are consistent
    if isinstance(fill_value, numbers.Number) and strategy != "constant":
        raise Exception("fill_value can be a number only if strategy is 'constant'")

    # Tests whether the inputs for strategy and fill_value are consistent
    if isinstance(fill_value, type(None)) and strategy == "constant":
        raise Exception("fill_value should be a number when strategy is 'constant'")

    result = pd.DataFrame()
    if strategy == "mean":
        result = df.apply(lambda x: x.fillna(x.mean()), axis=0)
    elif strategy == "median":
        result = df.apply(lambda x: x.fillna(x.median()), axis=0)
    elif strategy == "most_frequent":
        result = df.apply(lambda x: x.fillna(x.value_counts().index[0]), axis=0)
    elif strategy == "constant":
        result = df.apply(lambda x: x.fillna(fill_value))
    else:
        raise Exception(
            "strategy should be one of 'mean', 'median', 'most_frequent' and 'constant'"
        )

    return result


def cor_map(dataframe, num_col, col_scheme="purpleorange"):
    """
    A function to implement a correlation heatmap including coefficients based on given numeric columns of a data frame.
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        The data frame to be used for EDA.
    num_col : list
        A list of string of column names with numeric data from the data frame.
    col_scheme : str, default = 'purpleorange'
        The color scheme of the heatmap desired, can only be one of the following;
            - 'purpleorange'
            - 'blueorange'
            - 'redblue'
    Returns
    -------
    altair.vegalite.v4.api.Chart
        A correlation heatmap plot with correlation coefficient labels based on the numeric columns specified by user.
    Examples
    ---------
    >>> import pandas as pd
    >>> from eda_utils_py import cor_map
    >>> data = pd.DataFrame({
    >>>     'SepalLengthCm':[5.1, 4.9, 4.7],
    >>>     'SepalWidthCm':[1.4, 1.4, 1.3],
    >>>     'PetalWidthCm':[0.2, 0.1, 0.2],
    >>>     'Species':['Iris-setosa','Iris-virginica', 'Iris-germanica']
    >>> })
    >>> numerical_columns = ['SepalLengthCm','SepalWidthCm','PetalWidthCm']
    >>> cor_map(data, numerical_columns, col_scheme = 'purpleorange')
    """

    # Tests whether input data is of pd.DataFrame type
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("The input dataframe must be of pd.DataFrame type")

    # Tests whether input num_col is of type list
    if not isinstance(num_col, list):
        raise TypeError("The input num_col must be of type list")

    # Tests whether values of num_col is of type str
    for x in num_col:
        if not isinstance(x, str):
            raise TypeError("The type of values in num_col must all be str")

    # Tests whether input col_scheme is of type str
    if not isinstance(col_scheme, str):
        raise TypeError("col_scheme must be of type str")

    # Tests whether col_scheme is one of three possible options
    if col_scheme not in ("purpleorange", "blueorange", "redblue"):
        raise Exception(
            "This color scheme is not available, please use either 'purpleorange', 'blueorange' or 'redblue'"
        )

    # Tests whether all input columns exist in the input data
    for x in num_col:
        if x not in list(dataframe.columns):
            raise Exception("The given column names must exist in the given dataframe.")

    # Tests whether all input columns in num_col are numeric columns
    for x in num_col:
        if not is_numeric_dtype(dataframe[x]):
            raise Exception("The given numerical columns must all be numeric.")

    corr_matrix = dataframe[num_col].corr().reset_index().melt("index")
    corr_matrix.columns = ["var1", "var2", "cor"]

    plot = (
        alt.Chart(corr_matrix)
            .mark_rect()
            .encode(
            x=alt.X("var1", title=None),
            y=alt.Y("var2", title=None),
            color=alt.Color(
                "cor",
                title="Correlation",
                scale=alt.Scale(scheme=col_scheme, domain=(-1, 1)),
            ),
        )
            .properties(title="Correlation Matrix", width=400, height=400)
    )

    text = plot.mark_text(size=15).encode(
        text=alt.Text("cor", format=".2f"),
        color=alt.condition(
            "datum.cor > 0.5 | datum.cor < -0.3", alt.value("white"), alt.value("black")
        ),
    )

    cor_heatmap = plot + text

    return cor_heatmap


def outlier_identifier(dataframe, columns=None, method="trim"):
    """
    A function that identify by z-test with threshold of 3, and deal with outliers based on the method the user choose
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        The target dataframe where the function is performed.
    columns : list, default=None
        The target columns where the function needed to be performed. Defualt is None, the function will check all columns
    method : string
        The method of dealing with outliers.
            - if "trim" : we completely remove data points that are outliers.
            - if "median" : we replace outliers with median values
            - if "mean" : we replace outliers with mean values
    Returns
    -------
    pandas.core.frame.DataFrame
        a dataframe which the outlier has already process by the chosen method
    Examples
    --------
    >>> import pandas as pd
    >>> from eda_utils_py import cor_map

    >>> df = pd.DataFrame({
    >>>    'SepalLengthCm' : [5.1, 4.9, 4.7, 5.5, 5.1, 50, 5.4, 5.0, 5.2, 5.3, 5.1],
    >>>    'SepalWidthCm' : [1.4, 1.4, 20, 2.0, 0.7, 1.6, 1.2, 1.4, 1.8, 1.5, 2.1],
    >>>    'PetalWidthCm' : [0.2, 0.2, 0.2, 0.3, 0.4, 0.5, 0.5, 0.6, 0.4, 0.2, 5]
    >>> })
    >>> outlier_identifier(df)
    	 SepalLengthCm  	SepalWidthCm	   PetalWidthCm
    0	5.1	                1.4	                0.2
    1	4.9	                1.4	                0.2
    2	5.5	                2.0	                0.3
    3	5.1	                0.7	                0.4
    4	5.4	                1.2             	0.5
    5	5.0	                1.4	                0.6
    6	5.2	                1.8	                0.4
    7	5.3	                1.5	                0.2
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("The argument @dataframe must be of pd.DataFrame")

    if columns is None:
        for col in dataframe.columns:
            if not is_numeric_dtype(dataframe[col]):
                raise Exception(
                    "The given dataframe contains column that is not numeric column."
                )

    if columns is not None:
        if not isinstance(columns, list):
            raise TypeError("The argument @columns must be of type list")

        for col in columns:
            if col not in list(dataframe.columns):
                raise Exception(
                    "The given column list contains column that is not exist in the given dataframe."
                )
            if not is_numeric_dtype(dataframe[col]):
                raise Exception(
                    "The given column list contains column that is not numeric column."
                )

    if method not in ("trim", "median", "mean"):
        raise Exception("The method must be -trim- or -median- or -mean-")

    df = dataframe.copy()
    target_columns = []
    if columns is None:
        target_columns = list(df.columns.values.tolist())
    else:
        target_columns = columns

    outlier_index = []
    for column in target_columns:
        current_column = df[column]
        mean = np.mean(current_column)
        std = np.std(current_column)
        threshold = 3

        for i in range(len(current_column)):
            current_item = current_column[i]
            z = (current_item - mean) / std
            if z >= threshold:
                if i not in outlier_index:
                    outlier_index.append(i)
                if method == "mean":
                    df.at[i, column] = round(mean, 2)
                if method == "median":
                    df.at[i, column] = np.median(current_column)

    if method == "trim":
        df = df.drop(outlier_index)

    df.index = range(len(df))
    return df


def scale(dataframe, columns, scaler="standard"):
    """
    A function to scale features either by using standard scaler or minmax scaler method
    Parameters
    ----------
    dataframe : pandas.DataFrame
        The data frame to be used for EDA.
    columns : list, default=None
        A list of string of column names with numeric data from the data frame that we wish to scale.
    scaler: str, default="standard"
        A string to specify the sclaing method to be used
            - if "standard": it transforms features by centering the distribution of the data on the value 0 and the standard
                        deviation to the value 1.
            - if "minmax": it transforms features by rescaling each feature to the range between 0 and 1.
    Returns
    -------
    dataframe : pandas.core.frame.DataFrame
        The scaled dataframe for numerical features
    Examples
    --------
    >>> import pandas as pd
    >>> from eda_utils_py import scale
    >>> data = pd.DataFrame({
    >>>     'SepalLengthCm':[1, 0, 0, 3, 4],
    >>>     'SepalWidthCm':[4, 1, 1, 0, 1],
    >>>     'PetalWidthCm:[2, 0, 0, 2, 1],
    >>>     'Species':['Iris-setosa','Iris-virginica', 'Iris-germanica']
    >>> })
    >>> numerical_columns = ['SepalLengthCm','SepalWidthCm','PetalWidthCm']
    >>> scale(data, numerical_columns, scaler="minmax")
       SepalLengthCm  SepalWidthCm  PetalWidthCm
    0           0.25          1.00           1.0
    1           0.00          0.25           0.0
    2           0.00          0.25           0.0
    3           0.75          0.00           1.0
    4           1.00          0.25           0.5
    """

    # Check if input data is of pd.DataFrame type
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("The input dataframe must be of pd.DataFrame type")

    # Check if input num_col is of type list
    if not isinstance(columns, list):
        raise TypeError("The input columns must be of type list")

    # Check if values of columns are of type str
    for col in columns:
        if not isinstance(col, str):
            raise TypeError("The name of features in columns list must all be str")

    # Check if all input columns exist in the input data
    for col in columns:
        if col not in list(dataframe.columns):
            raise Exception("The given column names must exist in the given dataframe.")

    # Check if all input columns in columns are numeric columns
    for col in columns:
        if not is_numeric_dtype(dataframe[col]):
            raise Exception("The given numerical columns must all be numeric.")

    # Check if scaler is of type str
    if not isinstance(scaler, str):
        raise TypeError("Scaler must be of type str")

    scaled_df = None
    if scaler == "minmax":
        scaled_df = _minmax(dataframe[columns])
    else:
        scaled_df = _standardize(dataframe[columns])

    return scaled_df


def _standardize(dataframe):
    """Transform features by centering the distribution of the data
    on the value 0 and the standard deviation to the value 1.
    The transformation is given by:
        scaled_value = (value - mean) / standard deviation
    Parameters
    ----------
    dataframe : pandas.DataFrame
        The data frame to be used for EDA.
    Returns
    -------
    res : pandas.core.frame.DataFrame
        Scaled dataset
    """

    res = dataframe.copy()
    for feature_name in dataframe.columns:
        mean = dataframe[feature_name].mean()
        stdev = dataframe[feature_name].std()
        res[feature_name] = (dataframe[feature_name] - mean) / stdev
    return res


def _minmax(dataframe):
    """Transform features by rescaling each feature to the range between 0 and 1.
    The transformation is given by:
        scaled_value = (feature_value - min) / (mix - min)
    where min, max = feature_range.
    This transformation is often used as an alternative to zero mean,
    unit variance scaling.
    Parameters
    ----------
    dataframe : pandas.DataFrame
        The data frame to be used for EDA.
    Returns
    -------
    res : pandas.core.frame.DataFrame
        Scaled dataset
    """

    res = dataframe.copy()
    for feature_name in dataframe.columns:
        max = dataframe[feature_name].max()
        min = dataframe[feature_name].min()
        res[feature_name] = (dataframe[feature_name] - min) / (max - min)

    return res


Footer
