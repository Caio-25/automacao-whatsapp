from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from urllib.parse import quote
import time
opcoes = webdriver.ChromeOptions()

opcoes.add_argument(
    r"--user-data-dir=C:\Users\caios\Downloads\Projeto_watsapp_selenium")

navegador = webdriver.Chrome(options=opcoes)

navegador.get("https://web.whatsapp.com/")
# Esperar a tela do Whatsapp carregar -> espera um elemento que só existe na tela já carregada aparecer
while not navegador.find_elements(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[3]'):
    time.sleep(1)
time.sleep(2)

# Usa minha planilha pessoal apenas se ela existir localmente.
# Ela está no .gitignore e nunca será enviada ao GitHub.
if os.path.exists("dados/dados_automacao_selenium-v2.xlsx"):
    tabela = pd.read_excel("dados/dados_automacao_selenium-v2.xlsx")

# Caso contrário, usa a planilha de teste.
else:
    tabela = pd.read_excel("dados/Envios.xlsx")


# Enviar uma mensagem para cada pessoa
# Para cada linha na tabela
for linha in tabela.index:
    nome = tabela.loc[linha]['nome']
    mensagem = tabela.loc[linha]['mensagem']
    arquivo = tabela.loc[linha]['arquivo']
    telefone = tabela.loc[linha]['telefone']

    # Usa o replace para inverter o nome "fulano" para o nome que esta na tabela
    texto = mensagem.replace('fulano',nome)

    # serve para transformar o texto em um formato seguro para colocar dentro de uma URL.
    texto = quote(texto)

    print(texto)

    # Envia a mensagem
    link = (f"https://web.whatsapp.com/send?phone={telefone}&text={texto}")
    time.sleep(5)

    # Abre a conversa no WhatsApp
    navegador.get(link)
    print(f"Abrindo comversa de  {nome}")

    time.sleep(5)

    # Esperar a tela do Whatsapp carregar -> espera um elemento que só existe na tela já carregada aparecer
    while not navegador.find_elements(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[3]'):
        time.sleep(1)

    # Tempo para que o WatsApp abra por garantia
    time.sleep(2)

    navegador.find_element(By.XPATH,
                       '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[5]/div/span/div/button/div/div/div[1]/span').click()

if arquivo and str(arquivo).upper() != "N":
    caminho_completo = os.path.join("dados", "arquivos", str(arquivo))


# Mantém o navegador aberto até você apertar ENTER.
input("Pressione ENTER para sair")

# Fecha o navegador
navegador.quit()


