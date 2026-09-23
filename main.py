from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from urllib.parse import quote
import time

opcoes = webdriver.ChromeOptions()

opcoes.add_argument(
    r"--user-data-dir=C:\Users\caios\Downloads\Projeto_watsapp_selenium"
)

navegador = webdriver.Chrome(options=opcoes)

navegador.get("https://web.whatsapp.com/")

# Esperar a tela do WhatsApp carregar
# Espera um elemento que só existe na tela já carregada aparecer
while not navegador.find_elements(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[3]'):
    time.sleep(1)

time.sleep(2)

# Usa minha planilha pessoal apenas se ela existir localmente.
# Ela está no .gitignore e nunca será enviada ao GitHub.
if os.path.exists("dados/dados_automacao_selenium-v2 (2).xlsx"):
    tabela = pd.read_excel("dados/dados_automacao_selenium-v2 (2).xlsx")
    pasta_arquivos = "dados/foto"

# Caso contrário, usa a planilha de teste.
else:
    tabela = pd.read_excel("dados/Envios.xlsx")
    pasta_arquivos = "dados/arquivos"

print(tabela.head())

# Enviar uma mensagem para cada pessoa
# Para cada linha na tabela
for linha in tabela.index:

    nome = tabela.loc[linha]['nome']
    mensagem = tabela.loc[linha]['mensagem']
    arquivo = tabela.loc[linha]['arquivo']
    telefone = tabela.loc[linha]['telefone']

    print(f"Abrindo conversa de {nome}")
    print("Nome:", nome)
    print("Mensagem:", mensagem)
    print("Arquivo:", arquivo)

    # Usa o replace para trocar "fulano" pelo nome da pessoa
    texto = mensagem.replace('fulano', nome)

    # Transforma o texto em um formato seguro para colocar dentro de uma URL
    texto = quote(texto)

    # Envia a mensagem
    link = f"https://web.whatsapp.com/send?phone={telefone}&text={texto}"

    time.sleep(5)

    # Abre a conversa no WhatsApp
    navegador.get(link)

    time.sleep(5)

    # Esperar a tela do WhatsApp carregar
    while not navegador.find_elements(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[3]'):
        time.sleep(1)

    # Tempo para que o WhatsApp abra por garantia
    time.sleep(2)

    navegador.find_element(By.XPATH,
                           '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[5]/div/span/div/button/div/div/div[1]/span').click()

    if arquivo and str(arquivo).upper() != "N":
        caminho_completo = os.path.join(
            pasta_arquivos,
            str(arquivo)
        )

        print("Caminho do arquivo:", caminho_completo)
        print("Arquivo existe?", os.path.exists(caminho_completo))

        # Clica no botão de anexar
        botao_anexar = navegador.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Anexar"]'
        )

        botao_anexar.click()

        time.sleep(2)

        # Encontra os campos de arquivo
        campos_arquivo = navegador.find_elements(
            By.CSS_SELECTOR,
            'input[type="file"]'
        )

        print(
            "Quantidade de campos de arquivo:",
            len(campos_arquivo)
        )

        # Como encontramos apenas 1, pegamos o primeiro
        campo_arquivo = campos_arquivo[0]

        # Envia a imagem
        campo_arquivo.send_keys(
            os.path.abspath(caminho_completo)
        )

        print("Arquivo selecionado!")

        time.sleep(2)

        botoes = navegador.find_elements(
            By.CSS_SELECTOR,
            'button'
        )

        print("Quantidade de botões:", len(botoes))
        # Encontra os campos de arquivo
        campos_arquivo = navegador.find_elements(
            By.CSS_SELECTOR,
            'input[type="file"]'
        )

        print(
            "Quantidade de campos de arquivo:",
            len(campos_arquivo)
        )

        # Pega o último campo de arquivo
        campo_arquivo = campos_arquivo[-1]

        # Envia a imagem
        campo_arquivo.send_keys(
            os.path.abspath(caminho_completo)
        )

        print("Arquivo selecionado!")

        time.sleep(2)

        # Procura o botão Enviar
        botao_enviar = navegador.find_element(
            By.CSS_SELECTOR,
            '[aria-label^="Enviar"]'
        )

        # Clica para enviar
        botao_enviar.click()

        print("Arquivo enviado!")

    print("-----------------------------")

# Mantém o navegador aberto até você apertar ENTER
input("Pressione ENTER para sair")

# Fecha o navegador
navegador.quit()