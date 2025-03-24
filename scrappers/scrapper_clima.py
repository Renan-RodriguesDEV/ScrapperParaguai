from utils import remover_acentos
from scrapper import Scrapper
import pandas as pd


class Clima(Scrapper):
    def __init__(self):
        self.BASE_CLIMA_URL = "https://www.meteored.com.py/"
        super().__init__()

    def get_clima(self, cidade="Pedro Juan Caballero", principais=False):

        # removendo acentuação
        cidade = remover_acentos(cidade).title()

        self.page.goto(self.BASE_CLIMA_URL)

        # carrega a pagina
        self.page.wait_for_load_state("load")
        # preenche o campo de pesquisa
        input_text = self.page.query_selector("input#search_pc")
        input_text.click()
        input_text.fill(cidade)
        try:
            self.page.wait_for_selector(".bnom-txt")
        except Exception as e:
            pass
        encontrou = False
        for city in self.page.query_selector_all(".bnom-txt"):
            if city.text_content().lower() == cidade.lower():
                city.click()
                encontrou = True
                break
        if not encontrou:
            input_text.press("Enter")

        # carrega os dados
        self.page.wait_for_selector(".grid-container-7")
        clima = self.page.query_selector(".temp")
        pd.DataFrame({"Cidade": [cidade], "Clima": [clima.text_content()]}).to_csv(
            "clima.csv", index=False
        )

        if principais:
            principais_cidades = self.get_all_links_clima()
            pd.DataFrame(principais_cidades).to_csv(
                "principais_cidades.csv", index=False
            )
            for c in principais_cidades["citys"]:
                print(c)
            print("_" * 100)
            print("CSV salvo com sucesso!!")
            print("_" * 100)
        print("_" * 100)
        print("Busca finalizada com sucesso!!")
        print("_" * 100)

    def get_all_links_clima(self):
        self.page.goto(self.BASE_CLIMA_URL)
        self.page.wait_for_load_state("load")
        city_links = [
            city.get_attribute("href") for city in self.page.query_selector_all("a.row")
        ]
        city_text = [
            city.text_content()
            for city in self.page.query_selector_all("li.li-card.mini-card")
        ]
        return {"links": city_links, "citys": city_text}


if __name__ == "__main__":
    clima = Clima()
    while True:
        cidade = input('Digite sua cidade ou "sair" para fechar:').lower()
        principais = input("Deseja ver as principais cidades? (s/n): ").lower()
        if cidade.lower() == "sair":
            break
        if principais not in ["s", "n"]:
            print("Opção inválida")
            continue
        clima.get_clima(cidade, True if principais == "s" else False)
