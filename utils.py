import unicodedata


def remover_acentos(texto):
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(
        [char for char in texto_normalizado if not unicodedata.combining(char)]
    )
