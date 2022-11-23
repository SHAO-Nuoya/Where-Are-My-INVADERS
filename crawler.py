from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from tqdm import tqdm

options = Options()

# 设置无窗口
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.get('http://invader.spotter.free.fr/listing.php')

wait = WebDriverWait(driver, 10)

max_page = int(wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/p[2]/a[last()]'))).text)

infos = list(map(lambda x:x.text, wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'haut')))))

for page in tqdm(range(1, max_page)):
    wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[2]/div/p[2]/a[{page}]'))).click()
    current_infos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'haut')))
    current_infos = list(map(lambda x:x.text, current_infos))
    infos.extend(current_infos)

driver.close()

invaders = []

for info in tqdm(infos):
    lines = info.split('\n')
    ID, Point, _= lines[0].split(' ')
    Point = Point[1:]
    State = lines[2].split(': ')[1]
    if lines[3].strip():
        Source_date = lines[3].split(': ')[1]
    else:
        Source_date = ''
    invader = [ID, Point, State, Source_date]
    invaders.append(invader)

df = pd.DataFrame(invaders, columns = ['ID', 'Point', 'State', 'Source_date'])
df['ID'] = df['ID'].apply(lambda x:x.split('_')[0] + '_' + x.split('_')[1].zfill(4))
df.to_csv('data/info.csv', index=False, sep=';')
