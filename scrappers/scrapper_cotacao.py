import time
from scrapper import Scrapper
from sender_email import send_email
from utils import write_csv


class Cotacao(Scrapper):

    def __init__(self):
        self.URL_COTACAO = "http://ceteg.com.py/"
        super().__init__()

    def get_cotacoes(self):

        self.page.goto(self.URL_COTACAO)
        self.page.wait_for_load_state("load")
        if self.page.query_selector("div.modal-header"):
            self.page.query_selector(
                '//*[@id="myModal"]/div/div/div/div[1]/button/span'
            ).click()
        self.page.wait_for_selector("#tablero")
        cotacoes = [
            line.text_content()
            for line in self.page.query_selector_all(
                "//*[@id='tablero']/tbody/tr[*]/td"
            )
        ]
        arbitragens = [
            line.text_content()
            for line in self.page.query_selector_all(
                "//*[@id='tablero_arbitraje']/tbody/tr[*]/td"
            )
        ]
        # cotacoes = map(lambda x: x.replace(",", "."), cotacoes)
        # arbitragens = map(lambda x: x.replace(",", "."), arbitragens)
        print("Cotações")
        print("*" * 100)
        write_csv(cotacoes, "cotacoes.csv")
        print("Arbritagens")
        write_csv(arbitragens, "arbitragens.csv")


if __name__ == "__main__":
    while True:
        with Cotacao() as cotacao:
            cotacao.get_cotacoes()
        send_email("Cotações", "Cotações do dia", "cotacoes.csv")
        time.sleep(60)
        print("Atualizando cotações...")
