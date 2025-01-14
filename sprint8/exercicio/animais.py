animais = ['cachorro', 'gato', 'elefante', 'girafa', 'leão', 'tigre', 'macaco', 'panda', 'coelho', 'rato', 'cavalo', 'vaca', 'ovelha', 'porco', 'galinha', 'pato', 'peixe', 'pássaro', 'cobra', 'jacaré']


animais.sort()

for animal in animais:
    print(animal)
import random
import time
import names

random.seed(48)
qtd_nomes_unicos = 3880
qtd_nomes_aleatorios = 10000000

nomes_unicos = set()

while len(nomes_unicos) < qtd_nomes_unicos:
    nome = names.get_full_name()
    nomes_unicos.add(nome)

nomes_aleatorios = []
for _ in range(qtd_nomes_aleatorios):
    nome = random.choice(list(nomes_unicos))
    nomes_aleatorios.append(nome)

with open("nomes.csv", "w") as arquivo:
    for nome in nomes_aleatorios:
        arquivo.write(nome + "\n")