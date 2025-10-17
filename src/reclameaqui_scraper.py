from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from ExportaData import ExportaData
import re 


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
    #Rapasr dados
   
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
        
    def processar_empresas(self, lista_empresas):

        if not lista_empresas:
            print("Lista de empresas vazia. Nada para processar.")
           
            self.close() 
            return
        
        for empresa in lista_empresas:
            nome_empresa = empresa['Nome']
            url_do_perfil = self.base_url + empresa['Slug_path'] 
            
            try:
                
                self.reinicializar_driver() 
             
                time.sleep(2) 
                
                print(f"\n[INÍCIO DO PROCESSO] Empresa: {nome_empresa}")
                self.driver.get(url_do_perfil)
                
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer"))) 
                
                html_pagina = self.driver.page_source
                dados = self.raspar_dados_perfil(html_pagina, nome_empresa)

                dados['Tipo'] = empresa['Tipo']
                dados['URL'] = url_do_perfil
                self.results.append(dados) 
                
            except Exception as e:
                
                print(f"ERRO para processar: {nome_empresa}. Erro: {e}")
            
            finally:
                self.close()
                
        print("\nProcessamento de todas as empresas concluído.")


    # def raspar_dados_perfil(self, html_pagina, nome_empresa):
           
    #         soup = BeautifulSoup(html_pagina, 'html.parser')
    #         dados_raspadados = {'Empresa': nome_empresa}

    #         def extrair_do_texto(exp_chave, strong_p = 0):
    #             span_da_frase = soup.find('span', text=lambda t:t and exp_chave in t)

    #             if span_da_frase:
    #                 strong_elements = span_da_frase.find_all('strong')
    #                 if len(strong_elements)> strong_p:
    #                     valor_texto = strong_elements[strong_p].text.strip()
    #                     return valor_texto.split(" ")[0]
                
    #             return 'N/A'
            
    #         try:
    #             nota_element = soup.find('p', class_=lambda x: x and 'score-component-default__text--large' in x)
    #             dados_raspadados['Nota'] = nota_element.text.strip() if nota_element else 'N/A'

    #             if dados_raspadados['Nota'] == 'N/A':
    #                 nota_element_push = soup.find('h2', class_= lambda x:x and 'score' in x )
    #                 if nota_element_push:
    #                     dados_raspadados['Nota'] = nota_element_push.text.strip().splitlines()[0]



    #             dados_raspadados['Reclamações respondidas'] = extrair_do_texto('Respondeu', strong_p=0)
    #             dados_raspadados['Voltariam a fazer negócio'] = extrair_do_texto('Dos que avaliaram', strong_p=0)
    #             dados_raspadados['Índice de solução'] = extrair_do_texto('A empresa resolveu', strong_p=0)
    #             dados_raspadados['Nota do consumidor'] = extrair_do_texto('Há', strong_p=0)
                
    #             print(f"Dados de '{nome_empresa}' raspados com sucesso!")
                
    #         except Exception as e:
    #             print(f"ERRO para raspagem {nome_empresa}: {e}")
    #             dados_raspadados.update({
    #                 k: 'N/A' for k in ['Nota', 'Reclamações respondidas', 'Voltariam a fazer negócio', 'Índice de solução', 'Nota do consumidor'] if k not in dados_raspadados
    #             })
                
    #         return dados_raspadados
   
    def raspar_dados_perfil(self, html_pagina, nome_empresa):
        """
        Tenta extrair as métricas usando Beautiful Soup. Usa a busca pelo título 
        (texto exato) e busca de valores vizinhos para maior robustez.
        """
        soup = BeautifulSoup(html_pagina, 'html.parser')
        dados_raspadados = {'Empresa': nome_empresa}

        METRICAS = [
            'Nota', 
            'Reclamações respondidas', 
            'Voltariam a fazer negócio', 
            'Índice de solução', 
            'Nota do consumidor'
        ]
        
        # Inicializa todos com N/D (ou 'N/A' se for o padrão de saída)
        for k in METRICAS:
            dados_raspadados[k] = 'N/D'

        try:
            # --- FUNÇÃO AUXILIAR DE BUSCA ---
            def _extrair_valor_vizinho(titulo_procurado):
                # 1. Encontra a tag que contém o título (o label, ex: 'Índice de solução')
                titulo_tag = soup.find('p', text=titulo_procurado)
                
                if titulo_tag:
                    # 2. O valor (percentual) é geralmente o irmão anterior
                    valor_tag = titulo_tag.find_previous_sibling()
                    
                    if valor_tag:
                        valor_limpo = valor_tag.get_text(strip=True).replace(',', '.')
                        # Tenta extrair apenas o número se houver mais texto
                        match = re.search(r'[\d,.]+%?', valor_limpo)
                        return match.group(0) if match else valor_limpo
                
                return 'N/D'

            # --- 1. NOTA GERAL ---
            # Tenta a classe mais genérica para o score grande
            nota_element = soup.find('p', class_=lambda x: x and 'score-component-default' in x and 'large' in x)
            if nota_element:
                dados_raspadados['Nota'] = nota_element.get_text(strip=True).replace(',', '.')
            
            # --- 2. PERCENTUAIS ---
            dados_raspadados['Reclamações respondidas'] = _extrair_valor_vizinho('Reclamações respondidas')
            dados_raspadados['Voltariam a fazer negócio'] = _extrair_valor_vizinho('Voltariam a fazer negócio')
            dados_raspadados['Índice de solução'] = _extrair_valor_vizinho('Índice de solução')
            
            # Tenta a Nota do Consumidor, que às vezes está em estrutura diferente
            dados_raspadados['Nota do consumidor'] = _extrair_valor_vizinho('Nota do consumidor')
            
            print(f"✅ Raspagem de dados finalizada para '{nome_empresa}'.")

        except Exception as e:
            print(f"❌ Erro crítico no Beautiful Soup para {nome_empresa}. Motivo: {e}")
            # Retorna N/D
            
        return dados_raspadados
    def processar_empresas(self, lista_empresas):
       
        if not lista_empresas:
                print("Lista de empresas vazia. Nada para processar.")
                return
        
        PERIODO_RA = "Geral"   

        for empresa in lista_empresas:
                nome_empresa = empresa['Nome']
                url_do_perfil = self.base_url + empresa['Slug_path'] 
                try: 
                    if not self.reinicializar_driver():
                        
                        print("Parando o processamento devido à falha crítica de inicialização do driver.")
                        break
                    
                    time.sleep(2) 
                    
                    print(f"\nFazendo raspagem da empresa: {nome_empresa}")

                    self.driver.get(url_do_perfil) 
                    #ajusta periodo
                    dados_tempo = {}
                    try:
                        xpath_periodo = f"//button[contains(text(), '{PERIODO_RA})] | //span[text()='{PERIODO_RA}']"
                        bot_periodo = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_periodo)))
                        bot_periodo.clear()
                        print(f"periodo ajustado para {PERIODO_RA}")
                        time.sleep(3)

                        dados_tempo['Periodo'] = PERIODO_RA
                    except Exception as err:
                        print(f"Aviso: Não foi possível clicar no período '{PERIODO_RA}'. Usando o padrão da página.")
                        dados_tempo['Periodo'] = "Padrão (Não Selecionado)"

                    self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer"))) 
                    
                    html_pagina = self.driver.page_source
                    dados = self.raspar_dados_perfil(html_pagina, nome_empresa)

                    dados['Tipo'] = empresa['Tipo']
                    dados['URL'] = url_do_perfil
                    self.results.append(dados) 
                    

                except Exception as e:
                    print(f"Falha para processar:  {nome_empresa}. Erro inesperado: {e}")
                
                finally:
                    self.close() 
                
    def encontra_html_empresa(self, url_slug_empresa):
        print("Corrige Seletores")
        try:
            if not self.reinicializar_driver():
                return

            url_completa = self.base_url + url_slug_empresa
            self.driver.get(url_completa)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
            
            # OBTÉM O HTML DA PÁGINA
            html_pagina = self.driver.page_source
            soup = BeautifulSoup(html_pagina, 'html.parser')
            
            # PROCURA PELO CONTAINER PRINCIPAL DAS ESTATÍSTICAS (Isto é a chave!)
            # Sugestão 1: Tenta a classe da seção principal de notas (pode precisar de ajuste manual!)
            container_stats = soup.find('div', class_=lambda x: x and 'ui-score-component' in x) 
            
            if not container_stats:
                # Sugestão 2: Tenta encontrar o container que tem a métrica 'Reclamações respondidas'
                titulo_tag = soup.find('p', text='Reclamações respondidas')
                if titulo_tag:
                    # Pega o elemento pai principal que contém o bloco de estatísticas
                    container_stats = titulo_tag.find_parent('div', class_=lambda x: x and 'styles_MetricsContainer' in x) # Ajuste de classe

            print(f"\n--- HTML DA SEÇÃO DE ESTATÍSTICAS PARA: {url_slug_empresa} ---")
            if container_stats:
                # Imprime o HTML formatado da seção de interesse
                print(container_stats.prettify())
                print("\n--- FIM DO HTML DE DIAGNÓSTICO ---")
            else:
                print("NÃO FOI POSSÍVEL ISOLAR A SEÇÃO DE MÉTRICAS. Tente outra classe/seletor.")
                
        except Exception as e:
            print(f"Erro durante o diagnóstico: {e}")
            
        finally:
            self.close()


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
                
                self.processar_empresas(self.empresa_salvar) 

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