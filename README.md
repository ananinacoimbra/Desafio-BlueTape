# Desafio Técnico BlueTape: Web Scraping de Estatísticas no Reclame Aqui

Aqui está o resultado do Desafio Técnico - BlueTape
Este projeto é um *Web Scraper* desenvolvido em Python para consultar e extrair métricas específicadas no desafio de empresas do filtro de "Casa de Aposta" no site Reclame Aqui. Ele utiliza a biblioteca **Selenium** para automação e navegação, **Beautiful Soup** para extração de dados, e **Pandas** para a exportação final em um arquivo Excel, com dados organizados por abas de período de tempo.

O projeto segue o Princípio da Responsabilidade Única (SRP)
utiliza uma estratégia de **Reinicialização de Driver por Empresa** para garantir a máxima estabilidade.

## Pré-requisitos

Para executar este projeto, você precisará ter o Python 3.x instalado e o navegador **Microsoft Edge** (escolhido pela autora).

1.  **Python 3.x**
2.  **Microsoft Edge** (O Edge WebDriver deve ser gerenciado automaticamente pelo Selenium, mas para evitar erros, beixe uma versão compativel com seu Microsoft Edge).

## Instalação e Configuração

### 1. Clonar o Repositório

Obtenha o código do projeto via `git clone`:

```bash
git clone [URL_DO_SEU_REPOSITÓRIO]
cd [NOME_DA_PASTA_DO_PROJETO]

```

### 2. Cria o ambiente virtual

Recomendado o uso de um ambiente virtual (venv):

```bash
python -m venv venv
# Ativa o ambiente virtual (Windows PowerShell / Git Bash)
source venv/Scripts/activate 
```

### 3. Instalar Dependências Python

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install selenium beautifulsoup4 pandas xlsxwriter
```

(Nota: xlsxwriter é essencial para o Pandas salvar os dados em múltiplas abas por período.)

## Execução do Projeto

O script é coordenado pelo método *coordenar_raspagem* e automatizará o browser para consultar estatísticas.

### 1. Preparação
Feche o Excel: Certifique-se de que o arquivo de destino (Dados_Exportatos-Casa_de_Aposta_BlueTape.xlsx) não esteja aberto para evitar o erro de permissão (Permission denied).

### 2. Rodar o Scraper
Execute o arquivo principal no terminal (com o ambiente virtual ativado):

```bash
python src/reclameaqui_scraper.py
```

### 3. Acompanhamento
Durante a execução:

    O navegador será aberto e fechado diversas vezes (uma nova sessão limpa para cada empresa)

    O progresso e os resultados (como notas e índices) serão exibidos diretamente no console para verificação

## Saída do Projeto

Ao final da execução, será gerado automaticamente um arquivo Excel na pasta raiz do projeto:

### Arquivo:
Dados_Exportados-Casa_de_Aposta_BlueTape.xlsx

### Estrutura do Arquivo:

5 abas separadas, correspondentes aos períodos:

    6 meses

    12 meses

    Geral

    2024

    2023

### Métricas Extraídas:

    Nota da empresa

    Reclamações respondidas (%)

    Voltariam a fazer negócio (%)

    Índice de solução (%)

    Nota do consumidor

### Estrutura de Pastas:
    Projeto-ReclameAqui/
    │
    ├─ src/
    │  ├─ reclameaqui_scraper.py
    │  └─ ExportaData.py
    │
    ├─ venv/ ----> Ambiente virtual
    ├─ Dados_Exportados-Casa_de_Aposta_BlueTape.xlsx ----> Resultado Final da exportação
    └─ README.md

## Observações Técnicas

    Implementa reinicialização do driver por empresa para evitar erros de sessão e sobrecarga de memória. Tambem evita que o bot caia numa pagina de validação.

    Segue boas práticas de engenharia de software e separação de responsabilidades, considerando primordial as noções de POO

    O código seria facilmente expansível para outros filtros e categorias do site

#### Desenvolvido por Ana Coimbra 💙
Desafio Técnico – BlueTape
Agradeço pela oportunidade de participar deste processo seletivo. Foi uma ótima experiência desenvolver este teste e conhecer mais sobre a empresa. Estou à disposição para esclarecimentos adicionais.
