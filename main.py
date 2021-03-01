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

# ログの定義
logger = mylogger.setup_logger(__name__)

# ギフトショップのシート名の辞書
global_giftshop_sheetname_dic = {}

# NAVITIMEのシート名の辞書
global_navitime_sheetname_dic = {}

# MAPIONのシート名の辞書
global_mapion_sheetname_dic = {}

# 情報屋のシート名の辞書
global_johouya_sheetname_dic = {}


# 有効期限のチェック
def expexpiration_date_check():
    import datetime
    now = datetime.datetime.now()
    expexpiration_datetime = now.replace(month=3, day=17, hour=12, minute=0, second=0, microsecond=0)
    logger.info("有効期限：" + str(expexpiration_datetime))
    if now < expexpiration_datetime:
        return True
    else:
        return False

# 画面の表示
def main():

    root = Tk()
    #タイトル
    root.title('検索結果取得')
    root.minsize(350, 200)

    frmMain = Frame(root)

    #Configure the row/col of our frame and root window to be resizable and fill all available space
    frmMain.grid(row=0, column=0, sticky="NESW")
    frmMain.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Label Frame
    labelframe = tkinter.LabelFrame(frmMain, width=320, height=140, text="取得対象のサイト")
    labelframe.grid(row=0, column=0, pady=10, ipadx=10, ipady=10)

    # radioValue = tkinter.IntVar()
    # rdioOne = tkinter.Radiobutton(labelframe, text='Googleマップとgoo地図両方',
    #                          variable=radioValue, value=0)
    # rdioTwo = tkinter.Radiobutton(labelframe, text='Googleマップのみ',
    #                          variable=radioValue, value=1)
    # rdioThree = tkinter.Radiobutton(labelframe, text='goo地図のみ',
    #                          variable=radioValue, value=2)
    # rdioOne.grid(row=0, column=0, padx=5)
    # rdioTwo.grid(row=0, column=1, padx=5)
    # rdioThree.grid(row=0, column=2, padx=5)
    # # ラジオボタンの初期値を設定する
    # radioValue.set(0)

    # ギフトショップ検索チェックボックス
    giftshop_chk_state = BooleanVar()
    giftshop_chk_state.set(True)
    giftshop_chk = Checkbutton(labelframe, text='ギフトショップを検索する', var=giftshop_chk_state)
    giftshop_chk.grid(row=0, column=0, padx=10, sticky=tkinter.W)

    # NAVITIME検索チェックボックス
    navitime_chk_state = BooleanVar()
    navitime_chk_state.set(True)
    navitime_chk = Checkbutton(labelframe, text='NAVITIMEを検索する', var=navitime_chk_state)
    navitime_chk.grid(row=1, column=0, padx=10, sticky=tkinter.W)

    # MAPION検索チェックボックス
    mapion_chk_state = BooleanVar()
    mapion_chk_state.set(True)
    mapion_chk = Checkbutton(labelframe, text='MAPIONを検索する', var=mapion_chk_state)
    mapion_chk.grid(row=2, column=0, padx=10, sticky=tkinter.W)

    # 情報屋さん検索チェックボックス
    jouhouya_chk_state = BooleanVar()
    jouhouya_chk_state.set(True)
    jouhouya_chk = Checkbutton(labelframe, text='街の情報屋さんを検索する', var=jouhouya_chk_state)
    jouhouya_chk.grid(row=3, column=0, padx=10, sticky=tkinter.W)

    # 実行ボタン
    InputButton = Button(frmMain, text="取得開始",
                         command = lambda : execute_scraip(giftshop_chk_state.get(), navitime_chk_state.get(),
                                                           mapion_chk_state.get(), jouhouya_chk_state.get()))
    InputButton.grid(row=1, column=0)

    root.mainloop()


def execute_scraip(giftshop_flg, navitime_flg, mapion_flg, jouhouya_flg):

    # 有効期限チェック
    if not (expexpiration_date_check()):
        logger.info("有効期限切れため、プログラム起動終了")
        messagebox.showerror("エラー", "有効期限切れのため、処理を実行できません。")
        return

    try:
        logger.info("取得開始ボタンクリック")
        logger.info("ギフトショップ：" + str(giftshop_flg))
        logger.info("NAVITIME：" + str(navitime_flg))
        logger.info("MAPION：" + str(mapion_flg))
        logger.info("街の情報屋さん：" + str(jouhouya_flg))

        # 検索対象リスト
        search_list = []

        logger.info('処理を開始します')
        logger.info('検索情報リストの読み込みを開始します')

        # 検索リストファイルの読み込み（全て欠損値がある行は読み込まない）
        search_df = settings.read_search_list("./設定ファイル.xlsx", "検索設定", 0, "B:E", 0)

        for i in range(0, len(search_df)):

            _search = SearchInputInfo()
            _search.industry = search_df.iloc[i][0]
            _search.area = search_df.iloc[i][1]
            _search.prefecture = search_df.iloc[i][2]
            _search.exclusion_genre = search_df.iloc[i][3]

            # リストに追加
            search_list.append(_search)

        logger.info('検索情報リストの読み込みが完了しました')

        giftshop_file_path = ""
        giftshop_sheetname = ""
        navitime_file_path = ""
        navitime_sheetname = ""
        mapion_file_path = ""
        mapion_sheetname = ""
        jouhouya_file_path = ""
        jouhouya_sheetname = ""

        merge_flg = 0

        if giftshop_flg:
            giftshop_main(search_list)
            giftshop_file_path = "./output/ギフトショップ検索結果.xlsx"
            merge_flg += 1

        if navitime_flg:
            navitime_main(search_list)
            navitime_file_path = "./output/NAVITIME検索結果.xlsx"
            merge_flg += 1

        if mapion_flg:
            mapion_main(search_list)
            mapion_file_path = "./output/MAPION検索結果.xlsx"
            merge_flg += 1

        if jouhouya_flg:
            jouhouya_main(search_list)
            jouhouya_file_path = "./output/街の情報屋さん検索結果.xlsx"
            merge_flg += 1

        # ファイルをマージした結果を作成
        if merge_flg >= 2:
            for index in range(1, len(global_giftshop_sheetname_dic) + 1):
                # シート名を取得
                if len(global_giftshop_sheetname_dic):
                    giftshop_sheetname = global_giftshop_sheetname_dic[index]
                if len(global_navitime_sheetname_dic):
                    navitime_sheetname = global_navitime_sheetname_dic[index]
                if len(global_mapion_sheetname_dic):
                    mapion_sheetname = global_mapion_sheetname_dic[index]
                if len(global_johouya_sheetname_dic):
                    jouhouya_sheetname = global_johouya_sheetname_dic[index]

                # マージ処理呼び出し
                excel.merge_excel(giftshop_file_path, navitime_file_path, mapion_file_path, jouhouya_file_path,
                                    giftshop_sheetname, navitime_sheetname, mapion_sheetname, jouhouya_sheetname)

        messagebox.showinfo("実行結果", "処理が完了しました。")
        logger.info('処理が完了しました')

    except Exception as err:
        messagebox.showerror("実行結果", "処理が失敗しました。")
        logger.error('処理が失敗しました')
        logger.error(err)
        logger.error(traceback.format_exc())


def giftshop_main(search_list):

    # ギフトショップキーワード検索処理
    logger.info('ギフトショップ検索処理を開始します')
    GIFTSHOP_BASE_URL = "http://gift.nskdata.com/search/search.php?"
    SEARCH_PARAM = "&sub=検索"

    # ブラウザ表示オプションの取得
    DISPLAY = "1"

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in search_list:

        prefecture_param1 = "k1=" + search_dr.prefecture
        prefecture_param2 = "k2=" + search_dr.industry

        target_url = GIFTSHOP_BASE_URL + prefecture_param1  + "&" + prefecture_param2 + SEARCH_PARAM

        output_excel_list = []

        output_list = scraip.search_giftshop(driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, search_dr.industry + "_" + search_dr.prefecture, search_dr, 1)

        # 辞書にシート名を登録
        global_giftshop_sheetname_dic[sheet_index] = search_dr.industry + "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def navitime_main(search_list):

    # NAVITIMEキーワード検索処理
    logger.info('NAVITIME検索処理を開始します')
    NAVITIME_BASE_URL = "https://www.navitime.co.jp/freeword/?"
    SEARCH_PARAM = "&type=spot&from=freeword.spotlist"

    # ブラウザ表示オプションの取得
    DISPLAY = "1"

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in search_list:

        query_param = "keyword=" + search_dr.industry + "+" + search_dr.prefecture

        target_url = NAVITIME_BASE_URL + query_param + SEARCH_PARAM

        output_excel_list = []

        output_list = scraip.search_navitime(driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, search_dr.industry + "_" + search_dr.prefecture, search_dr, 2)

        # 辞書にシート名を登録
        global_navitime_sheetname_dic[sheet_index] = search_dr.industry + "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def mapion_main(search_list):

    # MAPIONキーワード検索処理
    logger.info('MAPION検索処理を開始します')
    MAPION_BASE_URL = "https://www.mapion.co.jp/s/"
    SEARCH_PARAM = "/t=spot/"

    # ブラウザ表示オプションの取得
    DISPLAY = "1"

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in search_list:

        query_param = "q=" + search_dr.industry + "%20" + search_dr.prefecture

        target_url = MAPION_BASE_URL + query_param + SEARCH_PARAM

        output_excel_list = []

        output_list = scraip.search_mapion(driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, search_dr.industry + "_" + search_dr.prefecture, search_dr, 3)

        # 辞書にシート名を登録
        global_mapion_sheetname_dic[sheet_index] = search_dr.industry + "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


def jouhouya_main(search_list):

    # 街の情報屋さんキーワード検索処理
    logger.info('街の情報屋さん検索処理を開始します')
    JOHOUYA_BASE_URL = "https://www.24u.jp/"

    # ブラウザ表示オプションの取得
    DISPLAY = "1"

    # ドライバー生成処理
    driver = scraip.create_driver()

    sheet_index = 1

    for search_dr in search_list:

        target_url = JOHOUYA_BASE_URL

        output_excel_list = []

        output_list = scraip.search_jouhouya(driver, target_url, search_dr.prefecture, search_dr.industry)
        output_excel_list.extend(output_list)

        excel.out_to_excel(output_excel_list, search_dr.industry + "_" + search_dr.prefecture, search_dr, 4)

        # 辞書にシート名を登録
        global_johouya_sheetname_dic[sheet_index] = search_dr.industry + "_" + search_dr.prefecture
        sheet_index += 1

    # ブラウザを終了する。
    driver.quit()


if __name__ == '__main__':

    main()