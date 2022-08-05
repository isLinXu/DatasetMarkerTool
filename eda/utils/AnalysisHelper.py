import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


class ColumnInfos:
    """
    Each column of the pandas DataFrame is a object that holds its own infos and advices.
    """

    def __init__(self, index, name, n_rows, nulls, dtype, uniques, categories, sample):
        """
        :param index: Number of the 0-indexed index in the DataFrame. Currently independent from the true Index.
        :param name: Name of the column.
        :param n_rows: Number of non-null values.
        :param nulls: Number of null values.
        :param dtype: dtype of the column.
        :param uniques: Number of uniques.
        :param categories: List of categories if less than the Helper parameter "max_categorisable".
        :param sample: first non NA value of the column, to test for other advices.
        """
        self.index = index
        self.name = name
        self.n_rows = n_rows
        self.nulls = nulls
        self.dtype = dtype
        self.uniques = uniques
        self.categories = categories
        self.is_date_compatible = date_compatible(sample)

    def has_advice(self):
        """
        Tells if the ColumnInfo presently holds an advice.
        :return: Boolean. True : yes, False = no.
        """
        if self.dtype != "datetime64[ns]" and self.is_date_compatible:
            return True
        if self.categories is None:
            return False
        if self.dtype != "category" and len(self.categories) > 2:
            return True
        if self.dtype != "bool" and len(self.categories) <= 2:
            return True

    def get_advice(self):
        """
        If it holds any advice, formats it then return it as a String.
        :return: Advice(s) as String to be printed as is.
        """
        if not self.has_advice():
            return
        ret = "The column \"%s\" (index %d)" % (self.name, self.index)
        if self.is_date_compatible:
            return ret + " seems compatible with datetime. Check and try to cast it using \"pandas.to_date_time()\"."
        if self.categories is not None:
            if self.uniques > 1:
                return ret + " should be casted into a %s." % \
                       ("category" if self.uniques > 2 else "boolean")
            else:
                return ret + "should be deleted."

    def get_advice_func(self):
        if self.is_date_compatible:
            return lambda col: pd.to_datetime(col)
        elif self.categories is not None:
            return lambda col: col.astype("category") if self.uniques > 2 else col == self.categories[0]
        else:
            return lambda col: col

    def __str__(self):
        return format_col_infos([self.name], {}, len(self.name))


class Helper:
    """
    A class that provides methods to quickly see points of interest of a pandas Dataframe.
    """
    # Shows a different color for each type of columns.
    color_dict = {"int8": "2;31;47", "int16": "3;31;47", "int32": "0;31;47", "int64": "1;31;47",
                  "uint8": "2;31;47", "uint16": "3;31;47", "uint32": "0;31;47", "uint64": "1;31;47",
                  "float16": "3;33;47", "float32": "0;33;47", "float64": "1;33;47", "object": "1;32;47",
                  "bool": "1;34;47", "category": "1;36;47", "datetime64[ns]": "1;37;47", "timedelta64[ns]": "1;35;47"}

    # Levels of correlations given a pearson correlation value (0 to 1).
    # Reference : http://www.statstutor.ac.uk/resources/uploaded/pearsons.pdf page 4
    corr_categories_intervals = (0.2, 0.4, 0.6, 0.8, 1)
    corr_categories_names = ('very weak', 'weak', 'moderate',
                             'strong', 'very strong')

    def __init__(self, dataframe, max_categorisable=12, show_corr_matrix=True, corr_annot=True, corr_cmap=None,
                 apply_advice=False):
        """
        :param dataframe: The Dataframe to analyse
        :param max_categorisable: Maximum number of uniques for a column to be considered as categorisable.
        :param corr_annot: Shows or not the correlation value on the Heatmap.
        :param corr_cmap: Sets the colormap used for the correlation matrix.
        Check here : https://python-graph-gallery.com/92-control-color-in-seaborn-heatmaps/
        :param show_corr_matrix: Sets if the correlation matrix is wanted to be drawn with seaborn.
        """
        assert isinstance(dataframe, pd.DataFrame)
        self.dataframe = dataframe
        self.annot_corr = corr_annot
        self.corr_cmap = corr_cmap if corr_cmap is not None else sns.diverging_palette(12.2, 127, sep=75, as_cmap=True)
        self.max_categorisable = max_categorisable
        self.show_corr_matrix = show_corr_matrix
        # The correlation matrix drawn with seaborn.
        self.corr = None
        # Dictionary of ColumnInfos, working along with the current class.
        self.dataframe_col_infos = []
        # True if the user wants the advices to be applied automatically
        self.is_apply_advices = apply_advice
        self.analyze()

    def analyze(self):
        """
        Launches basic hints for analyses :
        1- Extended info-like table.
        2- Correlation matrix and correlated pairs of characteristics.
        3- Relevant advices about columns.
        4- If the user set apply_advices as True, the DataFrame will be updated following the advices.
        :return:
        """
        analysis_text = "\n##### GENERAL DATAFRAME INFOS #####\n" + self.analyze_columns() + \
                        "\n\n##### CORRELATION INFOS #####\n" + self.analyze_correlations() + \
                        "\n\n##### GENERAL ADVICES #####\n"
        advices = self.get_advices()
        analysis_text += "\n" + (advices if advices != "\n" else "No advice available.")
        if self.is_apply_advices:
            analysis_text += "\nApplying advices now...\n"
            self.apply_advices()
            self.analyze()
            return
        analysis_text += "\n\n##### NULL CAUSES ESTIMATIONS #####\n" + self.analyze_null_causes()
        print(analysis_text)

        if self.show_corr_matrix and self.corr is not None:
            hm = sns.heatmap(self.corr, cmap=self.corr_cmap, annot=self.annot_corr, center=0,
                             xticklabels=self.corr.columns.values,
                             yticklabels=self.corr.columns.values, vmin=-1, vmax=1)
            bottom, top = hm.get_ylim()
            hm.set_ylim(bottom + 0.5, top - 0.5)
            plt.show()

    def analyze_columns(self):
        """
        Gives basic infos about the Dataframe, just like DataFrame.info(), but with some extras :
        - actually tells about the number of NaN per column.
        - informs about the number of uniques per column.
        - shows the unique values of a columns if they are less than the attribute max_categorisable (default=12).
        :return: All infos as formatted text to be printed as is.
        """
        cols = self.dataframe.columns
        n_cols = len(cols)
        n_rows = len(self.dataframe)
        indices = self.dataframe.index
        dataframe_main_infos = '\nThe dataframe has %s columns and %d rows.' % (n_cols, n_rows) + \
                               ("\nIndices : from %d to %d (step= %d)"
                                % (indices.start, indices.stop - indices.step, indices.step)
                                if isinstance(indices, pd.core.indexes.range.RangeIndex)
                                else "\nIndices are not a RangeIndex. %s instead." % type(indices))
        self.dataframe_col_infos = {}
        maxlength = 0
        for i in range(0, len(cols)):
            col = self.dataframe[cols[i]]
            name = cols[i]
            nulls = col.isna().sum()
            uniques = len(col.unique())
            coltype = str(col.dtype)
            if maxlength < len(name):
                maxlength = len(name)
            categories = None
            if coltype in ["category", "bool"] or uniques <= self.max_categorisable:
                categories = list(col.unique())
            self.dataframe_col_infos[i] = ColumnInfos(i, name, nulls, n_rows - nulls,
                                                      str(col.dtype), uniques, categories,
                                                      col.bfill(axis=0)[[0]])
        col_infos = format_col_infos(self.dataframe_col_infos, self.color_dict, maxlength)

        return dataframe_main_infos + "\n" + "\n".join(col_infos)

    def analyze_correlations(self):
        """
        Get the correlation of each pair of caracteristic and prints the correlation of strength of the correlated ones.
        :return: A string describing the correlation between numbers in the DataFrame.
        """
        self.corr = self.dataframe.corr()
        corr_infos = ""
        for i in range(len(self.corr) - 1):
            for j in range(i + 1, len(self.corr)):
                corr_value = self.corr.iloc[i][j]
                if pd.isnull(corr_value):
                    continue
                correlation_strength = get_interval(corr_value, self.corr_categories_intervals)
                if correlation_strength > 0:
                    corr_infos += "\n\"%s\" and \"%s\" have a %s %s correlation : %f" % (
                        self.dataframe.columns[i], self.dataframe.columns[j], self.corr_categories_names
                        [correlation_strength], "positive" if corr_value >= 0 else "negative",
                        corr_value)

        return corr_infos

    def analyze_null_causes(self):
        """
        For each column which has NANs or NAs, it will identify if another column is the cause.
        Example : NANS from "Mean per month" column might be because of the column "Period" (with a division by zero)
        :return: A string describing the cause of nulls, if found.
        """
        causes = ""
        for index_col in range(len(self.dataframe.columns)):
            if self.dataframe[self.dataframe.columns[index_col]].isna().sum() == 0:
                continue
            null_rows = self.dataframe[self.dataframe[self.dataframe.columns[index_col]].isna()]
            _is_not_empty = False
            for other_col in range(len(self.dataframe.columns)):
                if other_col == index_col:
                    continue
                values_other_col = null_rows[self.dataframe.columns[other_col]].dropna().unique()
                if len(values_other_col) == 1:
                    _is_not_empty = True
                    causes += ("\nThe null values from column \"%s\" (index %d) seem to be caused by the values "
                               "{%s} from the column \"%s\" (index %d)." % (str(self.dataframe.columns[index_col]),
                                                                            index_col, values_other_col[0],
                                                                            str(self.dataframe.columns[other_col]),
                                                                            other_col))

        return causes

    def get_advices(self):
        """
        Retrieves and concatenate advices from all ColumnInfos as a String.
        :return: String of all ColumnInfos advices.
        """
        advices = []
        for i in range(len(self.dataframe_col_infos)):
            if self.dataframe_col_infos[i].has_advice():
                advices.append(self.dataframe_col_infos[i].get_advice())
        return "\n" + "\n".join(advices)

    def apply_advices(self):
        """
        Apply the function given by the advices to each column of the dataframe.
        """
        for i in range(len(self.dataframe.columns)):
            self.dataframe[self.dataframe.columns[i]] = self.dataframe_col_infos[i].get_advice_func()(
                self.dataframe[self.dataframe.columns[i]])
        self.is_apply_advices = False


def format_col_infos(infos, color_dict, maxlength):
    """
    Format the infos passed as parameter so that they are displayed in a nice fashion in the console.
    :param infos: List or tuple of ColumnInfos instances. One per row.
    :param color_dict: Dictionary to set a color for each type of data.
    :param maxlength: Length of the longest name string. Need so each column of info is aligned.
    :return: A list of formatted strings to be joined with a line-return then to be displayed as is.
    """
    ret = []
    for i in range(len(infos)):
        colinfo = infos[i]
        col_text = str(i) + ":\t\"" + colinfo.name + "\"" + "." * (maxlength + 2 - len(colinfo.name)) + "of type %s " \
                                                                                                        "\t%d null " \
                                                                                                        "values" % (
                       "\x1b[" + color_dict[str(colinfo.dtype)] + "m" + str(colinfo.dtype) + "\x1b[0m", colinfo.n_rows)
        if not colinfo.categories:
            col_text += " and %d uniques" % colinfo.uniques
        elif colinfo.dtype != "bool":
            col_text += " and %d uniques [" % colinfo.uniques + ", ".join(map(str, colinfo.categories)) + "]"

        ret.append(col_text + ".")
    return ret


def get_interval(value, intervals):
    """
    Returns the index of the interval the value lies in.
    :param value: Value for which to find the interval.
    :param intervals: List or tuple of interval with values which represent the upper boundary of each interval.
    The first interval starts at 0 and ends ar the first value (excluded, except for the last interval).
    :return: Index in regard to the intervals list/tupple.
    """
    if value is None or isinstance(value, str):
        return
    for i in range(len(intervals)):
        if abs(value) < intervals[i]:
            return i
    return len(intervals) - 1


def date_compatible(sample):
    """
    Checks if a value is time_compatible.
    To do so, it passes two tests :
    1- It looks for three non-overlapping components thanks to a regex pattern :
        1- Year (4 digits)
        2- Month (three letters or numbers 00 to 19)
        3- Day (numbers 00 to 39)
    2- It tests the cast into Datetime type.
    If both tests passed, it will inform the calling ColumnInfos that it might be a date.
    WARNING : Needs further testing and improvements !!!
    For example : it doesn't detect this kind of pattern yet : "ddmmyyyy" (with no separator in-between)
    :param sample: Value to test.
    :return: True if sample looks like a relevant datetime.
    """
    if len(re.findall(r"(?i)(([12][\d]{3})(?=($|[^\d])))|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(?=($|[^\d]))"
                      r"|(([01][\d])(?=($|[^\d])))|((^|[^\d])([0-3][\d])(?=($|[^\d])))", str(sample))) < 3:
        return False
    try:
        pd.to_datetime(sample)
    except (ValueError, TypeError):
        return False
    return True
