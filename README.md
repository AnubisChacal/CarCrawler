# 🚗🔍 CarCrawler

CarCrawler é uma ferramenta automatizada desenvolvida em Python que utiliza Selenium e BeautifulSoup para coletar informações detalhadas sobre carros de sites de venda. O projeto é capaz de realizar buscas, extrair links relevantes, baixar imagens dos veículos, e salvar as características e descrições dos carros em arquivos de texto organizados por diretórios.

## 🛠️ Funcionalidades

- **Busca automatizada**: Realiza buscas por termos específicos, como o modelo do carro, em sites de venda.
- **Extração de links**: Coleta todos os links relevantes dos resultados de busca para posterior processamento.
- **Download de imagens**: Baixa automaticamente todas as imagens de veículos no formato `.webp`.
- **Armazenamento de informações**: Salva as características e descrições dos veículos em arquivos de texto, organizados em diretórios com base nos links.

## 📂 Estrutura do Projeto

- **`CarCrawler.py`**: Script principal que executa todo o processo de scraping e armazenamento de dados.
- **`/imagens`**: Diretório onde as imagens baixadas dos veículos são armazenadas.
- **`/informacoes`**: Diretório onde as informações dos veículos, como características e descrições, são armazenadas em arquivos `.txt`.

## 🚀 Como Usar

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/AnubisChacal/CarCrawler.git
    ```

2. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure o script**:
   - Substitua a variável `url` no script com o URL do site que você deseja scraper.
   - Ajuste a variável `pesquisa` para o termo que você deseja buscar (por exemplo, "chevrolet classic").

4. **Execute o script**:
    ```bash
    python CarCrawler.py
    ```

5. **Resultados**:
   - As imagens serão baixadas para o diretório correspondente, e as características e descrições dos veículos serão salvas em arquivos de texto.

## 🛠️ Requisitos

- **Python 3.x**
- **Selenium**
- **BeautifulSoup**
- **Requests**
- **Geckodriver** (para Firefox)

## 📝 Observações

- Este script foi desenvolvido para fins educacionais. Certifique-se de respeitar os termos de serviço dos sites ao utilizar web scrapers.
