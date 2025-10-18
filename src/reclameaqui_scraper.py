from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from bs4 import BeautifulSoup
from ExportaData import ExportaData
 


class ReclameAquiScraper:
    def __init__ (self):
        edge_options=webdriver.EdgeOptions()
        #edge_options.add_argument('--headless=new')
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument('--disable-blink-features=AutomationControlled')
        edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Edge(options=edge_options)

        #Abre navegador para edge
        self.base_url = "https://www.reclameaqui.com.br" 
        self.wait = WebDriverWait(self.driver, 6) 
        self.results = [] 
        self.empresa_salvar=[]
        
        print("Driver do Microsoft Edge inicializado")

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

#Extrai Lista de Casas de Aposta
    def get_empresa_lists(self):
        print("Buscando: 'Casa de aposta' ")
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
            print("Filtro de Categoria clicado")
            time.sleep(3)

            #slect casa de aposta
            aposta_option_xpath = "//button[@title='Casa de Aposta']" 
            aposta_element = self.wait.until(EC.presence_of_element_located((By.XPATH, aposta_option_xpath)))
            self.driver.execute_script("arguments[0].click();", aposta_element)

            print("Filtro 'Casa de Aposta' aplicado. \nAguardando listas...")
            time.sleep(3)

        #Extrai Empresas
            empresa_selector ='a[data-testid="listing-ranking"]'
                        
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, empresa_selector)))
            html_conteudo = self.driver.page_source
            soup = BeautifulSoup(html_conteudo, 'html.parser')
            
                #MELHORES
            empresa_elements_melhor = soup.select(empresa_selector)
            for element in empresa_elements_melhor [:3]:
                texto_completo = element.get_text(separator='\n', strip=True).splitlines()
                nome_limpo = texto_completo[1]
                slug_path = element.get('href')
                companies_to_scrape.append({'Nome': nome_limpo, 'Tipo': 'Melhor', 'Slug_path': slug_path})

                 #PIORES
            empresa_select_pior = 'li[data-testid="tab-worst"]'
            empresa_tab_pior = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, empresa_select_pior)))
            self.driver.execute_script("arguments[0].click();", empresa_tab_pior)

            time.sleep(2)
            html_conteudo_pior = self.driver.page_source
            soup_pior = BeautifulSoup(html_conteudo_pior, 'html.parser')
            empresa_elements_pior = soup_pior.select(empresa_selector)

            for element in empresa_elements_pior [:3]:
                texto_completo = element.get_text(separator='\n', strip=True).splitlines()
                nome_limpo = texto_completo[1]
                slug_path = element.get('href')
                companies_to_scrape.append({'Nome': nome_limpo, 'Tipo': 'Pior', 'Slug_path': slug_path})
                        
            print(f"Empresas encontradas: {len (companies_to_scrape)}")
            print(f"Lista parcial: {companies_to_scrape}") 
            return companies_to_scrape
             

        except Exception as err:
            print(f"Erro : {err}")
            return[]
    
    def reinicializar_driver(self):
        if hasattr(self, 'driver') and self.driver:
            self.close() 
            
        print("\nReinicializando o driver: nova raspagem! Aguarde...")
        
        
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument('--disable-blink-features=AutomationControlled')
        edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)

        try:
            self.driver = webdriver.Edge(options=edge_options)
            self.wait = WebDriverWait(self.driver, 6)
            print("Driver do Microsoft Edge REINICIALIZADO.")
            return True
        except Exception as e:
            print(f"ERRO CRÍTICO ao reinicializar o driver: {e}")
            return False
        
    def navegar_por_tabs (self, periodo_alvo):
        PERIODO_MAP = {
            "6 meses": "newPerformanceCard-tab-1",
            "12 meses": "newPerformanceCard-tab-2",
            "2024": "newPerformanceCard-tab-3",
            "2023": "newPerformanceCard-tab-4",
            "Geral": "newPerformanceCard-tab-5",
        }
        if periodo_alvo not in PERIODO_MAP:
            print("Periodo nao encontrado")
            return False

        id_periodo = PERIODO_MAP[periodo_alvo]

        try:

            qual_periodo = self.wait.until(EC.element_to_be_clickable((By.ID, id_periodo)))
            self.driver.execute_script("arguments[0].click();", qual_periodo)
            print(f"Periodo: {periodo_alvo}")
            time.sleep(2)
            return True
        
        except Exception as e:
            print(f"Nao foi possivel clicar em {periodo_alvo}")  
    

    def raspar_dados(self, html_pagina, nome_empresa):
        soup = BeautifulSoup(html_pagina, 'html.parser')
        dados_raspados = {'Empresa': nome_empresa}

        METRICAS = [
            'Nota', 'Reclamações respondidas', 'Voltariam a fazer negócio', 
            'Índice de solução', 'Nota do consumidor'
        ]
        for k in METRICAS:
            dados_raspados[k] = 'N/D'

        def extrair_proximo(frase_chave):
            tag = soup.find(text=lambda t: t and frase_chave.lower() in t.lower())
            if tag:
                parent = tag.find_parent()
                strong = parent.find('strong')
                if strong:
                    texto = strong.get_text(strip=True).replace(',', '.')
                    match = re.search(r'[\d,\.]+%?', texto)
                    return match.group(0) if match else texto
            return 'N/D'

        try:
            nota_geral = None

            possiveis_classes = [
                'sc-5z7mni-2',  
                'sc-1pe7b5t-2', 
                'rating',       
                'sc-gqPbQI',    
            ]
            for classe in possiveis_classes:
                tag = soup.find('div', class_=lambda c: c and classe in c)
                if tag and re.search(r'\d', tag.get_text()):
                    nota_geral = tag.get_text(strip=True)
                    break

            if not nota_geral:

                nota_tag = soup.find(text=re.compile(r'nota média', re.I))
                if nota_tag:
                    b_tag = nota_tag.find_parent().find('b')
                    if b_tag:
                        nota_geral = b_tag.get_text(strip=True)

            if nota_geral:
                nota_limpa = nota_geral.replace(',', '.').split('/')[0]
                dados_raspados['Nota'] = nota_limpa

            dados_raspados['Reclamações respondidas'] = extrair_proximo('Respondeu')
            dados_raspados['Voltariam a fazer negócio'] = extrair_proximo('Dos que avaliaram,')
            dados_raspados['Índice de solução'] = extrair_proximo('A empresa resolveu')

            nota_consumidor = None

            possiveis_textos = [
                'nota média dos consumidores',
                'nota do consumidor',
                'nota média avaliada pelos consumidores',
            ]

            for frase in possiveis_textos:
                tag = soup.find(text=lambda t: t and frase in t.lower())
                if tag:
                    
                    bloco = tag.find_parent()
                    if bloco:
                        
                        match = re.search(r'\d{1,2}[,.]\d{1}', bloco.get_text())
                        if match:
                            nota_consumidor = match.group(0)
                            break

            if not nota_consumidor:
                nota_tag = soup.find(string=re.compile(r'\d{1,2}[,.]\d{1}\s*/\s*10'))
                if nota_tag:
                    nota_consumidor = re.search(r'\d{1,2}[,.]\d{1}', nota_tag).group(0)

            if not nota_consumidor:
                possiveis_classes = ['sc-1pe7b5t-2', 'sc-5z7mni-2', 'rating']
                for classe in possiveis_classes:
                    div = soup.find('div', class_=lambda c: c and classe in c)
                    if div and re.search(r'\d', div.get_text()):
                        match = re.search(r'\d{1,2}[,.]\d{1}', div.get_text())
                        if match:
                            nota_consumidor = match.group(0)
                            break

            if nota_consumidor:
                dados_raspados['Nota do consumidor'] = nota_consumidor.replace(',', '.')


            print("\n--- DADOS RASPADOS PARA DEBUG ---")
            for chave, valor in dados_raspados.items():
                print(f"{chave}: {valor}")
            print("---------------------------------")

        except Exception as e:
            print(f"Erro na raspagem de dados para {nome_empresa}. Motivo: {e}")

        return dados_raspados


    def raspar_empresas(self, lista_empresas):
        PERIODOS_ALVO = ["6 meses", "12 meses", "2024", "2023", "Geral"]
        if not lista_empresas:
            print("Lista de empresas vazia. Nada para processar.")
            return

        for empresa in lista_empresas:
            nome_empresa = empresa['Nome']
            url_do_perfil = self.base_url + empresa['Slug_path'] 
            
            try: 
                if not self.reinicializar_driver():
                    print("Parando o processamento devido à falha crítica de inicialização do driver.")
                    break 
                
                time.sleep(2) 
                print(f"\n[INÍCIO DO PROCESSO] Empresa: {nome_empresa}")
                
                
                self.driver.get(url_do_perfil) 
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))


                for periodo_alvo in PERIODOS_ALVO:
                    
                    dados = None

                    try:
                        navegacao_sucedida = self.navegar_por_tabs(periodo_alvo) 
                        
                        if navegacao_sucedida:

                            html_pagina = self.driver.page_source
                            dados_raspadados = self.raspar_dados(html_pagina, nome_empresa)
                            

                            dados = dados_raspadados 

                    except Exception as e:
                        print(f"Falha de raspagem no período {periodo_alvo}: {e}")
                        
                    finally:
                        if dados is not None:
                            dados['Periodo'] = periodo_alvo 
                            dados['Tipo'] = empresa['Tipo']
                            dados['URL'] = url_do_perfil
                            self.results.append(dados) 
                        else:
                            self.results.append({
                                'Empresa': nome_empresa, 'Periodo': periodo_alvo, 
                                'Tipo': empresa['Tipo'], 'URL': url_do_perfil, 
                                'Nota': 'N/D', 'Reclamações respondidas': 'N/D', 'Voltariam a fazer negócio': 'N/D', 
                                'Índice de solução': 'N/D', 'Nota do consumidor': 'N/D'
                            })


            except Exception as e:
                print(f"Falha CRÍTICA (fora do loop) para processar: {nome_empresa}. Erro inesperado: {e}")
                
            finally:
                self.close() 

        print("\nProcessamento de todas as empresas concluído.")

    def salvar_em_excel(self):
        if not self.results:
            print("Lista vazia. Nada para salvar")
            return
        exportador = ExportaData()
        exportador.export_to_excel(self.results)

    def coordenar_raspagem(self):
            self.open_site()
            self.empresa_salvar = self.get_empresa_lists()
            self.close()

            if self.empresa_salvar:
                
                self.raspar_empresas(self.empresa_salvar) 

                self.salvar_em_excel()
            else:
                print("Nenhuma empresa para processar.")
                
            self.close() 


       
if __name__ == '__main__':

    print("INICIANDO RASPAGEM DE DADOS")
    print("Casas de Aposta - Reclame Aqui")
   
    scraper = ReclameAquiScraper()
        
    if scraper.driver:
        try:  
            scraper.coordenar_raspagem()
            print("\n PROCESSO FINALIZADO COM SUCESSO")

        except Exception as main_error:
            print(f" ERRO no main: {main_error}")
        finally:
            scraper.close()
            
    else:
        print("Não foi possível iniciar o scraper. Verifique a instalação do Edge e do WebDriver.")