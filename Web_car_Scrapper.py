# Importe das bibliotecas 

import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

#=================================================================

# Configurações do Selenium
# Caaso mude de web-drive sera necessario auterar essa região
# Recomendo utlixar o firefox por motivos de bypass de aspectos de sehurança
options = Options()
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0")
driver = webdriver.Firefox(options=options)

#======================================================================

url = '---------------------------------'  
pesquisa = 'chevrolet classic'  # Substitua com a pesquisa desejada
driver.get(url) # Abra a página da web com o Selenium
#========================================================================

# Realize a pesquisa
driver.find_element(By.XPATH, '/html/body/header/div/div[2]/form/input').send_keys(pesquisa)
driver.find_element(By.XPATH, '/html/body/header/div/div[2]/form/button').click()
#===============================================================================================

# Lidar com pop-up de confirmação de cookies, se presente
# takvez receba atualização nesse trecho por que o ML não  tranalha mais com esse tipo de pop-up de curso
try:
    cookie_popup = driver.find_element(By.XPATH, '//div[@class="cookie-modal__content"]')
    accept_cookie_button = cookie_popup.find_element(By.XPATH, '//button[contains(text(), "Aceitar todos")]')
    accept_cookie_button.click()
except Exception as e:
    print("Nenhum pop-up de confirmação de cookies encontrado ou já aceito.")

#====================================================================

# Função para extrair links da página atual
# Ele ta fazendo um find na class que determina o bloco da div e pegando os link com padrão "JM#position"
def extrair_links_pagina(driver):
    elements_ol = driver.find_elements(By.TAG_NAME, "ol")
    links = set()
    for ol_element in elements_ol:
        link_elements = ol_element.find_elements(By.TAG_NAME, "a")
        for link_element in link_elements:
            link = link_element.get_attribute("href")
            if link and "JM#position" in link:
                links.add(link)
    return links
#======================================================================

# Função para fazer o download de imagens .webp
def download_imagens_webp(link, link_dir):
    driver.get(link)
    time.sleep(15)  # Aguarde o carregamento da página
    try:
        # Encontre todas as imagens com extensão .webp na página
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for img_tag in soup.find_all('img', src=True):
            img_src = img_tag['src']
            if img_src.endswith('.webp'):
                img_url = img_src
                img_name = os.path.basename(img_url)
                img_path = os.path.join(link_dir, img_name)
                response = requests.get(img_url)
                with open(img_path, 'wb') as f:
                    f.write(response.content)
    except Exception as e:
        print(f"Erro ao fazer o download das imagens da página {link}: {str(e)}")

#==================================================================================================

# Loop para percorrer as páginas de resultados e coletar informações
# coleta do campo de caracteristicas e arquiva dentro do diretorio em um arquivo chamdo "caracteristicas.txt"
# coleta do campo de descrição e arquiva dentro do diretorio em um arquivo chamdo "descricao.txt"
while True:
    # Extrair links da página atual
    links_pagina_atual = extrair_links_pagina(driver)

    for link in links_pagina_atual:
        # Crie um diretório com base no nome do link
        link_dir = link.replace("https://", "").replace("http://", "").replace("/", "_")
        os.makedirs(link_dir, exist_ok=True)

        # Download de imagens .webp
        download_imagens_webp(link, link_dir)

        # Encontre o elemento com o ID "highlighted_specs_attrs"
        highlighted_specs_element = driver.find_element(By.ID, "highlighted_specs_attrs")

        # Obtenha o texto do elemento
        highlighted_specs_text = highlighted_specs_element.text

        # Escreva as informações no arquivo dentro do diretório
        caracteristicas_filename = os.path.join(link_dir, "caracteristicas.txt")
        with open(caracteristicas_filename, "w", encoding="utf-8") as caracteristicas_file:
            caracteristicas_file.write(f"Informações da página: {link}\n")
            caracteristicas_file.write(highlighted_specs_text + "\n\n")

        print(f"Informações da página {link} foram salvas em {caracteristicas_filename}.")

        # Encontre o elemento com a classe "ui-pdp-description"
        description_element = driver.find_element(By.CLASS_NAME, "ui-pdp-description")

        # Obtenha o texto do elemento
        description_text = description_element.text

        # Escreva as informações no arquivo dentro do diretório
        descricao_filename = os.path.join(link_dir, "descricao.txt")
        with open(descricao_filename, "w", encoding="utf-8") as descricao_file:
            descricao_file.write(f"Descrição da página: {link}\n")
            descricao_file.write(description_text + "\n\n")

        print(f"Descrição da página {link} foi salva em {descricao_filename}.")

    try:
        # Encontre e clique no link "Próxima página" (ou qualquer elemento que você use para navegar para a próxima página)
        proxima_pagina_element = driver.find_element(By.CLASS_NAME, "ui-pagination__next")
        proxima_pagina_element.click()

        # Aguarde alguns segundos para que a próxima página seja carregada completamente (ajuste conforme necessário)
        time.sleep(5)
    except Exception as e:
        print("Não foi possível encontrar a próxima página. O programa será encerrado.")
        break

# Feche o navegador do Selenium
driver.quit()
