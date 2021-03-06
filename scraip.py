import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
#import chromedriver_binary
from search_list import SearchInputInfo, SearchOutputInfo
import re
from selenium.common.exceptions import TimeoutException
import settings
import mylogger
import urllib

# ログの定義
logger = mylogger.setup_logger(__name__)


def create_driver(headless_flg=False):
    # chromeドライバーのパス
    chrome_path = "./driver/chromedriver.exe"

    # Selenium用オプション
    op = Options()
    op.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15')
    op.add_experimental_option("excludeSwitches", ["enable-automation"])
    op.add_experimental_option('useAutomationExtension', False)

    if headless_flg:
        op.add_argument("--disable-gpu")
        op.add_argument("--disable-extensions")
        op.add_argument("--proxy-server='direct://'")
        op.add_argument("--proxy-bypass-list=*")
        op.add_argument("--start-maximized")
        op.add_argument("--headless")
        #driver = webdriver.Chrome(chrome_options=op)
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=op)
    return driver


def search_giftshop(driver, url, prefecture, industry):
    try:
        driver.get(url)

        # ドメインのURLを取得
        domain_url = '{uri.scheme}://{uri.netloc}/'.format(
            uri=urllib.parse.urlparse(url))

        # 結果データリスト
        searchOutputInfoList = []

        # データがなかった時ようのハイフン
        NO_DATA_STR = '-'

        # ターゲット出現を待機
        body_sel = "div.listbody"
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, body_sel))
        )
        soup = BeautifulSoup(driver.page_source, features="html.parser")

        # 検索結果を取得
        # 大きい文字の場合があるため、その値を取得
        ret_body_a1_list = []
        ret_body_sel1 = "div.listbody1 > a"
        ret_body_a1_list = soup.select(ret_body_sel1)
        for ret_body_a1 in ret_body_a1_list:

            # 初期値設定
            _searchOutputInfo = SearchOutputInfo()
            _searchOutputInfo.search_keyword = industry
            _searchOutputInfo.search_areaname = prefecture
            _searchOutputInfo.storename = NO_DATA_STR
            _searchOutputInfo.address = NO_DATA_STR
            _searchOutputInfo.tel_number = NO_DATA_STR
            _searchOutputInfo.web_url = NO_DATA_STR
            _searchOutputInfo.industry = NO_DATA_STR

            # 店舗名は先に設定
            store_name = ret_body_a1.text
            if store_name:
                _searchOutputInfo.storename = store_name

            href_text = ret_body_a1.get("href")
            detail_url = domain_url + "search/" + href_text

            # 個別ページに遷移
            driver.get(detail_url)

            # テーブルデータ取得
            table_sel = "div.d_block1_1"
            row_header_sel = "div.d_block1_t"
            row_data_sel = "div.d_block1_c"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, table_sel))
            )
            detail_soup = BeautifulSoup(
                driver.page_source, features="html.parser")
            table_ele = detail_soup.select(table_sel)[0]
            row_header_eles = table_ele.select(row_header_sel)
            index = 0
            for row_header_ele in row_header_eles:
                row_data_eles = []
                row_data = None
                if row_header_ele.text == "所在地":
                    row_data_eles = table_ele.select(row_data_sel)
                    row_data = row_data_eles[index]
                    if row_data.text:
                        _searchOutputInfo.address = row_data.text

                elif row_header_ele.text == "TEL":
                    row_data_eles = table_ele.select(row_data_sel)
                    row_data = row_data_eles[index]
                    if row_data.text:
                        tel_num = row_data.text.replace("-", "")
                        _searchOutputInfo.tel_number = tel_num

                elif row_header_ele.text == "WEB":
                    row_data_eles = table_ele.select(row_data_sel)
                    row_data = row_data_eles[index]
                    if row_data.text:
                        _searchOutputInfo.web_url = row_data.text

                index += 1

            searchOutputInfoList.append(_searchOutputInfo)

        # 小さい文字を取得
        ret_body_a2_list = []
        ret_body_sel2 = "div.listbody1_2 > a"
        ret_body_a2_list = soup.select(ret_body_sel2)
        for ret_body_a2 in ret_body_a2_list:

            # 初期値設定
            _searchOutputInfo = SearchOutputInfo()
            _searchOutputInfo.search_keyword = industry
            _searchOutputInfo.search_areaname = prefecture
            _searchOutputInfo.storename = NO_DATA_STR
            _searchOutputInfo.address = NO_DATA_STR
            _searchOutputInfo.tel_number = NO_DATA_STR
            _searchOutputInfo.web_url = NO_DATA_STR
            _searchOutputInfo.industry = NO_DATA_STR

            # 店舗名は先に設定
            store_name = ret_body_a2.text
            if store_name:
                _searchOutputInfo.storename = store_name

            href_text = ret_body_a2.get("href")
            detail_url = domain_url + "search/" + href_text

            # 個別ページに遷移
            driver.get(detail_url)

            # テーブルデータ取得
            table_sel = "div.d_block1_1"
            row_header_sel = "div.d_block1_t"
            row_data_sel = "div.d_block1_c"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, table_sel))
            )
            detail_soup = BeautifulSoup(
                driver.page_source, features="html.parser")
            table_ele = detail_soup.select(table_sel)[0]
            row_header_eles = table_ele.select(row_header_sel)
            index = 0
            for row_header_ele in row_header_eles:
                row_data_eles = []
                row_data = None
                if row_header_ele.text == "所在地":
                    row_data_eles = table_ele.select(row_data_sel)
                    row_data = row_data_eles[index]
                    if row_data.text:
                        _searchOutputInfo.address = row_data.text

                elif row_header_ele.text == "TEL":
                    row_data_eles = table_ele.select(row_data_sel)
                    row_data = row_data_eles[index]
                    if row_data.text:
                        tel_num = row_data.text.replace("-", "")
                        _searchOutputInfo.tel_number = tel_num

                elif row_header_ele.text == "WEB":
                    row_data_eles = table_ele.select(row_data_sel)
                    row_data = row_data_eles[index]
                    if row_data.text:
                        _searchOutputInfo.web_url = row_data.text

                index += 1

            searchOutputInfoList.append(_searchOutputInfo)

        return searchOutputInfoList

    except TimeoutException:
        logger.error("TimeoutExceptionが発生したため、次の検索に移ります")
        logger.error("ギフトショップ検索処理 検索県名：" + prefecture + "、キーワード：" + industry)
        return searchOutputInfoList


def search_navitime(driver, url, prefecture, industry):
    try:
        driver.get(url)

        # ドメインのURLを取得
        domain_url = '{uri.scheme}://{uri.netloc}/'.format(
            uri=urllib.parse.urlparse(url))

        # 結果データリスト
        searchOutputInfoList = []

        # データがなかった時ようのハイフン
        NO_DATA_STR = '-'

        page_index = 1

        # 次ページが押せなくなるまで繰り返す
        while True:

            # ターゲット出現を待機
            store_sel = "div#spot_area"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, store_sel))
            )
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            store_eles = soup.select(store_sel)

            if not len(store_eles):
                return searchOutputInfoList

            detail_sel = "li.spot_detail"
            storename_sel = "a.candidate_link"
            address_sel = "dd.address_name"
            tel_num_sel = "div.phone_area"
            category_sel = "div.spot_category_name"
            detail_eles = store_eles[0].select(detail_sel)

            for detail_ele in detail_eles:
                # 初期値設定
                _searchOutputInfo = SearchOutputInfo()
                _searchOutputInfo.search_keyword = industry
                _searchOutputInfo.search_areaname = prefecture
                _searchOutputInfo.storename = NO_DATA_STR
                _searchOutputInfo.address = NO_DATA_STR
                _searchOutputInfo.tel_number = NO_DATA_STR
                _searchOutputInfo.web_url = NO_DATA_STR
                _searchOutputInfo.industry = NO_DATA_STR

                # 店舗名
                store_name_ele = []
                store_name_ele = detail_ele.select(storename_sel)
                if len(store_name_ele):
                    _searchOutputInfo.storename = store_name_ele[0].text

                # 住所
                address_ele = []
                address_ele = detail_ele.select(address_sel)
                if len(address_ele):
                    # [地図]部分を削除
                    _searchOutputInfo.address = address_ele[0].text.replace(
                        '[地図]', '')

                # 電話番号
                tel_num_ele = []
                tel_num_ele = detail_ele.select(tel_num_sel)
                if len(tel_num_ele):
                    tel_num = tel_num_ele[0].text.replace("-", "")
                    _searchOutputInfo.tel_number = tel_num

                # カテゴリ
                category_ele = []
                category_ele = detail_ele.select(category_sel)
                if len(category_ele):
                    category_text = category_ele[0].text.replace('<', '')
                    category_text = category_text.replace('>', '')
                    _searchOutputInfo.industry = category_text

                searchOutputInfoList.append(_searchOutputInfo)

            # 次へボタン確認
            page_ul_sel = "ul.col.pages"
            page_ul_ele = soup.select(page_ul_sel)
            if not len(page_ul_ele):
                break

            a_eles = page_ul_ele[0].select("a")
            if not len(a_eles):
                break

            if a_eles[-1].text == "次へ":
                # 次のページへ
                page_param = "&p=" + str(page_index)
                next_page_url = url + page_param
                driver.get(next_page_url)
                page_index += 1
                continue

            break

        return searchOutputInfoList

    except TimeoutException:
        logger.error("TimeoutExceptionが発生したため、次の検索に移ります")
        logger.error("NAVITIME検索処理 検索県名：" + prefecture + "、キーワード：" + industry)
        return searchOutputInfoList


def search_mapion(driver, url, prefecture, industry):
    try:
        driver.get(url)

        # ドメインのURLを取得
        domain_url = '{uri.scheme}://{uri.netloc}/'.format(
            uri=urllib.parse.urlparse(url))

        # 結果データリスト
        searchOutputInfoList = []

        # データがなかった時ようのハイフン
        NO_DATA_STR = '-'

        page_index = 1

        # 次ページが押せなくなるまで繰り返す
        while True:

            # ターゲット出現を待機
            header_sel = "header"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, header_sel))
            )
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            data_sel = "dd.numberTxt"
            data_eles = soup.select(data_sel)

            if not len(data_eles):
                return searchOutputInfoList

            title_sel = "dt.title"
            dd_sel = "dd"

            for data_ele in data_eles:
                # 初期値設定
                _searchOutputInfo = SearchOutputInfo()
                _searchOutputInfo.search_keyword = industry
                _searchOutputInfo.search_areaname = prefecture
                _searchOutputInfo.storename = NO_DATA_STR
                _searchOutputInfo.address = NO_DATA_STR
                _searchOutputInfo.tel_number = NO_DATA_STR
                _searchOutputInfo.web_url = NO_DATA_STR
                _searchOutputInfo.industry = NO_DATA_STR

                # 店舗名
                store_name_ele = []
                store_name_ele = data_ele.select(title_sel)
                if len(store_name_ele):
                    _searchOutputInfo.storename = store_name_ele[0].text.strip(
                    )

                pattern = re.compile(r'[\(]{0,1}[0-9]{2,4}[\)\-\(]')

                dd_eles = data_ele.select(dd_sel)
                for dd_ele in dd_eles:
                    text = dd_ele.text.strip()
                    if "最寄り駅：" in text:
                        pass
                    elif prefecture in text:
                        _searchOutputInfo.address = text
                    elif pattern.findall(text):
                        tel_number = text.replace("-", "")
                        _searchOutputInfo.tel_number = tel_number.strip()

                searchOutputInfoList.append(_searchOutputInfo)

            # 次へボタン確認
            next_page_sel = "a#m_nextpage_link"
            next_page_ele = soup.select(next_page_sel)
            if not len(next_page_ele):
                break

            # 次のページへ
            page_index += 1
            page_param = "p=" + str(page_index)
            next_page_url = url + page_param
            driver.get(next_page_url)
            continue

        return searchOutputInfoList

    except TimeoutException:
        logger.error("TimeoutExceptionが発生したため、次の検索に移ります")
        logger.error("MAPION検索処理 検索県名：" + prefecture + "、キーワード：" + industry)
        return searchOutputInfoList


def search_jouhouya(driver, url, prefecture, industry):
    try:
        driver.get(url)

        # ドメインのURLを取得
        domain_url = '{uri.scheme}://{uri.netloc}/'.format(
            uri=urllib.parse.urlparse(url))

        # 結果データリスト
        searchOutputInfoList = []

        # データがなかった時ようのハイフン
        NO_DATA_STR = '-'

        page_index = 0

        # ターゲット出現を待機
        a_sel = "li.li_box > a"
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, a_sel))
        )
        soup = BeautifulSoup(driver.page_source, features="html.parser")

        a_eles = soup.select(a_sel)

        if not len(a_eles):
            return searchOutputInfoList

        for a_ele in a_eles:
            if a_ele.text == prefecture:
                prefecture_href = a_ele.get("href")

        if not prefecture_href:
            return searchOutputInfoList

        # 都道府県のぺージへ遷移
        prefecture_url = url + prefecture_href
        driver.get(prefecture_url)

        search_name = "q"
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, search_name))
        )

        # キーワード検索
        input_form = driver.find_elements_by_name(search_name)[0]
        input_form.send_keys(industry)
        input_form.send_keys(Keys.ENTER)

        # 次ページが押せなくなるまで繰り返す
        while True:
            time.sleep(2.5)

            content_main_sel = "div#content-main"
            a_sel = "dl.li_box > dt > a"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, content_main_sel))
            )
            search_soup = BeautifulSoup(
                driver.page_source, features="html.parser")
            content_main_eles = search_soup.select(content_main_sel)

            if not len(content_main_eles):
                return searchOutputInfoList

            a_eles = content_main_eles[0].select(a_sel)

            if not len(a_eles):
                return searchOutputInfoList

            detail_href_list = []
            for a_ele in a_eles:
                href = a_ele.get("href")
                detail_href_list.append(href)

            top_sel = "div#topFreeArea"
            display_name_sel = "td.form_display_name"
            display_value_sel = "div.display_value"
            zipcode_sel = "span.display_zipcode"
            address_sel = "span.display_address"
            for detail_href in detail_href_list:
                # 初期値設定
                _searchOutputInfo = SearchOutputInfo()
                _searchOutputInfo.search_keyword = industry
                _searchOutputInfo.search_areaname = prefecture
                _searchOutputInfo.storename = NO_DATA_STR
                _searchOutputInfo.address = NO_DATA_STR
                _searchOutputInfo.tel_number = NO_DATA_STR
                _searchOutputInfo.web_url = NO_DATA_STR
                _searchOutputInfo.industry = NO_DATA_STR

                # 詳細ページに遷移
                detail_url = url + detail_href
                driver.get(detail_url)
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, top_sel))
                )
                detail_soup = BeautifulSoup(
                    driver.page_source, features="html.parser")
                top_content = detail_soup.select(top_sel)

                if not top_content:
                    return searchOutputInfoList

                tr_list = top_content[0].select("tr")

                for tr in tr_list:
                    if not tr.select(display_name_sel):
                        continue

                    name = tr.select(display_name_sel)[0].text
                    if name == "名称":
                        store_name = tr.select(display_value_sel)[0].text
                        _searchOutputInfo.storename = store_name
                        continue

                    if name == "住所":
                        zip_code_eles = tr.select(zipcode_sel)
                        if len(zip_code_eles) > 0:
                            zip_code = zip_code_eles[0].text
                        address_eles = tr.select(address_sel)
                        if len(address_eles) > 0:
                            address = address_eles[0].text
                        _searchOutputInfo.postal_code = zip_code.replace(
                            "〒", "")
                        _searchOutputInfo.address = address
                        continue

                    if name == "ＴＥＬ":
                        tel_number = tr.select(display_value_sel)[0].text
                        _searchOutputInfo.tel_number = tel_number.replace(
                            "-", "")
                        continue

                searchOutputInfoList.append(_searchOutputInfo)

            # 次へボタン確認
            next_page_sel = "a.inactive"
            next_page_ele = search_soup.select(next_page_sel)
            if not len(next_page_ele):
                break

            # 次のページへ
            page_index += 1
            key_param = "?q=" + industry
            page_param = "&p=" + str(page_index)
            next_page_url = prefecture_url + key_param + page_param
            driver.get(next_page_url)
            continue

        return searchOutputInfoList

    except TimeoutException:
        logger.error("TimeoutExceptionが発生したため、次の検索に移ります")
        logger.error("街の情報屋さん検索処理 検索県名：" + prefecture + "、キーワード：" + industry)
        return searchOutputInfoList


def search_odekake(driver, url, prefecture, industry):
    try:
        # ドメインのURLを取得
        domain_url = '{uri.scheme}://{uri.netloc}/'.format(
            uri=urllib.parse.urlparse(url))

        # 結果データリスト
        searchOutputInfoList = []

        # データがなかった時ようのハイフン
        NO_DATA_STR = '-'

        page_index = 0

        targrt_url = url + 'page/' + prefecture + '/' + industry + '.html'
        driver.get(targrt_url)

        # 404のケースチェック
        h1_sel = 'h1'
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, h1_sel))
        )
        tmp_soup = BeautifulSoup(driver.page_source, features="html.parser")
        h1_eles = tmp_soup.select(h1_sel)
        for h1_ele in h1_eles:
            if '404 File not found' in h1_ele.text:
                logger.info('検索結果が見つかりませんでした。検索条件：' +
                            prefecture + ' ' + industry)
                return searchOutputInfoList

        # 次ページが押せなくなるまで繰り返す
        while True:
            li_sel = "ul > li"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, li_sel))
            )
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            li_eles = soup.select(li_sel)

            if not len(li_eles):
                return searchOutputInfoList

            for li_ele in li_eles:
                li_text = li_ele.text

                if not industry in li_text:
                    continue

                # 初期値設定
                _searchOutputInfo = SearchOutputInfo()
                _searchOutputInfo.search_keyword = industry
                _searchOutputInfo.search_areaname = prefecture
                _searchOutputInfo.storename = NO_DATA_STR
                _searchOutputInfo.address = NO_DATA_STR
                _searchOutputInfo.tel_number = NO_DATA_STR
                _searchOutputInfo.web_url = NO_DATA_STR
                _searchOutputInfo.industry = NO_DATA_STR

                item_list = []
                item_list = li_text.split('\n')
                _searchOutputInfo.storename = item_list[0]
                client_info_list = item_list[1].split('\u3000')
                if len(client_info_list) > 0:
                    postalcode_text = client_info_list[0].replace('〒', '')
                    _searchOutputInfo.postal_code = postalcode_text
                if len(client_info_list) > 1:
                    _searchOutputInfo.address = client_info_list[1]
                if len(client_info_list) > 2:
                    tel_number_text = client_info_list[2].replace('TEL', '')
                    tel_number_text = tel_number_text.replace('-', '')
                    _searchOutputInfo.tel_number = tel_number_text.strip()

                _searchOutputInfo.industry = industry

                searchOutputInfoList.append(_searchOutputInfo)

            # 次へボタン確認
            pagenation_sel = "div#main > a"
            pagenation_eles = soup.select(pagenation_sel)
            if not len(pagenation_eles):
                break

            next_page_url = ''

            for pagenation_ele in pagenation_eles:
                page_text = pagenation_ele.text
                if '次のページ' in page_text:
                    next_page_url = pagenation_ele.get("href")

            # 次のページへ
            if not next_page_url:
                break

            driver.get(next_page_url)
            continue

        return searchOutputInfoList

    except TimeoutException:
        logger.error("TimeoutExceptionが発生したため、次の検索に移ります")
        logger.error("おでかけタウン情報検索処理 検索県名：" + prefecture + "、キーワード：" + industry)
        return searchOutputInfoList


def search_hotflog(driver, url, prefecture, industry):
    try:

        # 結果データリスト
        searchOutputInfoList = []

        driver.get(url)

        # ドメインのURLを取得
        domain_url = '{uri.scheme}://{uri.netloc}/'.format(
            uri=urllib.parse.urlparse(url))

        # データがなかった時ようのハイフン
        NO_DATA_STR = '-'

        page_index = 1

        # 次ページが押せなくなるまで繰り返す
        while True:

            # ターゲット出現を待機
            div_sel = "div.hf-box-wrap"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, div_sel))
            )
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            div_eles = soup.select(div_sel)

            if not len(div_eles):
                return searchOutputInfoList

            tel_text_sel = 'div.w-100 > a > strong'
            storename_sel = 'h3 > a > strong'
            address_sel = 'span.small'
            website_sel = 'small > span > a'

            for div_ele in div_eles:

                # 初期値設定
                _searchOutputInfo = SearchOutputInfo()
                _searchOutputInfo.search_keyword = industry
                _searchOutputInfo.search_areaname = prefecture
                _searchOutputInfo.storename = NO_DATA_STR
                _searchOutputInfo.address = NO_DATA_STR
                _searchOutputInfo.tel_number = NO_DATA_STR
                _searchOutputInfo.web_url = NO_DATA_STR
                _searchOutputInfo.industry = NO_DATA_STR

                text_eles = div_ele.select(tel_text_sel)
                if len(text_eles):
                    _searchOutputInfo.tel_number = text_eles[0].text.strip().replace(
                        '-', '')

                storename_eles = div_ele.select(storename_sel)
                if len(storename_eles):
                    _searchOutputInfo.storename = storename_eles[0].text.strip(
                    )

                address_eles = div_ele.select(address_sel)
                if len(address_eles) >= 2:
                    address_text = address_eles[1].text.strip()
                    address_list = []
                    address_list = address_text.split(',')
                    # 郵便番号
                    postal_code_pattern = r"\d{3}-\d{4}"
                    postal_code_rx = re.compile(postal_code_pattern)

                    if len(address_list) == 3:
                        postalcode_str = address_list[-1].strip()
                        postal_code_mo = postal_code_rx.search(postalcode_str)
                        if postal_code_mo:
                            _searchOutputInfo.postal_code = postal_code_mo.group()
                        _searchOutputInfo.address = address_list[0].strip()
                    elif len(address_list) == 4:
                        postalcode_str = address_list[-1].strip()
                        postal_code_mo = postal_code_rx.search(postalcode_str)
                        if postal_code_mo:
                            _searchOutputInfo.postal_code = postal_code_mo.group()
                        _searchOutputInfo.address = address_list[2].strip(
                        ) + address_list[1].strip() + address_list[0].strip()

                website_eles = div_ele.select(website_sel)
                for website_ele in website_eles:
                    if website_ele.text.strip() == 'ウェブサイト':
                        website_href = website_ele.get('href')
                        _searchOutputInfo.web_url = website_href

                searchOutputInfoList.append(_searchOutputInfo)

            # 次へボタン確認
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, window.maxScrollY, 0);")
            time.sleep(1.0)
            driver.execute_script("window.scrollTo(0, window.minScrollY, 0);")
            time.sleep(1.0)
            driver.execute_script("window.scrollTo(0, window.maxScrollY, 0);")
            next_page_sel = "a.page-link"
            next_page_eles = soup.select(next_page_sel)
            if not len(next_page_eles):
                break

            next_flg = False
            for next_page_ele in next_page_eles:
                if next_page_ele.text.strip() == '次のページ':
                    next_flg = True
                    break

            if next_flg:
                # 次のページへ
                page_index += 1
                next_page_url = url + '/' + str(page_index)
                driver.get(next_page_url)
                continue
            else:
                break

        return searchOutputInfoList

    except TimeoutException:
        logger.error("TimeoutExceptionが発生したため、次の検索に移ります")
        logger.error("Hotflog検索処理 検索県名：" + prefecture + "、キーワード：" + industry)
        return searchOutputInfoList
