import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
## inicialização do selenium (para firefox)
options = Options()
options.binary_location = r"C:\Program Files\LibreWolf\librewolf.exe" ## caminho do browser mozilla
service = Service(executable_path = r"C:\Users\Nome\Local\geckodriver.exe") ## caminho do geckodriver
driver = webdriver.Firefox(service=service, options=options)
actions = ActionChains(driver)
wait = WebDriverWait(driver, 15)

dfs = [] ## onde vai ficar os dados

def qtd_botoes(): ## pega o ultimo botão da DOM do site, extraindo assim, a quantidade de botões.
    sel_botao = driver.find_element(
        By.CSS_SELECTOR, "a[data-dt-idx='6']"
    )
    num_botao = sel_botao.text
    return num_botao

def sitezin(tipo, ativo):
     url = f"https://investidor10.com.br/{tipo}/{ativo}/"
     driver.get(url)

def sel_excel():
    while True:
        sel = str(input("deseja colocar o dataframe baixado no PC?: {S/N}: ")).upper()
        if(sel=="S"):
            transformar_em_excel()
            break
        elif(sel=="N"):
            print("Arquivo nao foi salvo")
            break
        else:
            print("Entrada invalida, deve ser [s ou n] ")


def formatacao_df():
    global dfs_div 
    dfs_div = pd.DataFrame(dfs)
    dfs_div.columns = ["Proventos", "Data_COM", "Pagamento", "Valor Pago"]
    print(dfs_div)

def transformar_em_excel():
    while True:
        caminho = input("Digite o camiho e o nome do arquivo que quer salvar no PC: (exemplo: C:\\Users\\Nome\\Local\\arquivo): ")
        caminho = caminho.replace("\\", "\\\\") ## replace nas barras pro input do usuario ficar como raw string
        if not caminho:
            print("Caminho vazio arquivo nao salvo.")
            return
        if not caminho.endswith(".xlsx"):
            caminho += ".xlsx"
        try:
            dfs_div.to_excel(caminho, index=False)
            print(f"Salvo com sucesso em {caminho}")
            break
        except Exception as e:
            print(f"Nao foi especificado o nome do arquivo, tente novamente error: {e}")



def clicar_localizar_next(): ## Localiza e clica no botão "Próximo" para navegar entre as tabelas
    try:
        localizador = (By.CSS_SELECTOR, "#table-dividends-history_next") ## o botao "Proximo" por seletor CSS.
        botao = wait.until(EC.presence_of_element_located(localizador))  ## espera ate o elemento estar presente no DOM
   

        driver.execute_script("""arguments[0].scrollIntoView({behavior:'instant', block:'center' });""", botao) ## scrolla ate o botao estar visivel
        

        driver.execute_script("arguments[0].click();", botao) ## clica no botao por JS
        wait.until(EC.presence_of_element_located((By.ID, "table-dividends-history"))) ## espera ate a nova tabela de dividendos renderizar
        pegar_tabelas()

    except Exception as e:
        print(f"Não foi possivel executar a funcao erro: {e}")
        return botao



def pegar_tabelas():
    try:
        tabela_div = driver.find_elements(By.ID, "table-dividends-history") ## acha a tabela de Dividendos
        for i, tabelas in enumerate(tabela_div):                            ## itera sobre as (linhas, index) da tabela
            linhas = tabelas.find_elements(By.TAG_NAME, "tr")               ## encontra as linhas tag="tr"
            for linha in linhas:                                            ## itera sobre as celulas das linhas, os dados nas table row
                celulas = linha.find_elements(By.TAG_NAME, "td")            ## encontra as celulas tag="td"
                if celulas:                                                 ## caso celulas = True
                    dados = [col.text.strip() for col in celulas]           ## formata os dados das celulas tirando os espaços em branco
                    dfs.append(dados)                                       ## manda os dividendos da linha para a lista "dfs"
    except Exception as e:
        print(f"Falha ao buscar tabelas erro: {e}")




def automatizar_next(): ## cria funcao para automatizar o click no next pelo num de botoes
    botoes = qtd_botoes()
    for i in range(0, int(botoes)-2):
        clicar_localizar_next()
    

sitezin("acoes", "vale3")
qtd_botoes()
pegar_tabelas()
clicar_localizar_next() ## testar isso assim primeiro
automatizar_next()
formatacao_df()
sel_excel()
