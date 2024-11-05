with open('actors.csv', 'r') as file:
    resultado = []
    for linha in file:
        palavras = linha.rsplit(',', 5)
        resultado.append(palavras[:])

for coluna in resultado[1::]:
    faturamentototal = coluna[3]
    with open ('etapa2.txt', 'at', encoding='utf-8') as text:
        text.write('Ator/atriz {} possui média de faturamento bruto{}.\n'.format(coluna[0],faturamentototal).replace('"',''))
        text.close()