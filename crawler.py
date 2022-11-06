from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

def extract_info(info, city):
    lines = info.text.split("\n")
    
    if city == "PA":
        if lines[0]:
            ID = lines[0].split(" ")[0]
            point = lines[0].split("[")[1].split(" ")[0]
        else:
            ID = ""
            point = ""
        if lines[2]:
            state = lines[2].split(": ")[1]
        else:
            state = ""
        if lines[3]:
            date = lines[3].split(": ")[1]
        else:
            date = ""
            
        return [ID, point, state, date]
    else:
        if lines[0]:
            ID = lines[0].split(" ")[0]
            point = lines[0].split("[")[1].split(" ")[0]
        else:
            ID = ""
            point = ""
        if lines[1]:
            state = lines[1].split(": ")[1]
        else:
            state = ""
        if lines[2]:
            date = lines[2].split(": ")[1]
        else:
            date = ""
    
        return [ID, point, state, date]

def crawler():
    options = Options()

    # 设置无窗口
    # options.add_argument('--headless')

    # 声明浏览器对象
    # 如果chromedriver在系统环境变量中, 那么其实executable_path可以不用显示指定
    chrome_driver = webdriver.Chrome(chrome_options=options)

    wait = WebDriverWait(chrome_driver, 10)
    # 访问页面
    chrome_driver.get('http://invader.spotter.free.fr/choixville.php')

    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/table/tbody/tr/td[3]/a[7]'))).click()
    # max_page = int(wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/p[5]/a[last()]'))).text)
    max_page = 1

    infos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'haut')))

    city = "VRS"
    dick = {"ID":[], "Point":[], "State":[], "Source_date":[]}

    for info in infos:
        print(info.text)
        ID, Point, State, Date = extract_info(info, city)
        dick["ID"].append(ID)
        dick["Point"].append(Point)
        dick["State"].append(State)
        dick["Source_date"].append(Date)


    for i in range(1, max_page):        
        xpath = f"/html/body/div[2]/div/p[5]/a[{i}]"
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        
        infos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'haut')))
        for info in infos:
            print(info.text)
            ID, Point, State, Date = extract_info(info, city)
            dick["ID"].append(ID)
            dick["Point"].append(Point)
            dick["State"].append(State)
            dick["Source_date"].append(Date)

    chrome_driver.close()

    for v in dick.values():
        print(len(v))
    df = pd.DataFrame.from_dict(dick)
    df['ID'] = df['ID'].apply(lambda x: 'VRS_' + x.split('_')[1].zfill(4))
    df.to_csv("versailles.csv", index=False)

    