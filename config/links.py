import os

from anyio import Path

# ============================================================
# Constantes
# ============================================================
INTERVALO = 3600 * 12  # 12 horas

ARQUIVO_CACHE = "documentos_fiscais.json"

GIST_DESCRIPTION = 'An example file upload via Python'

PUBLIC = True

CAMINHO_CACHE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")

GITHUB_PAT = os.getenv("GITHUB_PAT")

URLS_FISCAIS = {
    "NFe": "https://www.nfe.fazenda.gov.br/portal/principal.aspx/",
    "MDFe": "https://dfe-portal.svrs.rs.gov.br/Mdfe/Documentos/",
    "CTe": "https://www.cte.fazenda.gov.br/portal/",
    "NFCe": "https://www.nfe.fazenda.gov.br/portal/principal.aspx/"
}

PORTAIS_FISCAIS_UF = {
    "AC": {
        "NFCe": "https://www.sefaz.ac.gov.br/nfce",
        "MDFe": "https://www.sefaz.ac.gov.br/mdfe"
    },
    "AL": {
        "NFCe": "https://nfce.sefaz.al.gov.br",
        "MDFe": "https://www.sefaz.al.gov.br/mdfe"
    },
    "AM": {
        "NFCe": "https://nfce.sefaz.am.gov.br",
        "MDFe": "https://www.sefaz.am.gov.br/mdfe"
    },
    "AP": {
        "NFCe": "https://www.sefaz.ap.gov.br/nfce",
        "MDFe": "https://www.sefaz.ap.gov.br/mdfe"
    },
    "BA": {
        "NFCe": "https://www.sefaz.ba.gov.br/nfce",
        "MDFe": "https://www.sefaz.ba.gov.br/mdfe"
    },
    "CE": {
        "NFCe": "https://nfce.sefaz.ce.gov.br",
        "MDFe": "https://www.sefaz.ce.gov.br/mdfe"
    },
    "DF": {
        "NFCe": "https://www.sefaz.df.gov.br/nfce",
        "MDFe": "https://www.sefaz.df.gov.br/mdfe"
    },
    "ES": {
        "NFCe": "https://sefaz.es.gov.br/nfce",
        "MDFe": "https://sefaz.es.gov.br/mdfe"
    },
    "GO": {
        "NFCe": "https://www.sefaz.go.gov.br/nfce",
        "MDFe": "https://www.sefaz.go.gov.br/mdfe"
    },
    "MA": {
        "NFCe": "https://www.sefaz.ma.gov.br/nfce",
        "MDFe": "https://www.sefaz.ma.gov.br/mdfe"
    },
    "MG": {
        "NFCe": "https://www.fazenda.mg.gov.br/empresas/nfce",
        "MDFe": "https://www.fazenda.mg.gov.br/empresas/mdfe"
    },
    "MS": {
        "NFCe": "https://www.sefaz.ms.gov.br/nfce",
        "MDFe": "https://www.sefaz.ms.gov.br/mdfe"
    },
    "MT": {
        "NFCe": "https://www.sefaz.mt.gov.br/nfce",
        "MDFe": "https://www.sefaz.mt.gov.br/mdfe"
    },
    "PA": {
        "NFCe": "https://www.sefaz.pa.gov.br/nfce",
        "MDFe": "https://www.sefaz.pa.gov.br/mdfe"
    },
    "PB": {
        "NFCe": "https://www.sefaz.pb.gov.br/nfce",
        "MDFe": "https://www.sefaz.pb.gov.br/mdfe"
    },
    "PE": {
        "NFCe": "https://www.sefaz.pe.gov.br/nfce",
        "MDFe": "https://www.sefaz.pe.gov.br/mdfe"
    },
    "PI": {
        "NFCe": "https://www.sefaz.pi.gov.br/nfce",
        "MDFe": "https://www.sefaz.pi.gov.br/mdfe"
    },
    "PR": {
        "NFCe": "https://www.fazenda.pr.gov.br/nfce",
        "MDFe": "https://www.fazenda.pr.gov.br/mdfe"
    },
    "RJ": {
        "NFCe": "https://www.sefaz.rj.gov.br/nfce",
        "MDFe": "https://www.sefaz.rj.gov.br/mdfe"
    },
    "RN": {
        "NFCe": "https://www.sefaz.rn.gov.br/nfce",
        "MDFe": "https://www.sefaz.rn.gov.br/mdfe"
    },
    "RO": {
        "NFCe": "https://www.sefin.ro.gov.br/nfce",
        "MDFe": "https://www.sefin.ro.gov.br/mdfe"
    },
    "RR": {
        "NFCe": "https://www.sefaz.rr.gov.br/nfce",
        "MDFe": "https://www.sefaz.rr.gov.br/mdfe"
    },
    "RS": {
        "NFCe": "https://www.sefaz.rs.gov.br/nfce",
        "MDFe": "https://www.sefaz.rs.gov.br/mdfe"
    },
    "SC": {
        "NFCe": "https://www.sef.sc.gov.br/nfce",
        "MDFe": "https://www.sef.sc.gov.br/mdfe"
    },
    "SE": {
        "NFCe": "https://www.sefaz.se.gov.br/nfce",
        "MDFe": "https://www.sefaz.se.gov.br/mdfe"
    },
    "SP": {
        "NFCe": "https://portal.fazenda.sp.gov.br/servicos/nfce",
        "MDFe": "https://portal.fazenda.sp.gov.br/servicos/mdfe"
    },
    "TO": {
        "NFCe": "https://www.sefaz.to.gov.br/nfce",
        "MDFe": "https://www.sefaz.to.gov.br/mdfe"
    }
}