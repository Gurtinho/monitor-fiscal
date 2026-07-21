import pytest
from utils.chunks import dividir_texto

# ─── Casos básicos ────────────────────────────────────────────────────────────

def test_texto_menor_que_limite_retorna_um_chunk():
    resultado = dividir_texto("texto curto")
    assert len(resultado) == 1
    assert resultado[0] == "texto curto"


def test_texto_vazio_retorna_lista_vazia():
    resultado = dividir_texto("")
    assert resultado == []


def test_texto_exatamente_no_limite_nao_divide():
    texto = "x" * 1800
    resultado = dividir_texto(texto)
    assert len(resultado) == 1


# ─── Divisão ──────────────────────────────────────────────────────────────────

def test_texto_maior_que_limite_gera_multiplos_chunks():
    texto = "x" * 4000
    resultado = dividir_texto(texto)
    assert len(resultado) > 1


def test_todos_os_chunks_tem_no_maximo_1800_chars():
    texto = "x" * 5000
    resultado = dividir_texto(texto, limite=1800)
    for chunk in resultado:
        assert len(chunk) <= 1800


def test_conteudo_nao_e_perdido_na_divisao():
    # A soma dos chunks deve ter o mesmo conteúdo do original
    texto = "palavra " * 500 # 4000 chars
    resultado = dividir_texto(texto)
    reconstruido = "".join(resultado)
    assert reconstruido.replace(" ", "") == texto.replace(" ", "")


# ─── Quebra inteligente no título ─────────────────────────────────────────────

def test_quebra_preferencial_no_titulo_markdown():
    # Monta um texto que tem um título depois de 1000 chars
    parte1 = "a" * 1000
    titulo = "\n# Seção Nova"
    parte2 = "b" * 1000

    texto = parte1 + titulo + parte2
    resultado = dividir_texto(texto, limite=1800)

    # O segundo chunk deve começar com o título
    assert resultado[1].startswith("# Seção Nova")


def test_sem_titulo_corta_no_limite():
    texto = "y" * 3000
    resultado = dividir_texto(texto, limite=1800)
    assert len(resultado[0]) == 1800


# ─── Parametrize: testando vários inputs de uma vez ───────────────────────────
#
# Em vez de repetir a mesma função N vezes, o @pytest.mark.parametrize
# roda o mesmo teste com cada conjunto de parâmetros.

@pytest.mark.parametrize("limite,esperado_chunks", [
    (100, 10), # limite pequeno → muitos chunks
    (500, 2), # limite médio → poucos chunks
    (2000, 1), # limite grande → um chunk só
])
def test_limite_customizado(limite, esperado_chunks):
    texto = "z" * 1000
    resultado = dividir_texto(texto, limite=limite)
    assert len(resultado) == esperado_chunks
