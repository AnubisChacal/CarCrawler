import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

#=================================================================================================
# Configurações do Selenium
options = Options()
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0")
driver = webdriver.Firefox(options=options)

# URL da página da web que você deseja analisar
url = 'https://www.mercadolivre.com.br/'  # Substitua com a URL real
pesquisa = 'chevrolet classic'  # Substitua com a pesquisa desejada

# Abra a página da web com o Selenium
driver.get(url)

# Realize a pesquisa
driver.find_element(By.XPATH, '/html/body/header/div/div[2]/form/input').send_keys(pesquisa)
driver.find_element(By.XPATH, '/html/body/header/div/div[2]/form/button').click()

#===================================================================================================

# Lidar com pop-up de confirmação de cookies, se presente
try:
    cookie_popup = driver.find_element(By.XPATH, '//div[@class="cookie-modal__content"]')
    accept_cookie_button = cookie_popup.find_element(By.XPATH, '//button[contains(text(), "Aceitar todos")]')
    accept_cookie_button.click()
except Exception as e:
    print("Nenhum pop-up de confirmação de cookies encontrado ou já aceito.")

#===================================================================================================

# Função para extrair links da página atual
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

#=============================================================================================================

# Função para fazer o download de imagens .webp
def download_imagens_webp(img_elements, img_directory):
    for img_element in img_elements:
        img_url = img_element.get("src")

        if img_url and img_url.endswith(".webp"):
            img_response = requests.get(img_url)

            if img_response.status_code == 200:
                img_filename = os.path.join(img_directory, os.path.basename(img_url))

                with open(img_filename, "wb") as img_file:
                    img_file.write(img_response.content)

                print(f"Imagem {img_url} foi baixada e salva como {img_filename}")
            else:
                print(f"Erro ao baixar a imagem {img_url}")

#============================================================================================================

# Loop para percorrer as páginas de resultados e coletar informações
while True:
    # Extrair links da página atual
    links_pagina_atual = extrair_links_pagina(driver)

    for link in links_pagina_atual:
        # Crie um diretório com base no nome do link
        link_dir = link.replace("https://", "").replace("http://", "").replace("/", "_")
        os.makedirs(link_dir, exist_ok=True)
        
        # Abra a página da web com o Selenium
        driver.get(link)

        # Aguarde alguns segundos para que a página seja carregada completamente (ajuste conforme necessário)
        time.sleep(15)

#==========================================================================================================

        try:


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
#========================================================================================================

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

#=====================================================================================================================

            # Encontre o elemento com o ID "gallery"
            gallery_element = driver.find_element(By.ID, "gallery")

            # Use o BeautifulSoup para analisar o HTML do elemento "gallery"
            soup = BeautifulSoup(gallery_element.get_attribute("innerHTML"), 'html.parser')

            # Encontre todas as tags <img> dentro do elemento "gallery"
            img_elements = soup.find_all("img")

            # Diretório onde as imagens serão salvas (dentro do diretório link_dir)
            img_directory = os.path.join(link_dir, "imagens")
            os.makedirs(img_directory, exist_ok=True)

            # Faça o download das imagens .webp
            download_imagens_webp(img_elements, img_directory)

        except Exception as e:
            print(f"Erro ao acessar o link ou recuperar informações: {link}")
#====================================================================================================================

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
