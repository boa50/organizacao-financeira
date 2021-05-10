from flask import Flask
app = Flask(__name__)

import xml.etree.ElementTree as ET

def formata_moeda(valor):
    return "R$ {:.2f}".format(valor)

@app.route('/')
def home():
    codigo = ''
    valor_patrimonial_cota = valor_patrimonial(codigo)

    return codigo + ' - Valor patrimonial: ' + formata_moeda(valor_patrimonial_cota)

@app.route('/valor-patrimonial/<codigo>')
def valor_patrimonial(codigo):
    tree = ET.parse('app/arquivos/' + codigo + '/mensal.xml')
    root = tree.getroot()

    valor_patrimonial_cota = (float(root.find('InformeMensal') 
                                .find('Resumo')
                                .find('ValorPatrCotas').text))

    return valor_patrimonial_cota

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')