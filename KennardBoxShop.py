import sys
import os
import json
import time
from xml.etree import ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
from multiprocessing import Process, Queue, Manager
import copy

dir_path = os.path.dirname(os.path.abspath(__file__))
browser = webdriver.Chrome(executable_path='%s' % os.path.join(dir_path, 'chromedriver.exe'))

url = 'https://m.kss.com.au/boxshop/'

browser.get(url)

e = browser.find_elements_by_class_name('boxshop-item-input')
print e