import time
import json
import xml.etree.ElementTree
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_root_text(html_str):
    root = xml.etree.ElementTree.fromstring(html_str)
    ret = [root.text] + [child.tail for child in root]
    ret = [e for e in ret if e]
    return ''.join(ret)

print("ChromeDriverInstall")
chrome_service = service.Service(service=ChromeService(ChromeDriverManager().install()))
options = Options()
options.add_argument('--headless')
driver : webdriver = webdriver.Chrome(service=chrome_service, options=options)

print("開始")
driver.get("https://west2-univ.jp/sp/menu.php?t=650111")
kinds = driver.find_elements(By.CLASS_NAME, "toggleTitle")
kinds.pop(0)

print("メニュー展開")
for kind in kinds:
    kind.click()
    time.sleep(0.5)
html = driver.page_source.encode('utf-8')

print("html取得")
bsObj = BeautifulSoup(html, "html.parser")
names = bsObj.find_all('p', {'class' : 'toggleTitle'})
catMenus = bsObj.find_all('div', {'class': 'catMenu'})
dict = {}
for catMenu in catMenus:
    lis = catMenu.find_all('li')
    sub_dict = {}
    for li in lis:
        menu = li.find('h3')
        meal = get_root_text(str(menu))
        price = menu.find('span', {'class': 'price'}).get_text()
        price = price[1:]
        sub_dict[meal] = int(price)
    dict[names[0].get_text().split("　")[0]] = sub_dict
    names.pop(0)

with open("./output/seikyo.json", mode="w", encoding="utf-8") as f:
    json.dump(dict, f, ensure_ascii=False, indent=4, separators=(',', ': '))
print("完了")

output = {}
json_open = open('seikyo.json', 'r')
seikyo_json = json.load(json_open)
for v in seikyo_json.values():
    if(len(v) != 0):
        i = random.choice(list(v.keys()))
        print(f"{i},{v[i]}")
        output[i] = v[i]


with open("./output/output.json", mode="w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4, separators=(',', ': '))