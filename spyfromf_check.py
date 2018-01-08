import os
import os.path

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

_config = {}

# 該当拡張子のコンフィグファイルを読み込む（仕様により名無しファイル（拡張子だけ）は読まない）
def load_secret_config():
  config_ext = ['.config', '.config_secret']  #コンフィグファイル用拡張子一覧

  for filename in os.listdir():
    # 拡張子から該当ファイルがコンフィグファイルであるか判別
    if os.path.splitext(filename)[1] in config_ext:
      file = open(filename, 'r')
      lines = file.readlines()
      for line in lines:
        token = line.split()
        if len(token) == 0 : continue #空白列
        if token[0][0] == '#' : continue  #コメント
        if len(token) == 2:
          _config[token[0]] = token[1]
        else:
          print("Can't read config [" + token[0] + "] . Be sure format is correct.")

load_secret_config()

def check_connection():
  #初期化、接続
  r = requests.get("https://spyfromf.nc2.co")
  return r.status_code

def check_login():
  driver = webdriver.Chrome()
  driver.get("https://spyfromf.nc2.co/auth/twitter")

  #login_button = driver.find_elements_by_xpath("/html/body/div/div/a")[0]
  #login_button.click()

  driver.find_element_by_id('username_or_email').send_keys(_config["twitter_account"])
  driver.find_element_by_id('password').send_keys(_config["twitter_pswd"])
  driver.find_element_by_id('allow').click()

  driver.get("https://spyfromf.nc2.co")

  username = driver.find_elements_by_xpath("/html/body/div/div/div[1]/div[1]/div/p[1]/a")[0]
  result = "成功" if username.text == "@" + _config["twitter_account"] else "ログイン後表示の異常"
 
  driver.quit()
  return result