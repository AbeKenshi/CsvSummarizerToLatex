# csvファイルのデータをtexのテーブル形式に変換するプログラム
import pandas as pd
import numpy as np


def summarizeCsvToLatex(name, significant_figure, multipliers, isStd):
    df = pd.DataFrame.from_csv(name + ".csv")  # ファイル読み込み
    if len(df.columns) != len(significant_figure):
        raise ValueError("The length of the array of significant figure does not match the number of columns of data.")
    if len(df.columns) != len(multipliers):
        raise ValueError("The length of the array of multiplier does not match the number of columns of data.")
    for i in range(len(df.columns)):
        if multipliers[i] != None:
            df.ix[:, [i]] = df.ix[:, [i]] / (10 ** multipliers[i])
        if significant_figure[i] != None:
            s_orig = df.ix[:, [i]].as_matrix()
            s_orig = round_sig(s_orig, significant_figure[i])
            dfn = pd.DataFrame(s_orig)
            dfn.columns = [df.columns[i]]
            df.ix[:, [i]] = dfn
    df.ix[:, :] = df.ix[:, :].astype(str)
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            if str_isdigit(df.ix[i, j]):
                while significant_figure[j] != None and len_str(df.ix[i, j]) < significant_figure[j]:
                    df.ix[i, j] += "0"

    for i in range(len(df.columns)):
        if isStd[i]:
            df.ix[:, i - 1] = df.ix[:, i - 1] + "(\pm" + df.ix[:, i] + ")"
            df = df.drop(df.columns[i], axis=1)

    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            df.ix[i, j] = " $" + str(df.ix[i, j]) + "$ "
    df.to_csv(name + ".tex", sep='&', line_terminator='\\\\ \hline\n', quotechar=" ")


# 有効桁数に丸め込むメソッド
def round_sig(x, sig=2):
    y = [np.around(x[i], sig - np.int_(np.floor(np.log10(abs(x[i] + 1e-200)))) - 1) if
         not (np.math.isnan(x[i])) else x[i] for i in range(len(x))]
    return y


# 文字列の長さを返すメソッド
def len_str(str):
    minus = 0
    if "." in str:
        minus += 1
    for i in range(len(str)):
        if str[i] == "0":
            minus += 1
        else:
            break
    return len(str) - minus


# 文字列が数値かどうか調べるメソッド
def str_isdigit(str):
    try:
        float(str)
        return True

    except ValueError:
        return False


if __name__ == '__main__':
    name = "sample/sample"
    significant_figure = [None, 3, 3]  # 有効桁数，Noneの場合は桁数調整をしない
    multipliers = [None, 4, 4]  # 各列のデータを10の乗数で割る，Noneの場合は乗算をしない
    isStd = [False, False, True]  # 標準偏差かどうか，標準偏差なら左のやつと結合
    summarizeCsvToLatex(name, significant_figure, multipliers, isStd)
