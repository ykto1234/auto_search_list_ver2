import os
import glob
from os.path import join

class SearchInputInfo:
    def __init__(self):
        self.industry = None
        self.area = None
        self.prefecture = None
        self.target_industry_str = None
        self.target_industry_list = []
        self.exclusion_genre = None
        self.genre = []
        self.municipality_list = []

    def setFromExcelRow(self, item_row):
        self.industry = str(item_row[0])
        self.area = str(item_row[1])
        self.prefecture = str(item_row[2])
        self.target_industry_list = str(item_row[3]).split(",")


class SearchOutputInfo:
    def __init__(self):
        self.search_keyword = None
        self.search_areaname = None
        self.storename = None
        self.industry = None
        self.postal_code = None
        self.address = None
        self.tel_number = None
        self.web_url = None

    def __eq__(self, other):
        if not isinstance(other, SearchOutputInfo):
            return False
        return self.storename == other.storename

    def __hash__(self):
        return hash(self.storename)


class ExcelList:
    def __init__(self):
        self.out_file_path = None
        self.sheet_name = None