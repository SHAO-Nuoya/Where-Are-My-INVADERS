from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from tqdm import tqdm

class Crawler:
    def __init__(self, url:str='http://invader.spotter.free.fr/listing.php') -> None:
        options = Options()
        # 设置无窗口
        options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(url)

    def get_max_page(self):
        max_page = int(self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/p[2]/a[last()]'))).text)
        return max_page
    
    def crawler(self):
        infos = list(map(lambda x:x.text, self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'haut')))))
        max_page = self.get_max_page()
        
        for page in tqdm(range(1, max_page)):
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[2]/div/p[2]/a[{page}]'))).click()
            current_infos = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'haut')))
            current_infos = list(map(lambda x:x.text, current_infos))
            infos.extend(current_infos)

        self.driver.close()
        return infos

    def generate_info(self):
        invaders = []
        infos = self.crawler()
        
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

if __name__ == "__main__":
    Crawler().crawler()