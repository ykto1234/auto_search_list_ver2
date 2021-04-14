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
import pyperclip
import settings
import mylogger

# ログの定義
logger = mylogger.setup_logger(__name__)


def scroll_down(driver, element):
    for index in range(0, 5):
        # ページの高さを取得
        height = driver.execute_script("return arguments[0].scrollHeight", element)
        driver.execute_script("arguments[0].scrollTo(0, " + str(height) + ");", element)
        time.sleep(1.0)


def search_google_map(driver, search_keyword, url):
    try:
        SEARCH_name = "q"
        SEARCH_BTN_sel = ".searchbox-searchbutton"

        driver.get(url)

        # ターゲット出現を待機
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, SEARCH_name))
        )
        # 検索を行う
        driver.find_elements_by_name(SEARCH_name)[0].send_keys(search_keyword)
        driver.find_elements_by_name(SEARCH_name)[0].send_keys(Keys.ENTER)

        # 結果データリスト
        searchOutputInfoList = []
        all_div_results = []

        # データがなかった時ようのハイフン
        NO_DATA_STR = '-'

        before_div_results = None

        # 次ページが押せなくなるまで繰り返す
        while True:
            # 1件しか検索結果がない場合、構成が異なるためここで処理
            Panel_sel = "div.widget-pane.widget-pane-visible"
            Img_sel = "button.section-hero-header-image-hero"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, Panel_sel))
            )
            count1_soup = BeautifulSoup(driver.page_source, features="html.parser")
            img_results = count1_soup.select(Img_sel)
            if len(img_results):
                # 1件取得用の処理
                # 初期値設定
                _searchOutputInfo = SearchOutputInfo()
                _searchOutputInfo.search_keyword = search_keyword
                _searchOutputInfo.search_areaname = search_keyword.split(" ")[1]
                _searchOutputInfo.storename = NO_DATA_STR
                _searchOutputInfo.industry = NO_DATA_STR
                _searchOutputInfo.address = NO_DATA_STR
                _searchOutputInfo.tel_number = NO_DATA_STR
                _searchOutputInfo.web_url = NO_DATA_STR

                # 値の取得
                if len(count1_soup.select("h1")):
                    _searchOutputInfo.storename = count1_soup.select("h1")[0].text.strip()

                if len(count1_soup.select("span.section-rating-term")):
                    _searchOutputInfo.industry = count1_soup.select("span.section-rating-term")[1].text

                if len(count1_soup.select("div.ugiz4pqJLAG__primary-text.gm2-body-2")):
                    address_info = count1_soup.select("div.ugiz4pqJLAG__primary-text.gm2-body-2")[0].text
                    if address_info:
                        address_list = address_info.split(" ")
                        # 郵便番号
                        postal_code_pattern = r"\d{3}-\d{4}"
                        postal_code_rx = re.compile(postal_code_pattern)
                        # 住所
                        address = ""
                        for address_str in address_list:
                            postal_code_mo =  postal_code_rx.search(address_str)
                            if postal_code_mo:
                                postal_code = postal_code_mo.group()
                            else:
                                address += address_str
                        _searchOutputInfo.address = address
                        _searchOutputInfo.postal_code = postal_code

                for detail_content in driver.find_elements_by_css_selector("button.ugiz4pqJLAG__button"):
                    aria_label = ""
                    if detail_content:
                        aria_label = detail_content.get_attribute("aria-label")
                    # 電話番号
                    if aria_label:
                        tel_pattern = r"\d{2,4}-\d{2,4}-\d{2,4}"
                        tel_number_rx = re.compile(tel_pattern)
                        tel_number_mo =  tel_number_rx.search(aria_label)
                        if tel_number_mo:
                            tel_number_text = tel_number_mo.group().replace('-', '')
                            _searchOutputInfo.tel_number = tel_number_text

                action_byn_sel = "button.section-action-chip-button"
                for action_button in driver.find_elements_by_css_selector(action_byn_sel):
                    action_button_aria_label = ""
                    if action_button:
                        action_button_aria_label = action_button.get_attribute("aria-label")
                    # ウェブサイト
                    if action_button_aria_label and "ウェブサイトをコピーします" in action_button_aria_label:
                        WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, action_byn_sel))
                        )
                        driver.execute_script("arguments[0].click();", action_button)
                        web_url = pyperclip.paste()
                        _searchOutputInfo.web_url = web_url
                        break

                searchOutputInfoList.append(_searchOutputInfo)
                return searchOutputInfoList

            # ターゲット出現を待機
            DivPanel_sel = "div.section-layout.section-scrollbox"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, DivPanel_sel))
            )
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            # 一致する検索結果がありません
            NotFound_sel = "div.section-no-result-title"
            not_found_eles = soup.select(NotFound_sel)
            if len(not_found_eles) > 0:
                break

            # 結果リストを取得する
            div_results = []
            DivResult_sel = "a.place-result-container-place-link"
            DivInfo_sel = "h1.section-hero-header-title-title"
            ButtonBack_sel = "button.section-back-to-list-button"
            NextBtn_xpath = '//*[@id="n7lv7yjyC35__section-pagination-button-next"]'

            # ターゲット出現を待機
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, DivResult_sel))
            )
            # ページ遷移が上手くできていないことがあるため、チェック処理を加える
            if before_div_results:
                before_a = before_div_results[-1]
                for tmp in range(0, 30):
                    soup = BeautifulSoup(driver.page_source, features="html.parser")
                    after_div_results = soup.select(DivResult_sel)
                    if after_div_results:
                        after_a = after_div_results[-1]
                        if before_a != after_a:
                            break

                    time.sleep(1.0)

            # スクロールを動かして最下部まで読み込ませる
            scroll_sel = 'div.section-scrollbox'
            scroll_ele = driver.find_elements_by_css_selector(scroll_sel)
            scroll_down(driver, scroll_ele[1])

            soup = BeautifulSoup(driver.page_source, features="html.parser")
            div_results = soup.select(DivResult_sel)

            # 検索結果一覧を保持しておく
            before_div_results = div_results
            all_div_results.extend(div_results)

            # 次のページボタンが押せるか確認
            NextBtn_sel = "section-pagination-button-next"
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, NextBtn_xpath))
            )
            main_soup = BeautifulSoup(driver.page_source, features="html.parser")
            btn_next_ele = []
            btn_next_disabled = None
            btn_next_ele = main_soup.find_all('button', id=re.compile(NextBtn_sel))
            btn_next_disabled = btn_next_ele[0].has_attr("disabled")
            if bool(btn_next_disabled):
                # 非活性の場合
                break
            else:
                # 活性の場合、次のページボタンを押下する
                next_btn_ele = driver.find_element_by_xpath(NextBtn_xpath)
                driver.execute_script("arguments[0].click();", next_btn_ele)
                time.sleep(1.0)


        for index in range(0, len(all_div_results)):

            detail_page_link = all_div_results[index].get('href')
            driver.get(detail_page_link)

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, DivInfo_sel))
            )
            detail_soup = BeautifulSoup(driver.page_source, features="html.parser")

            # 初期値設定
            _searchOutputInfo = SearchOutputInfo()
            _searchOutputInfo.search_keyword = search_keyword
            _searchOutputInfo.search_areaname = search_keyword.split(" ")[1]
            _searchOutputInfo.storename = NO_DATA_STR
            _searchOutputInfo.industry = NO_DATA_STR
            _searchOutputInfo.address = NO_DATA_STR
            _searchOutputInfo.tel_number = NO_DATA_STR
            _searchOutputInfo.web_url = NO_DATA_STR

            # 値の設定
            if len(detail_soup.select("h1")):
                _searchOutputInfo.storename = detail_soup.select("h1")[0].text.strip()

            if len(detail_soup.select("div.ugiz4pqJLAG__primary-text.gm2-body-2")):
                address_info = detail_soup.select("div.ugiz4pqJLAG__primary-text.gm2-body-2")[0].text
                if address_info:
                    address_list = address_info.split(" ")
                    # 郵便番号
                    postal_code_pattern = r"\d{3}-\d{4}"
                    postal_code_rx = re.compile(postal_code_pattern)
                    # 住所
                    address = ""
                    for address_str in address_list:
                        postal_code_mo =  postal_code_rx.search(address_str)
                        if postal_code_mo:
                            postal_code = postal_code_mo.group()
                        else:
                            address += address_str
                    _searchOutputInfo.address = address
                    _searchOutputInfo.postal_code = postal_code

            for indeustry_content in driver.find_elements_by_xpath('//button[@jsaction="pane.rating.category"]'):
                _searchOutputInfo.industry = indeustry_content.text

            for detail_content in driver.find_elements_by_css_selector("button.ugiz4pqJLAG__button"):
                aria_label = ""
                if detail_content:
                    aria_label = detail_content.get_attribute("aria-label")
                # 電話番号
                if aria_label:
                    tel_pattern = r"\d{2,4}-\d{2,4}-\d{2,4}"
                    tel_number_rx = re.compile(tel_pattern)
                    tel_number_mo =  tel_number_rx.search(aria_label)
                    if tel_number_mo:
                        tel_number_text = tel_number_mo.group().replace('-', '')
                        _searchOutputInfo.tel_number = tel_number_text

            action_byn_sel = "button.section-action-chip-button"
            for action_button in driver.find_elements_by_css_selector(action_byn_sel):
                action_button_aria_label = ""
                if action_button:
                    action_button_aria_label = action_button.get_attribute("aria-label")
                # ウェブサイト
                if action_button_aria_label and "ウェブサイトをコピーします" in action_button_aria_label:
                    WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, action_byn_sel))
                    )
                    action_button.click()
                    web_url = pyperclip.paste()
                    _searchOutputInfo.web_url = web_url
                    break

            searchOutputInfoList.append(_searchOutputInfo)

            continue

        return searchOutputInfoList

    except TimeoutException:
        logger.error("TimeoutExceptionが発生したため、次の検索に移ります")
        logger.error("Googleマップ検索処理 検索キーワード：" + search_keyword)
        return searchOutputInfoList

    return searchOutputInfoList


def search_goo_map(driver, search_keyword, url):
    try:
        search_url = url + "/search/q/" + search_keyword

        driver.get(search_url)

        # 結果データリスト
        searchOutputInfoList = []

        # データがなかった時ようのハイフン
        NO_DATA_STR = '-'

        # ページ番号
        page_number = 1

        # 次ページが押せなくなるまで繰り返す
        while True:

            # ターゲット出現を待機
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located
            )
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            # 検索結果0件の場合
            NotFound_sel = "div.no_results"
            not_found_eles = soup.select(NotFound_sel)
            if len(not_found_eles) > 0:
                break

            # 次のページボタンが押せるか確認
            next_page_flg = False
            NextBtn_sel = "a.button--search-pager"
            btn_next_ele = []
            btn_next_ele = soup.select(NextBtn_sel)
            if len(btn_next_ele):
                # 存在する場合
                next_page_flg = True
                page_number += 1

            # 結果リストを取得する
            div_results = []
            div_sel = "div.search-card"
            div_results = soup.select(div_sel)

            for div_result in div_results:
                # 個別ページに遷移
                href_text = div_result.find("a").get("href")
                driver.get(url + href_text)

                h3_sel = "h3.head__text"

                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, h3_sel))
                )
                tmp_soup = BeautifulSoup(driver.page_source, features="html.parser")

                h3_list = tmp_soup.select(h3_sel)
                target_idx = 0
                for h3 in h3_list:
                    if h3.text == "基本情報":
                        break
                    target_idx += 1

                DivBody_sel = "div.l-sub-section__body"
                li_sel = "li.spot-table__item"
                team_sel = "div.team"
                description_sel = "div.description"

                basic_info = tmp_soup.select(DivBody_sel)[target_idx]
                basic_info_list = basic_info.select(li_sel)

                # 初期値設定
                _searchOutputInfo = SearchOutputInfo()
                _searchOutputInfo.search_keyword = search_keyword
                _searchOutputInfo.search_areaname = search_keyword.split(" ")[1]
                _searchOutputInfo.storename = NO_DATA_STR
                _searchOutputInfo.address = NO_DATA_STR
                _searchOutputInfo.tel_number = NO_DATA_STR
                _searchOutputInfo.web_url = NO_DATA_STR
                _searchOutputInfo.industry = NO_DATA_STR

                for basic_info_li in basic_info_list:
                    team_text = basic_info_li.select(team_sel)[0].text

                    if team_text == "お店/施設名":
                        _searchOutputInfo.storename = basic_info_li.select(description_sel + " > p")[0].text.strip()
                        continue

                    if team_text == "住所":
                        _searchOutputInfo.address = basic_info_li.select(description_sel + " > p")[0].text.strip()
                        continue

                    if team_text == "公式HP":
                        _searchOutputInfo.web_url = basic_info_li.select(description_sel + " > a")[0].text.strip()
                        continue

                    if team_text == "ジャンル":
                        a_list = []
                        a_text_list = []
                        a_list = basic_info_li.select(description_sel + " > a")
                        for a_text in a_list:
                            a_text_list.append(a_text.text)
                        _searchOutputInfo.genre = a_text_list
                        _searchOutputInfo.industry = ("/").join(a_text_list)
                        continue

                    if team_text == "お問い合わせ電話番号":
                        # 電話番号アンカークリック
                        a_tel_sel = "a#tel_pagelink"
                        div_tel_sel = "div.modal-tel__number"
                        tel_num_btn = driver.find_elements_by_css_selector(a_tel_sel)
                        if len(tel_num_btn):
                            tel_num_btn[0].click()
                            # 電話番号取得
                            WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, div_tel_sel))
                            )
                            tel_number_text = driver.find_elements_by_css_selector(div_tel_sel)[0].text.strip()
                            tel_number_text = tel_number_text.replace('-', '')
                            _searchOutputInfo.tel_number = tel_number_text
                        continue

                searchOutputInfoList.append(_searchOutputInfo)

            if next_page_flg:
                # 次へボタンが存在する場合、次のページに遷移する
                driver.get(search_url + "/page/" + str(page_number))
            else:
                # 存在しない場合
                break

    except TimeoutException:
        logger.error("TimeoutExceptionが発生したため、次の検索に移ります")
        logger.error("goo地図検索処理 検索キーワード：" + search_keyword)
        return searchOutputInfoList

    return searchOutputInfoList
