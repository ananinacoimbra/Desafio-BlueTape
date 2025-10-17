def raspar_dados_perfil(self, html_pagina, nome_empresa):
    """
    Extrai a nota e os percentuais de estatísticas do perfil usando Beautiful Soup, 
    baseado nos textos-chave do XPath anterior.
    """
    soup = BeautifulSoup(html_pagina, 'html.parser')
    dados_raspadados = {'Empresa': nome_empresa}

    # --- Função auxiliar para buscar o valor baseado na frase-chave ---
    def _extrair_valor_por_texto(frase_chave, posicao_forte=0):
        # Localiza o elemento 'span' que contém a frase chave (texto do rótulo)
        span_com_frase = soup.find('span', text=lambda t: t and frase_chave in t)
        
        if span_com_frase:
            # O valor que queremos está dentro de uma tag <strong> próxima
            # O XPath anterior era: //span[contains(text(), 'Respondeu')]/strong
            
            # Tenta encontrar a tag <strong> que segue a frase
            strong_elements = span_com_frase.find_all('strong')
            
            if len(strong_elements) > posicao_forte:
                # O valor é o texto dentro dessa tag <strong> (ou o texto aninhado)
                valor_texto = strong_elements[posicao_forte].text.strip()
                # Retorna apenas o número/percentual (seu código splitlines()[0])
                return valor_texto.split(" ")[0]
        
        return 'N/D'

    try:
        
        nota_element = soup.find('p', class_=lambda x: x and 'score-component-default' in x)
        dados_raspadados['Nota'] = nota_element.text.strip() if nota_element else 'N/D'
        
        if dados_raspadados['Nota'] == 'N/D':
            # Tenta um seletor mais agressivo se a classe falhou
            nota_element_agressivo = soup.find('h2', class_=lambda x: x and 'score' in x)
            if nota_element_agressivo:
                 # Assume que a nota é o primeiro número grande da seção
                 dados_raspadados['Nota'] = nota_element_agressivo.text.strip().splitlines()[0] 
        
        # 2. Reclamações respondidas (Chave: 'Respondeu')
        dados_raspadados['Reclamações respondidas'] = _extrair_valor_por_texto('Respondeu', posicao_forte=0)

        # 3. Voltariam a fazer negócio (Chave: 'Dos que avaliaram')
        dados_raspadados['Voltariam a fazer negócio'] = _extrair_valor_por_texto('Dos que avaliaram', posicao_forte=0)
        
        # 4. Índice de solução (Chave: 'A empresa resolveu')
        dados_raspadados['Índice de solução'] = _extrair_valor_por_texto('A empresa resolveu', posicao_forte=0)
        
        # 5. Nota do consumidor (Chave: 'Há', e queremos o segundo <strong>, index 1)
        dados_raspadados['Nota do consumidor'] = _extrair_valor_por_texto('Há', posicao_forte=1)
        
        print(f"✅ Dados de '{nome_empresa}' raspados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro crítico no Beautiful Soup para {nome_empresa}. Motivo: {e}")
        # Se houver um erro, preenche com N/D
        dados_raspadados.update({
            k: 'N/D' for k in ['Nota', 'Reclamações respondidas', 'Voltariam a fazer negócio', 'Índice de solução', 'Nota do consumidor'] if k not in dados_raspadados
        })

    return dados_raspadados