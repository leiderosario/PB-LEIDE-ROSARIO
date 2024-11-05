with open('actors.csv', 'r') as file:
    resultado = []
    for linha in file:
        palavras = linha.rsplit(',',5)
        resultado.append(palavras[:])

for coluna in resultado [1::]:
    with open ('etapa5.txt', 'at', encoding='utf-8') as text:
        text.write('Ator: {} | Faturamento Bruto Total: {}\n'.format(coluna[0],coluna[1]).replace('"',''))