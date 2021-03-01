import configparser
import pandas as pd


def read_config(section):
    # coding: utf-8
    # --------------------------------------------------
    # iniファイルの読み込み
    # --------------------------------------------------
    config_ini = configparser.ConfigParser()
    config_ini.read('config.ini', encoding='utf-8')

    return config_ini[section]


# how_load（0：全て空の場合その行は読み込まない、1：どれか１つでも空の場合その行は読み込まない）
def read_search_list(file_path, sheet_name, header_idx, cols, how_load):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_idx, usecols=cols)
    if how_load == 0:
        # データフレームから全て空白の値の行を削除する
        df_formatted = df.dropna(how='all', axis=0)
    else:
        # データフレームから空白の値を含む行を削除する
        df_formatted = df.dropna(how='any', axis=0)
    # 業種と都道府県がNaNの行は削除する
    #df_formatted = df.dropna(subset=['業種','都道府県'])
    df_ret = df_formatted.fillna('')
    return df_ret


def read_postal_code(prefecture, municipality, area, address):
    params = {}
    params['prefecture'] = prefecture
    params['municipality'] = municipality
    params['area'] = area
    params['address'] = address

    # zip圧縮されたcsvを読み込む
    csvfile = './csv/ken_all.zip'
    df = pd.read_csv(csvfile, compression='zip', header=None, quotechar='"', dtype=object, encoding='shift_jis')

    # 郵便番号をインデックスにする
    df.set_index(df.columns[2], inplace=True)

    # 県と市区町村とエリアを結合する
    df_join = df[df.columns[5]].str.cat(df[df.columns[6]]).str.cat(df[df.columns[7]])
    df_filtered = df[df_join.str.contains(params['address'], regex=False)]

    # df_filtered = df[
    #     df[df.columns[5]].str.contains(params['prefecture'], regex=False) &
    #     df[df.columns[6]].str.contains(params['municipality'], regex=False) &
    #     df[df.columns[7]].str.contains(params['area'], regex=False)]

    if len(df_filtered.index) == 0:
        #print('No zip code was found.')
        return "-"
    else:
        for zip_code, row in df_filtered.iterrows():
            #print(zip_code + ' ' + ' '.join(row.tolist()[5:8]))
            return zip_code


if __name__ == '__main__':
    read_postal_code("", "", "", "愛媛県愛南町福浦")