from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

def extract_info(info):
    lines = info.text.split("\n")
    if lines[0]:
        ID = lines[0].split(" ")[0]
        point = lines[0].split("[")[1].split(" ")[0]
    else:
        ID = ""
        point = ""
    if lines[0]:
        District = lines[1][1:-1]
    else:
        District = ""
    if lines[2]:
        state = lines[2].split(": ")[1]
    else:
        state = ""
    if lines[3]:
        date = lines[3].split(": ")[1]
    else:
        date = ""
    
    return [ID, point, District, state, date]

options = Options()

# 设置无窗口
# options.add_argument('--headless')

# 声明浏览器对象
# 如果chromedriver在系统环境变量中, 那么其实executable_path可以不用显示指定
driver = webdriver.Chrome(chrome_options=options)

wait = WebDriverWait(driver, 10)
# 访问页面
driver.get('http://invader.spotter.free.fr/choixville.php')

time.sleep(1)
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/table/tbody/tr/td[3]/a[1]'))).click()
max_page = int(wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/p[5]/a[last()]'))).text)

infos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'haut')))

dic = {"ID":[], "point":[], "District":[], "Last state":[], "Source_date":[]}

for info in infos:
    ID, point, District, state, date = extract_info(info)
    dic["ID"].append(ID)
    dic["point"].append(point)
    dic["District"].append(District)
    dic["Last state"].append(state)
    dic["Source_date"].append(date)

for i in range(1, max_page):        
    xpath = f"/html/body/div[2]/div/p[5]/a[{i}]"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    
    infos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'haut')))
    for info in infos:
        print(info.text)
        # ID, point, District, state, date = extract_info(info)
        # dic["ID"].append(ID)
        # dic["point"].append(point)
        # dic["District"].append(District)
        # dic["Last state"].append(state)
        # dic["Source_date"].append(date)

driver.close()

df = pd.DataFrame.from_dict(dic)
# df.to_csv("data.csv", index=False)

    