# csvファイルのデータをtexのテーブル形式に変換するプログラム
import pandas as pd
import numpy as np


def round_sig(x, sig=2):
    y = [np.around(x[i], sig - np.int_(np.floor(np.log10(abs(x[i] + 1e-200)))) - 1) for i in range(len(x))]
    return y


significant_figure = [None, 3, 3]  # 有効桁数，Noneの場合は桁数調整をしない
multipliers = [None, 4, 4]  # 各列のデータを10の乗数で割る，Noneの場合は乗算をしない

name = "sample/sample"  # ファイル名
df = pd.DataFrame.from_csv(name + ".csv")  # ファイル読み込み
df.columns = ["成功回数",
              "平均評価回数($\\times10^" + str(multipliers[1]) + "$)",
              "標準偏差($\\times10^" + str(multipliers[2]) + "$)"]
for i in range(len(df.columns)):
    if multipliers[i] != None:
        df.ix[:, [i]] = df.ix[:, [i]] / (10 ** multipliers[i])
    if significant_figure[i] != None:
        s_orig = df.ix[:, [i]].as_matrix()
        s_orig = round_sig(s_orig, significant_figure[i])
        # print(pd.DataFrame(s_orig))
        dfn = pd.DataFrame(s_orig)
        dfn.columns = [df.columns[i]]
        df.ix[:, [i]] = dfn

df.to_csv(name + ".tex", sep='&', line_terminator='\\\\ \hline\n', quotechar=" ")
