from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
import re

import sys
import time

option = webdriver.ChromeOptions()

option.add_argument('disable-infobars')
option.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=option)
Max_Time_Out = 30
Time_Out = 10
Mini_Time_Out = 3
pass_score = "80"


class pass_six_units():
    def __init__(self):

        self.memberid = sys.argv[1]
        self.host = sys.argv[2]
        self.url = "https://{}.englishtown.com/services/api/school/_tools/SubmitScoreHelper.aspx".format(self.host)
        self.load_btn_id = "btnLoad"
        self.load_txt_id = "txtMemberId"
        self.score_txt_id = "txtUnitScore"
        self.score_btn_id = "btnUnitScore"
        self.level_txt_id = "txtLevelTestScore"
        self.level_btn_id = "btnLevelTestScore"

    def open_url(self):
        driver.set_page_load_timeout(Max_Time_Out)
        try:
            driver.get(self.url)
        except TimeoutError:
            print("cannot open the page for {} seconds".format(Max_Time_Out))
            driver.execute_script('window.stop()')

    def find_element(self, obj):
        WebDriverWait(driver, Time_Out).until(EC.visibility_of_element_located((By.ID, obj)))
        element = WebDriverWait(driver, Time_Out).until(lambda x: driver.find_element(By.ID, obj))
        return element

    def type(self, obj, value):
        self.find_element(obj).clear()
        self.find_element(obj).send_keys(value)

    def clickat(self, obj):
        WebDriverWait(driver, Time_Out).until(EC.element_to_be_clickable((By.ID, obj)))
        self.find_element(obj).click()

    def pass_6_units(self):

        self.type(self.load_txt_id, self.memberid)
        self.clickat(self.load_btn_id)

        units = self.find_element('dpUntiList')
        get_start_unit = Select(units)

        start_unit = re.search("\d", get_start_unit.first_selected_option.text).group()

        for i in range(int(start_unit), 7):
            self.type(self.score_txt_id, pass_score)
            self.clickat(self.score_btn_id)
            self.clickat(self.load_btn_id)
            driver.implicitly_wait(Time_Out)
            print("Save progress for unit {}".format(i))

    def pass_level_test(self):
        self.type(self.level_txt_id, pass_score)
        self.clickat(self.level_btn_id)
        print("pass unit test")


if __name__ == '__main__':
    p = pass_six_units()
    p.open_url()
    p.pass_6_units()
    p.pass_level_test()
    driver.implicitly_wait(Time_Out)
    driver.quit()
