from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup


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
    def get_empresa_lists(self):
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
                    slug_path = element.get_attribute('href')
                    companies_to_scrape.append({'Nome': nome_limpo, 'Tipo': 'Melhor', 'Slug_path': slug_path})

                #PIORES
                empresa_select_pior = 'li[data-testid="tab-worst"]'
                empresa_tab_pior = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, empresa_select_pior)))
                self.driver.execute_script("arguments[0].click();", empresa_tab_pior)

                time.sleep(2)

                empresa_elements_pior = self.driver.find_elements(By.CSS_SELECTOR, empresa_selector)

                for element in empresa_elements_pior [:3]:
                    nome_limpo = element.text.strip().splitlines()[1]
                    slug_path = element.get_attribute('href')
                    companies_to_scrape.append({'Nome': nome_limpo, 'Tipo': 'Pior', 'Slug_path': slug_path})
                        
                print(f"Empresas encontradas: {len (companies_to_scrape)}")
                print(f"Lista parcial: {companies_to_scrape}") 
                return companies_to_scrape
            
            except Exception as erro:
                print(f"Erro ao exibir as listas: {erro}")

        except Exception as err:
            print(f"Erro : {err}")
            return[]
       
#Extrai dados
    def extrai_data(self, empresa_data,  per_f = "últimos 6 meses é", per_label = "6 meses"):
        nome_empresa = empresa_data['Nome']

        slug_path = empresa_data['Slug_path']       
  
        data = empresa_data.copy()
        data ['Período'] = per_label     

        if slug_path.startswith('http'):
            empresa_URL = slug_path
        else:
            empresa_URL = self.base_url.rstrip('/') + slug_path
            
        self.driver.get(empresa_URL)
        data['URL'] = empresa_URL

        print(f"Extraindo dados da empresa: {nome_empresa}")

        teste_xpath_espera = f"//span[contains(text(), '{per_f}' ]/b"
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, teste_xpath_espera)))
        except:
            print(f"ERRO perfil {nome_empresa} não carrega")
            data['Nota Geral'] = "Pagina nao carregada"
            self.results.append(data)
            return
        html_conteudo = self.driver.page_source
        soup = BeautifulSoup(html_conteudo, 'html.parser')

        data_bs4 = {
        'Nota Geral': (lambda tag: tag.name == 'b' and tag.parent and per_f in tag.parent.text),
        'Reclamações respondidas (%)': (lambda tag: tag.name == 'strong' and 'Respondeu' in tag.parent.text),
        'Voltariam a fazer negócio (%)': (lambda tag: tag.name == 'strong' and 'Dos que avaliaram' in tag.parent.text),
        'Índice de solução (%)': (lambda tag: tag.name == 'strong' and 'A empresa resolveu' in tag.parent.text),
        'Nota do consumidor': (lambda tag: tag.name == 'strong' and 'Nota média' in tag.parent.text and tag.parent.find_all('strong')) 
        }

        for label, bs4_selector in data_bs4.items():
            try:
                elemento = soup.find(bs4_selector)
                if elemento:
                    valor_bruto = elemento.text.strip()
                    if label == 'Nota Geral' :
                        valor = valor_bruto.splitlines()[0]
                    else:
                        valor= valor_bruto.split(" ")[0]
                    data[label]= valor
                else:
                    data[label]= "N/A"
                    
            except Exception as e:
                data[label]= "N/A"

        self.results.append(data)
        print(f"Dados de {nome_empresa} extraidos com sucesso")

#troca de periodo
    def troca_periodo(self, periodo_nome):
        if periodo_nome =="6 meses":
            return True
    
        print("Alternando periodos")

        tab_xpath = f"//button[contains(text(), '{periodo_nome}')]"

        try:
            tab_elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))
            self.driver.execute_script("arguments[0].click();", tab_elemento)
            print(f"Alternado para {periodo_nome}")
            return True
        except:
            print(f"Aba {periodo_nome} não encontrada")
            return False


from ExportaData import ExportaData
if __name__ == '__main__':
        scraper = None
        exporter = ExportaData()
        try:
            scraper = ReclameAquiScraper()
            scraper.open_site()
            companies = scraper.get_empresa_lists()

            periodos = {
                "6 meses": "últimos 6 meses é", 
                "12 meses": "últimos 12 meses é",
                "2024": "2024 é",
                "2023": "2023 é",
                "Geral": "geral é"
            }

            for empresa_data in companies:
                for per_label, per_f in periodos.items():
                    if scraper.troca_periodo(per_label):
                        scraper.extrai_data(
                            empresa_data.copy(),
                            per_f=per_f,
                            per_label=per_label
                        )
            print("exportando para excel...")
            exporter.export_to_excel(scraper.results)


        except Exception as e:
            print(f"erro final {e}")
        finally:
            if scraper:
                scraper.close()

