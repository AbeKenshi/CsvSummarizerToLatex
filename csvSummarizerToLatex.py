# csvファイルのデータをtexのテーブル形式に変換するプログラム
import pandas as pd
import numpy as np


def summarizeCsvToLatex(name, significant_figure, multipliers):
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

    df.to_csv(name + ".tex", sep='&', line_terminator='\\\\ \hline\n', quotechar=" ")


# 有効桁数に丸め込むメソッド
def round_sig(x, sig=2):
    y = [np.around(x[i], sig - np.int_(np.floor(np.log10(abs(x[i] + 1e-200)))) - 1) if
         not (np.math.isnan(x[i])) else x[i] for i in range(len(x))]
    return y


if __name__ == '__main__':
    name = "sample/sample"
    significant_figure = [None, 3, 3]  # 有効桁数，Noneの場合は桁数調整をしない
    multipliers = [None, 4, 4]  # 各列のデータを10の乗数で割る，Noneの場合は乗算をしない
    summarizeCsvToLatex(name, significant_figure, multipliers)
