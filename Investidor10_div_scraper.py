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

dfs = [] ## onde vai ficar os dfs

def qtd_botoes():
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
    return dfs_div

def transformar_em_excel():
    while True:
        caminho = input("Digite o camiho e o nome do arquivo que quer salvar no PC: (exemplo: C:\\Users\\Nome\\Local\\arquivo): ")
        caminho = caminho.replace("\\", "\\\\")
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
            print(f"Nao foi especificado o nome do arquivo, tente novamente{e}")



def clicar_localizar_next():
    try:
        localizador = (By.CSS_SELECTOR, "#table-dividends-history_next") ## trocar o botao pela paginacao next(tirar parametro)
        botao = wait.until(EC.presence_of_element_located(localizador))
   
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        driver.execute_script("""arguments[0].scrollIntoView({behavior:'instant', block:'center' });""", botao)
        

        driver.execute_script("arguments[0].click();", botao)
        wait.until(EC.presence_of_element_located((By.ID, "table-dividends-history")))
        pegar_tabelas()

    except Exception as e:
        print(f"nao foi possivel executar a funcao erro {e}")
        return botao



def pegar_tabelas():
    try:
        tabela_div = driver.find_elements(By.ID, "table-dividends-history")
        for i, tabelas in enumerate(tabela_div):
            linhas = tabelas.find_elements(By.TAG_NAME, "tr")
            for linha in linhas:
                celulas = linha.find_elements(By.TAG_NAME, "td")
                if celulas:
                    dados = [col.text.strip() for col in celulas]
                    dfs.append(dados)
    except Exception as e:
        print(f"Falha ao buscar tabelas erro: {e}")

## cria funcao para automatizar o next pelo num de botoes, com true e saindo no class disabled


def automatizar_next():
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
## organizar odf
