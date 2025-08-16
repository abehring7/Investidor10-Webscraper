# Investidor10-Webscraper
Webscraper simples para o site www.investidor10.com.br puxa e baixa em arquivo excel (.xlsx) todos os dividendos, bonificações, e juros sobre capital próprio dispóniveis no site para determinado ativo, seja ele FII ou ação.

Como usar?:
  No fim do código tem a função sitezin() que tem os argumentos ("tipo do ativo", "ativo"). Por padrão está como tipo "acoes" e o ativo como "vale3".
  Para pegar um FII por exemplo, o HGLG11, escreva: sitezin("fiis", "hglg11").
  Paralelamente, para extrair os proventos de outra ação que não seja Vale3, apenas mude o segundo argumento, exemplo com banco ItaúPN: sitezin("acoes", "itub4"). ATENÇÃO: os inputs na função devem ser em minúsculo e sem acentuação.
IMPORTANTE!!!: O script está programado para utilização em navegadores Mozilla, caso esteja em Chrome apenas delete ou comente(com #) a linha 12:

options.binary_location = r"C:\Program Files\Mozilla\browser.exe" ## caminho do browser mozilla



Utilidade:
  Pelo script possibilitar exportar para .xlsx localmente, é possível utilizar a biblioteca Pandas e seus métodos para fazer análises de portifólio para as ações e FIIS pagadoras de dividendos. Ou usar outras bibliotecas para fazer análises quantitativas e estatísticas mais avançadas.
