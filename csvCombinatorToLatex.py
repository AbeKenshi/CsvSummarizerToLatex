# csvファイルのデータをtexのテーブル形式に変換するプログラム
import pandas as pd
import numpy as np


def combinateCsvToLatex(file_name, names, method_names, significant_figure, multipliers, isStd):
    dfs = []
    for h in range(len(names)):
        name = names[h]
        df = pd.DataFrame.from_csv(name + ".csv", encoding="shift-jis")  # ファイル読み込み
        if len(df.columns) != len(significant_figure):
            raise ValueError(
                "The length of the array of significant figure does not match the number of columns of data.")
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
                dfn.index = df.index
                df.ix[:, [i]] = dfn
        df.ix[:, :] = df.ix[:, :].astype(str)
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                if str_isdigit(df.ix[i, j]):
                    while significant_figure[j] != None and len_str(df.ix[i, j]) < significant_figure[j]:
                        df.ix[i, j] += "0"

        for i in range(len(df.columns)):
            if isStd[i]:
                df.ix[:, i - 1] = df.ix[:, i - 1] + "(\pm " + df.ix[:, i] + ")"
                df = df.drop(df.columns[i], axis=1)

        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                df.ix[i, j] = " $" + str(df.ix[i, j]) + "$ "
        df['手法'] = [ " " + method_names[h] + " " for i in range(len(df.index))]
        newcolumns = []
        newcolumns.append(df.columns[len(df.columns) - 1])
        for i in range(len(df.columns) - 1):
            newcolumns.append(df.columns[i])
        df = df[newcolumns]
        if h != 0:
            df.index = ["" for i in range(len(df.index))]
        dfs.append(df)
    dfa = pd.DataFrame()
    for h in range(len(dfs[0].index)):
        for i in range(0, len(dfs)):
            dfa = dfa.append(dfs[i].ix[[h], :])
    # インデックスを出力する必要がない場合，index=Falseとする
    dfa.to_csv(file_name + ".tex", sep='&', line_terminator='\\\\ \hline\n', quotechar=" ", index=True)


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
    task = "mountaincar"
    file_name = "log/summarize_" + task
    names = ["log/isSuccessed_ebpnes_" + task, "log/isSuccessed_sapga_" + task, "log/isSuccessed_esapga_" + task]
    method_names = ["EBP-NES", "SAP-GA", "eSAP-GA"]
    significant_figure = [None, 3, 3]  # 有効桁数，Noneの場合は桁数調整をしない
    multipliers = [None, 2, 2]  # 各列のデータを10の乗数で割る，Noneの場合は乗算をしない
    isStd = [False, False, True]  # 標準偏差かどうか，標準偏差なら左のやつと結合
    combinateCsvToLatex(file_name, names, method_names, significant_figure, multipliers, isStd)
