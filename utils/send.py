from datetime import datetime, timezone

import requests

from config import links

# ============================================================
# Envio de mensagem
# ============================================================
def enviar_discord(nome, novos_links):
    if not novos_links:
        return

    cor = 0x007BFF
    titulo = f"🚨 Novas Notas Técnicas em {nome}"
    descricao = "\n".join([ f"🔗 [{x['texto']}]({x['url']})\n\n" for x in novos_links ])

    payload = {
        "embeds": [
            {
            "title": titulo,
            "description": descricao,
            "color": cor,
            "footer": {"text": "Monitor • Receita Federal"},
            "timestamp": datetime.now(timezone.utc).isoformat()
            }
        ]
    }

    # try:
        # resp = requests.post(, json=payload)
        # if resp.status_code in (200, 204):
        #     print("✅ Embed enviado ao Discord!")
        # else:
        #     print(f"⚠️ Erro {resp.status_code}: {resp.text}")
    # except Exception as e:
    #     print(f"❌ Falha ao enviar embed: {e}")


def enviar_email(nome, novos_links):
    if not novos_links:
        return