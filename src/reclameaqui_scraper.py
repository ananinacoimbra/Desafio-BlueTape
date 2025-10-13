from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from bs4 import BeautifulSoup
import time
#EDGE_DRIVER_PATH = r"C:\caminho\para\seu\msedgedriver.exe"

class ReclameAquiScraper:
    def __init__ (self):
        edge_options=webdriver.EdgeOptions()
        self.driver=webdriver.Edge(options=edge_options)

        self.base_url = "https://www.reclameaqui.com.br" 
        self.wait = WebDriverWait(self.driver, 15) 
        self.results = [] 
        print("Driver do Microsoft Edge inicializado.")

    def open_site(self):
        print(f"Abrindo o site: {self.base_url}")
        self.driver.get(self.base_url)
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
            print("Página principal do Reclame Aqui carregada.")
        except:
            print("Tempo esgotado ao esperar pela página.")

    def close(self):
        if self.driver:
            self.driver.quit()
            print("Navegador fechado.")

  #  def get_company_lists(self):



if __name__ == '__main__':
        scraper = None
        try:
            scraper = ReclameAquiScraper()
            scraper.open_site()

            time.sleep(5)

        except Exception as e:
            print("Erro na execução: {e}")
        finally:
            if scraper:
                scraper.close()

