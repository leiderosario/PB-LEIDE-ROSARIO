with open('actors.csv', 'r') as file:
    resultado = []
    for linha in file:
        palavras = linha.rsplit(',', 5)
        resultado.append(palavras[:])

numerofilmes = []
for coluna in resultado[1::]:
    numerofilmes.append(coluna[2])
    maior = max(numerofilmes)
    if coluna[2] == maior:
        ator= coluna[0]
print(ator, maior)

with open ('etapa1.txt', 'w', encoding='utf-8') as text:
    text.write('Apresente o ator/atriz com maior número de filmes e a respectiva quantidade:')
    text.write('\nAtor com mais filmes: {}, quantidade filmes: {}.'.format(ator, maior))
    text.close()