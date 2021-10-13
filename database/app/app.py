from flask import Flask
app = Flask(__name__)

import xml.etree.ElementTree as ET
import json
import requests

def formata_moeda(valor):
    return "R$ " + formata_decimal(valor)

def formata_decimal(valor):
    return "{:.2f}".format(valor)

@app.route('/')
def home():
    codigo = ''
    pvpa, valor_atual_cota, valor_patrimonial_cota = p_vpa(codigo)

    return codigo + \
        '<br>P/VPA: ' + formata_decimal(pvpa) + \
        '<br>Valor atual: ' + formata_moeda(valor_atual_cota) + \
        '<br>Valor patrimonial: ' + formata_moeda(valor_patrimonial_cota)

@app.route('/valor-patrimonial/<codigo>')
def valor_patrimonial(codigo):
    tree = ET.parse('app/arquivos/' + codigo + '/mensal.xml')
    root = tree.getroot()

    valor_patrimonial_cota = (root.find('InformeMensal') 
                                .find('Resumo')
                                .find('ValorPatrCotas').text)

    return float(valor_patrimonial_cota)

@app.route('/valor-cota/<codigo>')
def valor_cota(codigo):
    response = requests.get('https://query2.finance.yahoo.com/v10/finance/quoteSummary/' + codigo +'.sa?modules=price')
    if response.status_code in (200,):
        conteudo = json.loads(response.content)
        valor_atual_cota = conteudo['quoteSummary']['result'][0]['price']['regularMarketPrice']['fmt']

    return float(valor_atual_cota)

@app.route('/p-vpa/<codigo>')
def p_vpa(codigo):
    valor_patrimonial_cota = valor_patrimonial(codigo)
    valor_atual_cota = valor_cota(codigo)
    pvpa = valor_atual_cota / valor_patrimonial_cota

    return pvpa, valor_atual_cota, valor_patrimonial_cota

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')