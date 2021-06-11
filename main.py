import os
import traceback
import pandas as pd
import tkinter
from tkinter import *
from tkinter import messagebox, ttk

import settings
import scraip
from search_list import SearchInputInfo
import excel
import mylogger
import search_list
import map_scraip

# ログの定義
logger = mylogger.setup_logger(__name__)

# Googleマップのシート名の辞書
global_google_sheetname_dic = {}

# goo地図のシート名の辞書
global_goo_sheetname_dic = {}

# ギフトショップのシート名の辞書
global_giftshop_sheetname_dic = {}

# NAVITIMEのシート名の辞書
global_navitime_sheetname_dic = {}

# MAPIONのシート名の辞書
global_mapion_sheetname_dic = {}

# 情報屋のシート名の辞書
global_johouya_sheetname_dic = {}

# おでかけタウン情報のシート名の辞書
global_odekake_sheetname_dic = {}

# Hotflogのシート名の辞書
global_hotflog_sheetname_dic = {}


# 有効期限のチェック
def expexpiration_date_check():
    import datetime
    now = datetime.datetime.now()
    expexpiration_datetime = now.replace(
        month=4, day=17, hour=12, minute=0, second=0, microsecond=0)
    logger.info("有効期限：" + str(expexpiration_datetime))
    if now < expexpiration_datetime:
        return True
    else:
        return False

# 画面の表示


def main():

    root = Tk()
    # タイトル
    root.title('検索結果取得')
    root.minsize(450, 250)

    frmMain = Frame(root)

    # Configure the row/col of our frame and root window to be resizable and fill all available space
    frmMain.grid(row=0, column=0, sticky="NESW")
    frmMain.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Label Frame1
    labelframe1 = tkinter.LabelFrame(
        frmMain, width=320, height=140, text="取得対象の地図サイト")
    labelframe1.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10)

    # Googleマップ検索チェックボックス
    google_chk_state = BooleanVar()
    google_chk_state.set(True)
    google_chk = Checkbutton(
        labelframe1, text='Googleマップを検索する', var=google_chk_state)
    google_chk.grid(row=0, column=0, padx=10, sticky=tkinter.W)

    # goo地図検索チェックボックス
    goo_chk_state = BooleanVar()
    goo_chk_state.set(True)
    goo_chk = Checkbutton(labelframe1, text='goo地図を検索する', var=goo_chk_state)
    goo_chk.grid(row=1, column=0, padx=10, sticky=tkinter.W)

    googleRadioValue = tkinter.IntVar()
    rdioOne = tkinter.Radiobutton(labelframe1, text='Googleマップで市区町村を含めない',
                                  variable=googleRadioValue, value=0)
    rdioTwo = tkinter.Radiobutton(labelframe1, text='Googleマップで市区町村を含める　',
                                  variable=googleRadioValue, value=1)
    rdioOne.grid(row=2, column=0, padx=5)
    rdioTwo.grid(row=3, column=0, padx=5)
    # ラジオボタンの初期値を設定する
    googleRadioValue.set(0)

    # Label Frame2
    labelframe2 = tkinter.LabelFrame(
        frmMain, width=320, height=140, text="取得対象の検索サイト")
    labelframe2.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10)

    # ギフトショップ検索チェックボックス
    giftshop_chk_state = BooleanVar()
    giftshop_chk_state.set(True)
    giftshop_chk = Checkbutton(
        labelframe2, text='ギフトショップを検索する', var=giftshop_chk_state)
    giftshop_chk.grid(row=0, column=0, padx=10, sticky=tkinter.W)

    # NAVITIME検索チェックボックス
    navitime_chk_state = BooleanVar()
    navitime_chk_state.set(True)
    navitime_chk = Checkbutton(
        labelframe2, text='NAVITIMEを検索する', var=navitime_chk_state)
    navitime_chk.grid(row=1, column=0, padx=10, sticky=tkinter.W)

    # MAPION検索チェックボックス
    mapion_chk_state = BooleanVar()
    mapion_chk_state.set(True)
    mapion_chk = Checkbutton(
        labelframe2, text='MAPIONを検索する', var=mapion_chk_state)
    mapion_chk.grid(row=2, column=0, padx=10, sticky=tkinter.W)

    # 情報屋さん検索チェックボックス
    jouhouya_chk_state = BooleanVar()
    jouhouya_chk_state.set(True)
    jouhouya_chk = Checkbutton(
        labelframe2, text='街の情報屋さんを検索する', var=jouhouya_chk_state)
    jouhouya_chk.grid(row=3, column=0, padx=10, sticky=tkinter.W)

    # おでかけタウン情報検索チェックボックス
    odekake_chk_state = BooleanVar()
    odekake_chk_state.set(True)
    odekake_chk = Checkbutton(
        labelframe2, text='おでかけタウン情報を検索する', var=odekake_chk_state)
    odekake_chk.grid(row=4, column=0, padx=10, sticky=tkinter.W)

    # Hotflog検索チェックボックス
    hotflog_chk_state = BooleanVar()
    hotflog_chk_state.set(True)
    hotflog_chk = Checkbutton(
        labelframe2, text='Hotflogを検索する', var=hotflog_chk_state)
    hotflog_chk.grid(row=0, column=1, padx=10, sticky=tkinter.W)

    # 実行ボタン
    InputButton = Button(frmMain, text="取得開始",
                         command=lambda: execute_scraip(google_chk_state.get(), googleRadioValue.get(), goo_chk_state.get(),
                                                        giftshop_chk_state.get(), navitime_chk_state.get(),
                                                        mapion_chk_state.get(), jouhouya_chk_state.get(),
                                                        odekake_chk_state.get(), hotflog_chk_state.get()))
    InputButton.grid(row=2, column=1)

    root.mainloop()


def execute_scraip(google_flg, google_radio_flg, goo_flg, giftshop_flg, navitime_flg, mapion_flg, jouhouya_flg, odekake_flg, hotflog_flg):

    # # 有効期限チェック
    # if not (expexpiration_date_check()):
    #     logger.info("有効期限切れため、プログラム起動終了")
    #     messagebox.showerror("エラー", "有効期限切れのため、処理を実行できません。")
    #     return

    try:
        logger.info("取得開始ボタンクリック")

        logger.info("Googleマップ：" + str(google_flg))
        logger.info("goo地図：" + str(goo_flg))
        logger.info("ギフトショップ：" + str(giftshop_flg))
        logger.info("NAVITIME：" + str(navitime_flg))
        logger.info("MAPION：" + str(mapion_flg))
        logger.info("街の情報屋さん：" + str(jouhouya_flg))
        logger.info("おでかけタウン情報：" + str(odekake_flg))
        logger.info("Hotfrog：" + str(hotflog_flg))

        # 検索対象リスト
        tmp_search_list = []
        odekake_search_list = []

        logger.info('処理を開始します')
        logger.info('検索情報リストの読み込みを開始します')

        # 検索リストファイルの読み込み（全て欠損値がある行は読み込まない）
        search_df = settings.read_search_list(
            "./設定ファイル.xlsx", "検索設定", 0, "B:E", 0)
        odekake_search_df = settings.read_search_list(
            "./設定ファイル.xlsx", "おでかけタウン情報検索設定", 0, "B:E", 0)

        for i in range(0, len(search_df)):
            _search = SearchInputInfo()
            _search.industry = search_df.iloc[i][0]
            _search.area = search_df.iloc[i][1]
            _search.prefecture = search_df.iloc[i][2]
            _search.exclusion_genre = search_df.iloc[i][3]
            # リストに追加
            tmp_search_list.append(_search)

        for i in range(0, len(odekake_search_df)):
            tmp_search = SearchInputInfo()
            tmp_search.industry = odekake_search_df.iloc[i][0]
            tmp_search.area = odekake_search_df.iloc[i][1]
            tmp_search.prefecture = odekake_search_df.iloc[i][2]
            target_str = str(odekake_search_df.iloc[i][3])
            tmp_search.target_industry_str = target_str
            tmp_search.target_industry_list = target_str.split(",")
            # リストに追加
            odekake_search_list.append(tmp_search)

        logger.info('検索情報リストの読み込みが完了しました')

        giftshop_file_path = ""
        giftshop_sheetname = ""
        navitime_file_path = ""
        navitime_sheetname = ""
        mapion_file_path = ""
        mapion_sheetname = ""
        jouhouya_file_path = ""
        jouhouya_sheetname = ""
        odekake_file_path = ""
        odekake_sheetname = ""
        google_file_path = ""
        google_sheet_name = ""
        goo_file_path = ""
        goo_sheet_name = ""
        hotflog_file_path = ""
        hotflog_sheet_name = ""

        merge_flg = 0

        if google_flg:
            google_map_main(google_radio_flg)
            google_file_path = './output/Googleマップ検索結果.xlsx'
            merge_flg += 1

        if goo_flg:
            goo_map_main()
            goo_file_path = './output/goo地図検索結果.xlsx'
            merge_flg += 1

        if giftshop_flg:
            giftshop_main(tmp_search_list)
            giftshop_file_path = "./output/ギフトショップ検索結果.xlsx"
            merge_flg += 1

        if navitime_flg:
            navitime_main(tmp_search_list)
            navitime_file_path = "./output/NAVITIME検索結果.xlsx"
            merge_flg += 1

        if mapion_flg:
            mapion_main(tmp_search_list)
            mapion_file_path = "./output/MAPION検索結果.xlsx"
            merge_flg += 1

        if jouhouya_flg:
            jouhouya_main(tmp_search_list)
            jouhouya_file_path = "./output/街の情報屋さん検索結果.xlsx"
            merge_flg += 1

        if odekake_flg:
            odekake_main(odekake_search_list)
            odekake_file_path = "./output/おでかけタウン情報検索結果.xlsx"
            merge_flg += 1

        if hotflog_flg:
            hotflog_main(tmp_search_list)
            hotflog_file_path = "./output/Hotflog検索結果.xlsx"
            merge_flg += 1

        # ファイルをマージした結果を作成
        if merge_flg >= 2:

            for index in range(1, len(global_giftshop_sheetname_dic) + 1):
                excel_item_list = []
                # シート名を取得
                if len(global_google_sheetname_dic) >= index:
                    google_sheet_name = global_google_sheetname_dic[index]
                    _excel_list = search_list.ExcelList()
                    _excel_list.out_file_path = google_file_path
                    _excel_list.sheet_name = google_sheet_name
                    excel_item_list.append(_excel_list)

                if len(global_goo_sheetname_dic) >= index:
                    goo_sheet_name = global_goo_sheetname_dic[index]
                    _excel_list = search_list.ExcelList()
                    _excel_list.out_file_path = goo_file_path
                    _excel_list.sheet_name = goo_sheet_name
                    excel_item_list.append(_excel_list)

                if len(global_giftshop_sheetname_dic) >= index:
                    giftshop_sheetname = global_giftshop_sheetname_dic[index]
                    _excel_list = search_list.ExcelList()
                    _excel_list.out_file_path = giftshop_file_path
                    _excel_list.sheet_name = giftshop_sheetname
                    excel_item_list.append(_excel_list)

                if len(global_navitime_sheetname_dic) >= index:
                    navitime_sheetname = global_navitime_sheetname_dic[index]
                    _excel_list = search_list.ExcelList()
                    _excel_list.out_file_path = navitime_file_path
                    _excel_list.sheet_name = navitime_sheetname
                    excel_item_list.append(_excel_list)

                if len(global_mapion_sheetname_dic) >= index:
                    mapion_sheetname = global_mapion_sheetname_dic[index]
                    _excel_list = search_list.ExcelList()
                    _excel_list.out_file_path = mapion_file_path
                    _excel_list.sheet_name = mapion_sheetname
                    excel_item_list.append(_excel_list)

                if len(global_johouya_sheetname_dic) >= index:
                    jouhouya_sheetname = global_johouya_sheetname_dic[index]
                    _excel_list = search_list.ExcelList()
                    _excel_list.out_file_path = jouhouya_file_path
                    _excel_list.sheet_name = jouhouya_sheetname
                    excel_item_list.append(_excel_list)

                if len(global_odekake_sheetname_dic) >= index:
                    odekake_sheetname = global_odekake_sheetname_dic[index]
                    _excel_list = search_list.ExcelList()
                    _excel_list.out_file_path = odekake_file_path
                    _excel_list.sheet_name = odekake_sheetname
                    excel_item_list.append(_excel_list)

                if len(global_hotflog_sheetname_dic) >= index:
                    hotflog_sheet_name = global_hotflog_sheetname_dic[index]
                    _excel_list = search_list.ExcelList()
                    _excel_list.out_file_path = hotflog_file_path
                    _excel_list.sheet_name = hotflog_sheet_name
                    excel_item_list.append(_excel_list)

                # マージ処理呼び出し
                excel.merge_excel(excel_item_list)

        messagebox.showinfo("実行結果", "処理が完了しました。")
        logger.info('処理が完了しました')

    except Exception as err:
        messagebox.showerror("実行結果", "処理が失敗しました。")
        logger.error('処理が失敗しました')
        logger.error(err)
        logger.error(traceback.format_exc())


def goo_map_main():
    # 検索対象リスト
    goo_search_list = []
    # 検索成功した商品リスト
    goo_success_list = []
    # 検索スキップした商品リスト
    goo_skip_list = []

    logger.info('処理を開始します')
    logger.info('検索情報リストの読み込みを開始します')

    SITE_NAME = 'goo地図'

    # goo地図検索リストファイルの読み込み（全て欠損値がある行は読み込まない）
    search_df = settings.read_search_list(
        "./設定ファイル.xlsx", "goo地図設定", 0, "B:E", 0)

    for i in range(0, len(search_df)):

        _search = SearchInputInfo()
        _search.industry = search_df.iloc[i][0]
        _search.area = search_df.iloc[i][1]
        _search.prefecture = search_df.iloc[i][2]
        _search.exclusion_genre = search_df.iloc[i][3]

        # リストに追加
        goo_search_list.append(_search)

    logger.info('検索情報リストの読み込みが完了しました')

    # goo地図キーワード検索処理
    logger.info('検索処理を開始します')
    GOO_MAP_URL = "https://map.goo.ne.jp"

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in goo_search_list:

        output_excel_list = []

        # キーワード作成
        search_keyword = search_dr.industry + " " + search_dr.prefecture
        output_list = map_scraip.search_goo_map(
            driver, search_keyword, GOO_MAP_URL)
        if output_list or len(output_list):
            output_excel_list.extend(output_list)
            goo_success_list.append(
                search_dr.industry + "-" + search_dr.prefecture)
        else:
            goo_skip_list.append(search_dr.industry +
                                 "-" + search_dr.prefecture)

        excel.out_to_excel(output_excel_list, search_dr.industry +
                           "_" + search_dr.prefecture, search_dr, SITE_NAME, 6)

        # 辞書にシート名を登録
        global_goo_sheetname_dic[sheet_index] = search_dr.industry + \
            "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def google_map_main(google_search_mode):
    # 検索対象リスト
    google_search_list = []
    # 検索成功した商品リスト
    google_success_list = []
    # 検索スキップした商品リスト
    google_skip_list = []

    logger.info('Googleマップ処理を開始します')
    logger.info('Googleマップ検索情報リストの読み込みを開始します')

    SITE_NAME = 'Googleマップ'

    # Googleマップの検索リストファイルの読み込み（全て欠損値がある行は読み込まない）
    search_df = settings.read_search_list(
        "./設定ファイル.xlsx", "Googleマップ設定", 0, "B:E", 0)

    for i in range(0, len(search_df)):

        _search = SearchInputInfo()
        _search.setFromExcelRow(search_df.iloc[i])

        # Googleマップの検索対象の市区町村リストの読み込み（全て欠損値がある行は読み込まない）
        if google_search_mode == 1:
            municipality_df = settings.read_search_list(
                "./設定ファイル.xlsx", "市区町村", 0, "B:C", 1)
            target_municipality_df = municipality_df[municipality_df['都道府県名'].str.contains(
                _search.prefecture)]
            target_municipality_list = target_municipality_df['市区町村名'].values.tolist(
            )
            _search.municipality_list = target_municipality_list

        # リストに追加
        google_search_list.append(_search)

    logger.info('Googleマップ検索情報リストの読み込みが完了しました')

    # Googleキーワード検索処理
    logger.info('Googleマップ検索処理を開始します')
    GOOGLE_MAP_URL = "https://www.google.co.jp/maps/?hl=ja"

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in google_search_list:

        output_excel_list = []

        if google_search_mode == 1:
            for search_municipality in search_dr.municipality_list:
                # キーワード作成
                search_keyword = search_dr.industry + " " + \
                    search_dr.prefecture + search_municipality
                output_list = map_scraip.search_google_map(
                    driver, search_keyword, GOOGLE_MAP_URL)
                if output_list or len(output_list):
                    output_excel_list.extend(output_list)
                    google_success_list.append(
                        search_dr.industry + "-" + search_dr.prefecture + "-" + search_municipality)
                else:
                    google_skip_list.append(
                        search_dr.industry + "-" + search_dr.prefecture + "-" + search_municipality)

        else:
            # キーワード作成
            search_keyword = search_dr.industry + " " + search_dr.prefecture
            output_list = map_scraip.search_google_map(
                driver, search_keyword, GOOGLE_MAP_URL)
            if output_list or len(output_list):
                output_excel_list.extend(output_list)
                google_success_list.append(
                    search_dr.industry + "-" + search_dr.prefecture)
            else:
                google_skip_list.append(
                    search_dr.industry + "-" + search_dr.prefecture)

        excel.out_to_excel(output_excel_list, search_dr.industry +
                           "_" + search_dr.prefecture, search_dr, SITE_NAME, 7)

        # 辞書にシート名を登録
        global_google_sheetname_dic[sheet_index] = search_dr.industry + \
            "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def giftshop_main(search_list):

    # ギフトショップキーワード検索処理
    logger.info('ギフトショップ検索処理を開始します')
    GIFTSHOP_BASE_URL = "http://gift.nskdata.com/search/search.php?"
    SEARCH_PARAM = "&sub=検索"

    SITE_NAME = 'ギフトショップ'

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in search_list:

        prefecture_param1 = "k1=" + search_dr.prefecture
        prefecture_param2 = "k2=" + search_dr.industry

        target_url = GIFTSHOP_BASE_URL + prefecture_param1 + \
            "&" + prefecture_param2 + SEARCH_PARAM

        output_excel_list = []

        output_list = scraip.search_giftshop(
            driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, search_dr.industry +
                           "_" + search_dr.prefecture, search_dr, SITE_NAME, 1)

        # 辞書にシート名を登録
        global_giftshop_sheetname_dic[sheet_index] = search_dr.industry + \
            "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def navitime_main(search_list):

    # NAVITIMEキーワード検索処理
    logger.info('NAVITIME検索処理を開始します')
    NAVITIME_BASE_URL = "https://www.navitime.co.jp/freeword/?"
    SEARCH_PARAM = "&type=spot&from=freeword.spotlist"

    SITE_NAME = 'NAVITIME'

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in search_list:

        query_param = "keyword=" + search_dr.industry + "+" + search_dr.prefecture

        target_url = NAVITIME_BASE_URL + query_param + SEARCH_PARAM

        output_excel_list = []

        output_list = scraip.search_navitime(
            driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, search_dr.industry +
                           "_" + search_dr.prefecture, search_dr, SITE_NAME, 2)

        # 辞書にシート名を登録
        global_navitime_sheetname_dic[sheet_index] = search_dr.industry + \
            "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def mapion_main(search_list):

    # MAPIONキーワード検索処理
    logger.info('MAPION検索処理を開始します')
    MAPION_BASE_URL = "https://www.mapion.co.jp/s/"
    SEARCH_PARAM = "/t=spot/"

    SITE_NAME = 'MAPION'

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in search_list:

        query_param = "q=" + search_dr.industry + "%20" + search_dr.prefecture

        target_url = MAPION_BASE_URL + query_param + SEARCH_PARAM

        output_excel_list = []

        output_list = scraip.search_mapion(
            driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, search_dr.industry +
                           "_" + search_dr.prefecture, search_dr, SITE_NAME, 3)

        # 辞書にシート名を登録
        global_mapion_sheetname_dic[sheet_index] = search_dr.industry + \
            "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def jouhouya_main(search_list):

    # 街の情報屋さんキーワード検索処理
    logger.info('街の情報屋さん検索処理を開始します')
    JOHOUYA_BASE_URL = "https://www.24u.jp/"

    SITE_NAME = '街の情報屋さん'

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in search_list:

        target_url = JOHOUYA_BASE_URL

        output_excel_list = []

        output_list = scraip.search_jouhouya(
            driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, search_dr.industry +
                           "_" + search_dr.prefecture, search_dr, SITE_NAME, 4)

        # 辞書にシート名を登録
        global_johouya_sheetname_dic[sheet_index] = search_dr.industry + \
            "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def odekake_main(search_list):

    # おでかけタウン情報キーワード検索処理
    logger.info('おでかけタウン情報検索処理を開始します')
    ODEKAKE_BASE_URL = "http://www.gekinavi.net/"

    SITE_NAME = 'おでかけタウン情報'

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in search_list:

        target_url = ODEKAKE_BASE_URL

        output_excel_list = []
        sheet_name = ''
        if len(search_dr.target_industry_str):
            sheet_name = (search_dr.industry + "_" + search_dr.prefecture +
                          "_" + search_dr.target_industry_str)[:30]
        else:
            sheet_name = (search_dr.industry + "_" + search_dr.prefecture)[:30]

        output_list = scraip.search_odekake(
            driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, sheet_name,
                           search_dr, SITE_NAME, 5)

        # 辞書にシート名を登録
        global_odekake_sheetname_dic[sheet_index] = sheet_name
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def hotflog_main(search_list):

    # Hotflog検索処理
    logger.info('Hotflog検索処理を開始します')
    HOTFLOG_BASE_URL = "https://www.hotfrog.jp/"

    SITE_NAME = 'Hotflog'

    # ドライバー生成処理
    driver = scraip.create_driver(headless_flg=False)

    sheet_index = 1

    for search_dr in search_list:

        target_url = HOTFLOG_BASE_URL + 'search/' + \
            search_dr.prefecture + '/' + search_dr.industry

        output_excel_list = []

        output_list = scraip.search_hotflog(
            driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, search_dr.industry +
                           "_" + search_dr.prefecture, search_dr, SITE_NAME, 8)

        # 辞書にシート名を登録
        global_hotflog_sheetname_dic[sheet_index] = search_dr.industry + \
            "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


if __name__ == '__main__':

    main()
