import unicodedata
import csv


def remover_acentos(texto):
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(
        [char for char in texto_normalizado if not unicodedata.combining(char)]
    )


def write_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Cabeçalho do CSV
        writer.writerow(
            ["Moeda Origem", "Moeda Destino", "Valor Compra", "Valor Venda"]
        )
        # Agrupa a cada 4 elementos
        for i in range(0, len(data), 4):
            writer.writerow(data[i : i + 4])
    print(f"Arquivo {filename} gerados com sucesso!")
