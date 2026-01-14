### Salvando bibliotecas no requirements.txt

```
pip freeze > requirements.txt
```

### Instalando as bibliotecas do requirements.txt

```
pip install -r requirements.txt
```

### Rodar o script

```
uvicorn main:app --host 0.0.0.0 --port 8080
```