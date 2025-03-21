import time
import pandas as pd
from playwright.sync_api import sync_playwright, Page

from utils import remover_acentos

# variaveis de configuração
SITE_COTACAO = "http://ceteg.com.py/"
SITE_CLIMA = "https://www.meteored.com.py/tiempo-en_{}-{}-{}-{}--1-22839.html"
BASE_CLIMA_URL = "https://www.meteored.com.py/"


def get_cotacoes():
    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto(SITE_COTACAO)
        page.wait_for_load_state("load")
        if page.query_selector("div.modal-header"):
            page.query_selector(
                '//*[@id="myModal"]/div/div/div/div[1]/button/span'
            ).click()
        page.wait_for_selector("#tablero")
        cotacoes = [
            line.text_content()
            for line in page.query_selector_all("//*[@id='tablero']/tbody/tr[*]/td")
        ]
        arbitragens = [
            line.text_content()
            for line in page.query_selector_all(
                "//*[@id='tablero_arbitraje']/tbody/tr[*]/td"
            )
        ]
        print("Cotações")
        print("*" * 100)
        i = 0
        with open("cotacoes.txt", "w", encoding="utf-8") as f:
            linhas = ""
            for line in cotacoes:
                if i >= 4:
                    linhas += "\n"
                    print()
                    i = 0
                i += 1
                linhas += line + " "
                print(f"R$: {line}")
            f.write(linhas)
            print("cotacoes.txt salvo com sucesso!!")
        i = 0
        print("Arbritagens")
        print("*" * 100)
        with open("arbitragens.txt", "w", encoding="utf-8") as f:
            linhas = ""
            for line in arbitragens:
                if i >= 4:
                    linhas += "\n"
                    print()
                    i = 0
                i += 1
                linhas += line + " "
                print(f"R$: {line}")
            f.write(linhas)
            print("arbitragens.txt salvo com sucesso!!")


def get_clima(cidade="Pedro Juan Caballero", principais=False):
    with sync_playwright() as playwright:
        # removendo acentuação
        cidade = remover_acentos(cidade).title()

        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(BASE_CLIMA_URL)

        # carrega a pagina
        page.wait_for_load_state("load")
        # preenche o campo de pesquisa
        input_text = page.query_selector("input#search_pc")
        input_text.click()
        input_text.fill(cidade)
        try:
            page.wait_for_selector(".bnom-txt")
        except Exception as e:
            pass
        encontrou = False
        for city in page.query_selector_all(".bnom-txt"):
            if city.text_content().lower() == cidade.lower():
                city.click()
                encontrou = True
                break
        if not encontrou:
            input_text.press("Enter")

        # carrega os dados
        page.wait_for_selector(".grid-container-7")
        clima = page.query_selector(".temp")
        with open("clima.txt", "w", encoding="utf-8") as f:
            f.write(f"{cidade}\n{clima.text_content()}")
            print(clima.text_content())

        if principais:
            principais_cidades = get_all_links_clima(page)
            pd.DataFrame(principais_cidades).to_csv("principais_cidades.csv")
            for c in principais_cidades["citys"]:
                print(c)
            print("_" * 100)
            print("CSV salvo com sucesso!!")
            print("_" * 100)
    print("_" * 100)
    print("Busca finalizada com sucesso!!")
    print("_" * 100)


def get_all_links_clima(page: Page):
    page.goto(BASE_CLIMA_URL)
    page.wait_for_load_state("load")
    city_links = [
        city.get_attribute("href") for city in page.query_selector_all("a.row")
    ]
    city_text = [
        city.text_content() for city in page.query_selector_all("li.li-card.mini-card")
    ]
    return {"links": city_links, "citys": city_text}


get_cotacoes()
get_clima("Pedro Juan Caballero", True)
