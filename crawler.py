from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import urllib.request
import time
import pandas as pd
from tqdm import tqdm

class Crawler:
    def __init__(self, url:str="https://www.invader-spotter.art/cherche.php") -> None:
        # 设置无窗口
        self.driver = webdriver.Edge()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = url
        self.goToRightPage()

    def get_max_page(self):
        max_page = int(self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/p[2]/a[last()]"))).text)
        return max_page
    
    def goToRightPage(self):
        self.driver.get(self.url)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/form/p/input"))).click()
        
    def crawler(self):
        infos = list(map(lambda x:x.text, self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "haut")))))
        max_page = self.get_max_page()
        
        for page in tqdm(range(1, max_page)):
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[2]/div/p[2]/a[{page}]"))).click()
            current_infos = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "haut")))
            current_infos = list(map(lambda x:x.text, current_infos))
            infos.extend(current_infos)
        
        # unflashed_list = pd.read_csv('data/unflashed_invaders.csv', on_bad_lines='skip',delimiter=';')['ID'].values.tolist()
        # urls = []
        # for page in tqdm(range(39, 70)):
        #     self.wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[2]/div/p[2]/a[{page}]"))).click()
        #     current_urls =42 map(lambda x:x.get_attribute('src'), self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".haut [src]"))))
        #     current_urls = list(filter(lambda x:x[-4:]=='.jpg', current_urls))
        #     urls.extend(current_urls)
        self.driver.close()
        return infos

        # urls = [url for url in urls if any(str(unflashed) in url for unflashed in unflashed_list)]

        # for url in urls:
        #     urllib.request.urlretrieve(url, '/Users/ritsuritsu/Python/Invader in Paris/' + url.split('/')[-1])
        
        # return 

    def generate_info(self):
        invaders = []
        infos = self.crawler()
        
        for info in tqdm(infos):
            lines = info.split("\n")
            ID, Point, _= lines[0].split(" ")
            Point = Point[1:]
            State = lines[2].split(": ")[1]
            if lines[3].strip():
                Source_date = lines[3].split(": ")[1]
            else:
                Source_date = ""
            invader = [ID, Point, State, Source_date]
            invaders.append(invader)

        df = pd.DataFrame(invaders, columns = ["ID", "Point", "State", "Source_date"])
        df["ID"] = df["ID"].apply(lambda x:x.split("_")[0] + "_" + x.split("_")[1].zfill(4))
        df.to_csv("data/info.csv", index=False, sep=";")

if __name__ == "__main__":
    Crawler().crawler()