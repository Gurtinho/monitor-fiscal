def dividir_texto(texto, limite=1800):
    chunks = []
    while len(texto) > 0:
        if len(texto) <= limite:
            chunks.append(texto)
            break
        
        # Pega os primeiros 1800 caracteres
        fatia = texto[:limite]
        
        # Tenta quebrar em um Título (assumindo que use # ou similar) ou quebra de linha
        ponto_de_quebra = fatia.rfind('\n#') # Procura último título
        if ponto_de_quebra == -1:
            ponto_de_quebra = fatia.rfind('\n\n') # Se não tem título, tenta parágrafo
        if ponto_de_quebra == -1:
            ponto_de_quebra = fatia.rfind(' ') # Se não tem parágrafo, tenta espaço
        if ponto_de_quebra == -1:
            ponto_de_quebra = limite # Se nada der certo, corta no limite mesmo

        chunks.append(texto[:ponto_de_quebra])
        texto = texto[ponto_de_quebra:].lstrip() # Remove espaços em branco do início do próximo chunk
    return chunks