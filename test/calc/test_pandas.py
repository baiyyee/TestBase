# Reference: https://www.pypandas.cn/docs/getting_started/10min.html

import logging
import numpy as np
import pandas as pd


def test_generate_df():
    series = pd.Series([1, 3, 5, np.NAN, 6, 8])

    dates = pd.date_range("20221011", periods=6, freq="D")

    df1 = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

    df2 = pd.DataFrame(
        {
            "A": 1,
            "B": pd.Timestamp("20221011"),
            "C": pd.Series(1, index=list(range(4)), dtype="float32"),
            "D": np.array([3] * 4, dtype="int32"),
            "E": pd.Categorical(["test", "train", "test", "train"]),
            "F": "foo",
        }
    )

    df3 = pd.DataFrame([{"name": "hhb", "age": 18, "height": 180}, {"name": "baiye", "age": 18, "height": 180}])

    df4 = pd.DataFrame({"name": ["hhb", "baiye"], "age": [18, 20]})

    df5 = pd.DataFrame([[1, 2], [3, 4]], columns=["A", "B"])

    df6 = pd.DataFrame()
    df6["name"] = ["hhb"]
    df6["age"] = [18]

    logging.info(series)
    logging.info(dates)
    logging.info(df1)
    logging.info(df2)
    logging.info(df3)
    logging.info(df4)
    logging.info(df5)
    logging.info(df6)


def test_df_attribute():
    df = pd.DataFrame(
        {
            "A": 1,
            "B": pd.Timestamp("20221011"),
            "C": pd.Series(1, index=list(range(4)), dtype="float32"),
            "D": np.array([3] * 4, dtype="int32"),
            "E": pd.Categorical(["test", "train", "test", "train"]),
            "F": "foo",
        }
    )

    logging.info(df.dtypes)
    logging.info(df.head(2))
    logging.info(df.tail(2))
    logging.info(df.index)
    logging.info(df.index.to_list())
    logging.info(df.columns)
    logging.info(df.columns.to_list())
    logging.info(df.describe())
    logging.info(df.T)


def test_df_timeseries():
    range = pd.date_range("2022/10/13", periods=20, freq="S")
    series = pd.Series(np.random.randint(0, 100, len(range)), index=range)

    series.resample("3S").sum()

    ts_utc = series.tz_localize("UTC")
    ts_utc.tz_convert("US/Eastern")

    range = pd.date_range("2022/10/13", periods=20, freq="D")
    series = pd.Series(np.random.randint(0, 100, len(range)), index=range)

    series.to_period("M")
    series.to_period("Q")

    range = pd.period_range("1990Q1", "2000Q4", freq="Q-NOV")
    series = pd.Series(np.random.randn(len(range)), range)


def test_df_category():
    df = pd.DataFrame({"id": [1, 2, 3, 4, 5, 6], "raw_grade": ["a", "b", "b", "a", "a", "e"]})

    df["grade"] = df["raw_grade"].astype("category")
    df["grade"].cat.categories = ["very good", "good", "very bad"]

    df["grade"] = df["grade"].cat.set_categories(["very bad", "bad", "medium", "good", "very good"])

    # 按类列分组（groupby）时，即便某类别为空，也会显示
    df.groupby("grade").size()


def test_df_sort():
    dates = pd.date_range("20221011", periods=6, freq="D")
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

    df.sort_index(axis=1, ascending=False)
    df.sort_values(by="B")


def test_df_get_value():
    dates = pd.date_range("20221011", periods=6, freq="D")
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

    df["A"]
    df[0:3]
    df["2022-10-11":"2022-10-13"]

    df.loc["2022-10-11"]
    df.loc["2022-10-11"]["A"]
    df.loc["2022-10-11", "A"]
    df.loc["2022-10-11", ["A", "B"]]
    df.loc[:, ["A", "B"]]
    df.loc["2022-10-11":"2022-10-13", ["A", "B"]]

    df.iloc[3]
    df.iloc[3:5, 0:2]
    df.iloc[[1, 2, 4], [0, 2]]
    df.iloc[1:3, :]
    df.iloc[:, 1:3]
    df.iloc[1, 1]

    df.at["2022-10-11", "A"]
    df.iat[1, 1]


def test_df_set_value():
    dates = pd.date_range("20221011", periods=6, freq="D")
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
    series = pd.Series([1, 2, 3, 4, 5, 6], index=dates)

    df["E"] = series

    df.loc["2022-10-11", "A"] = 0
    df.loc[:, "D"] = np.array([5] * len(df))

    df.at["2022-10-11", "A"] = 0
    df.iat[0, 0] = 0

    df[df > 0] = -df


def test_df_filter():
    dates = pd.date_range("20221011", periods=6, freq="D")
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

    df2 = df.copy()
    df2["E"] = ["one", "one", "two", "three", "four", "three"]

    df[df > 0]
    df[df["A"] > 0]

    df2[df2["E"].isin(["two", "four"])]


def test_df_na():
    dates = pd.date_range("20221011", periods=6, freq="D")
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

    df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ["E"])
    df1.loc[dates[0] : dates[1], "E"] = 1

    df1.dropna(how="any")
    df1.fillna(value=5)

    pd.isna(df1)


def test_df_stas():
    dates = pd.date_range("20221011", periods=6, freq="D")
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

    series = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)

    df.describe()

    df.mean()
    df.mean(0)  # col
    df.mean(1)  # row

    # 不同维度对象运算时，要先对齐。 此外，Pandas 自动沿指定维度广播
    df.sub(series, axis="index")


def test_df_value_counts():
    series = pd.Series(np.random.randint(0, 7, size=10))

    series.value_counts()
    dict(series.value_counts())
    {k: v for k, v in series.value_counts().items()}


def test_df_apply():
    dates = pd.date_range("20221011", periods=6, freq="D")
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

    df.apply(np.cumsum)
    df.apply(lambda x: x.max() - x.min())


def test_df_concat():
    df = pd.DataFrame(np.random.randn(10, 4))
    series = pd.Series([1, 2, 3, 4])

    # 分解为多组
    pieces = [df[:3], df[3:7], df[7:]]
    # 将多个组拼接到一起
    pd.concat(pieces)

    # 将 Series 拼接到 DataFrame
    pd.concat([df, series.to_frame().T], ignore_index=True)


def test_df_merge():
    left = pd.DataFrame({"key": ["foo", "foo"], "lval": [1, 2]})
    right = pd.DataFrame({"key": ["foo", "foo"], "rval": [4, 5]})
    pd.merge(left, right, on="key")

    left = pd.DataFrame({"key": ["foo", "bar"], "lval": [1, 2]})
    right = pd.DataFrame({"key": ["foo", "bar"], "rval": [4, 5]})
    pd.merge(left, right, on="key")


def test_df_group():
    df = pd.DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.randn(8),
            "D": np.random.randn(8),
        }
    )

    df.groupby("A").size()
    df.groupby("A").sum()
    df.groupby(["A", "B"]).sum()

    """
    test.log
    
        IP,URL
        1.1.1.1,www.baidu.com
        1.1.1.2,www.baidu.com
        1.1.1.3,www.baidu.com
        1.1.1.1,www.baidu.com
        1.1.1.2,www.baidu.com
        1.1.1.1,www.baidu.com1
        1.1.1.2,www.baidu.com1
        1.1.1.1,www.baidu.com2
        1.1.1.2,www.baidu.com2

    # 解法一：
    import pandas as pd

    path = "test.log"
    df = pd.read_csv(path)
    data = df.groupby(["URL"]).agg(COUNT=("IP", lambda data: len(set(data)))).reset_index()
    data


    # 解法二：
    path = "test.log"

    lines = None
    with open(path, "r") as f:
        lines = f.readlines()

    columns = lines[0].split(",")
    lines = lines[1:]

    datas = [{data.split(",")[1].replace("\n", ""): data.split(",")[0]} for data in lines]

    result = {k: set() for data in datas for k in data}

    for data in datas:
        for k, v in data.items():
            if k in result:
                result[k].add(v)

    result = {k: len(v) for k, v in result.items()}
    result
    """


def test_df_stack():
    data = list(
        zip(*[["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"], ["one", "two", "one", "two", "one", "two", "one", "two"]])
    )
    index = pd.MultiIndex.from_tuples(data, names=["first", "second"])
    df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=["A", "B"])

    df.stack()
    df.stack().unstack()
    df.stack().unstack(0)
    df.stack().unstack(1)


def test_df_pivot():
    df = pd.DataFrame(
        {
            "A": ["one", "one", "two", "three"] * 3,
            "B": ["A", "B", "C"] * 4,
            "C": ["foo", "foo", "foo", "bar", "bar", "bar"] * 2,
            "D": np.random.randn(12),
            "E": np.random.randn(12),
        }
    )

    pd.pivot_table(df, values="D", index=["A", "B"], columns=["C"])
    pd.pivot_table(df, values=["D", "E"], index=["A", "B"], columns=["C"])


def test_df_str():
    series = pd.Series(["A", "B", "C", "Aaba", "Baca", np.nan, "CABA", "dog", "cat"])

    series.str.lower()


def test_df_plotting():
    series = pd.Series(np.random.randn(1000), index=pd.date_range("2000/1/1", periods=1000))
    series = series.cumsum()
    series.plot()

    df = pd.DataFrame(np.random.randn(1000, 4), index=series.index, columns=["A", "B", "C", "D"])
    df = df.cumsum()
    df.plot()
