[![HitCount](http://hits.dwyl.com/learning-crawlers/bolsafamilia.svg)](http://hits.dwyl.com/learning-crawlers/bolsafamilia)

# Bolsa Familia
Extração de dados com Requests para listar brasileiros do Bolsa Família

## Modo de usar

Execute o arquivo run.py:

```bash
python run.py
```

## Resultado

**Schema**

- ms_referncia: string
- ms_competncia: string
- uf: string
- cdigo_municpio_siafi: string
- nome_municpio: string
- nis_favorecido: string
- nome_favorecido: string
- valor_parcela: string

**Dados**

```json
{
    "ms_referncia": "202001",
    "ms_competncia": "201901",
    "uf": "MG",
    "cdigo_municpio_siafi": "4123",
    "nome_municpio": "BELO HORIZONTE",
    "nis_favorecido": "16271288457",
    "nome_favorecido": "IOLANDA DE ASSIS SILVA CESARINO",
    "valor_parcela": "294,00"
}
```