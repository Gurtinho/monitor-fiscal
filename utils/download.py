import discord
import requests
import io
import zipfile

def realizar_download(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        return res.content if res.status_code == 200 else None
    except:
        return None

def zipar(documentos, choice):
    # Criando ZIP em memória
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        count = 0
        for i in documentos:
            if count == 5:
                break
            content = realizar_download(i['url'])
            if content:
                nome_pdf = f"{i['texto'][:50]}.pdf".replace("/", "-")
                zip_file.writestr(nome_pdf, content)
            count += 1
    
    zip_buffer.seek(0)
    file = discord.File(fp=zip_buffer, filename=f"DocumentosFiscais_{choice}.zip")
    return file