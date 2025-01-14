import names
import random

qtd_nomes_unicos = 3880  
qtd_nomes_aleatorios = 10000000  


nomes_unicos = []

try:
   
    for _ in range(qtd_nomes_unicos):
        nomes_unicos.append(names.get_full_name())

    nomes_aleatorios = []

    for _ in range(qtd_nomes_aleatorios):
        nome_aleatorio = random.choice(nomes_unicos)
        nomes_aleatorios.append(nome_aleatorio)

    with open("nomes_aleatorios.txt", "w") as arquivo:
        for nome in nomes_aleatorios:
            arquivo.write(nome + "\n")

    print(f"Gerados {qtd_nomes_aleatorios} nomes aleatórios e salvos em 'nomes_aleatorios.txt'")

except KeyboardInterrupt:
    print("\nOperação interrompida pelo usuário.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")