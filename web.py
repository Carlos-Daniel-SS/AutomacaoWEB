
# Automação para pegar cotação de moedas na web e recalcular valores de produtos.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Acessando o navegador:

navegador = webdriver.Chrome()

# Realizando a pesquisa e pegando o valor do dólar:

def pegar_dolar():

    navegador.get("https://www.google.com/")

    navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('Cotação dólar')

    navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

    valor_dolar = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

    return float(valor_dolar)


# Realizando a pesquisa e pegando o valor do euro:

def pegar_euro():

    navegador.get("https://www.google.com/")

    navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('Cotação euro')

    navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

    valor_euro = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

    return float(valor_euro)

# Realizando a pesquisa e pegando o valor do ouro:

def pegar_ouro():
        
    navegador.get("https://www.melhorcambio.com/ouro-hoje#:~:text=O%20valor%20do%20grama%20do,em%20R%24%20312%2C76.")

    valor_ouro = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')

    valor_ouro = valor_ouro.replace(',','.')
    
    return float(valor_ouro)

print('Cotação do dólar R$ {}, euro R$ {} e ouro R$ {}'.format(pegar_dolar(), pegar_euro(), pegar_ouro()))

# Importando base de dados dos produtos e alterando o valor de cada moeda:

tabela = pd.read_excel("Produtos.xlsx")

print('Tabela antes da atualização de valores: ', tabela)

tabela.loc[tabela['Moeda'] == 'Dólar', 'Cotação'] = pegar_dolar()

tabela.loc[tabela['Moeda'] == 'Euro', 'Cotação'] = pegar_euro()

tabela.loc[tabela['Moeda'] == 'Ouro', 'Cotação'] = pegar_ouro()

print(tabela)

# Realizando o recalculo de cada produto e exportando nova base de dados dos produtos:

tabela['Preço de Compra'] = tabela['Cotação'] * tabela['Preço Original']

tabela['Preço de Venda'] = tabela['Preço de Compra'] * tabela['Margem']

tabela['Preço de Venda'] = tabela['Preço de Venda'].map('R${:.2f}'.format)

print(tabela)

# Criando nova base de produtos com preço atualizado:

tabela.to_excel('Produtos_Novos_Preços.xlsx', index = False)