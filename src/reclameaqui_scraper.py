from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from bs4 import BeautifulSoup
import time


class ReclameAquiScraper:
    def __init__ (self):
        edge_options=webdriver.EdgeOptions()
        self.driver=webdriver.Edge(options=edge_options)

#Abre navegador para edge
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

#Extrai Casas de Aposta
    def get_company_lists(self):
        print("Extraindo de: 'Casa de aposta' ")
        companies_to_scrape=[]

        try:
            poup_close_selector = "button[aria-label='fechar']"
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, poup_close_selector))).click()
            print("Pop-up fechado")
        except:
            pass
        try:
            time.sleep(2)   
            #filtro de categoria
            category_filter_xpath = "//label[contains(text(), 'Selecione uma categoria')]/following-sibling::div[1]"

            filter_element = self.wait.until(EC.presence_of_element_located((By.XPATH, category_filter_xpath)))
            self.driver.execute_script("arguments[0].click();", filter_element)
            print("Filtro de Categoria clicado via JavaScript.")

            time.sleep(3)

           # time.sleep(3)

            #slect casa de aposta
            aposta_option_xpath = "//button[@title='Casa de Aposta']" 
            aposta_element = self.wait.until(EC.presence_of_element_located((By.XPATH, aposta_option_xpath)))
            self.driver.execute_script("arguments[0].click();", aposta_element)

            print("'Filtro 'Casa de Aposta' aplicado. Aguardando listas")
            time.sleep(3)

        #Extrai Empresas
            #MELHORES
            empresa_selector ='a[data-testid="listing-ranking"]'
            
            try:
                
                self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, empresa_selector)))
                empresa_elements_melhor = self.driver.find_elements(By.CSS_SELECTOR, empresa_selector)

                
                for element in empresa_elements_melhor [:3]:
                    nome_limpo = element.text.strip().splitlines()[1]
                    companies_to_scrape.append({'Nome': nome_limpo, 'Tipo': 'Melhor'})

                #PIORES
                empresa_select_pior = 'li[data-testid="tab-worst"]'
                empresa_tab_pior = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, empresa_select_pior)))
                self.driver.execute_script("arguments[0].click();", empresa_tab_pior)

                time.sleep(2)

                empresa_elements_pior = self.driver.find_elements(By.CSS_SELECTOR, empresa_selector)

                for element in empresa_elements_pior [:3]:
                    nome_limpo = element.text.strip().splitlines()[1]
                    companies_to_scrape.append({'Nome': nome_limpo, 'Tipo': 'Pior'})
                        
                print(f"Empresas encontradas: {len (companies_to_scrape)}")
                print(f"Lista parcial: {companies_to_scrape}") 
                return companies_to_scrape
            
            except Exception as erro:
                print(f"Erro ao exibir as listas: {erro}")
        
        
        except Exception as err:
            print(f"Erro : {err}")
            return[]


if __name__ == '__main__':
        scraper = None
        try:
            scraper = ReclameAquiScraper()
            scraper.open_site()

            companies = scraper.get_company_lists()

            time.sleep(5)

        except Exception as e:
            print("Erro na execução: {e}")
        finally:
            if scraper:
                scraper.close()

