# Exercício 11
# Leia o arquivo person.json, faça o parsing e imprima seu conteúdo.
# Dica: leia a documentação do pacote json

import json

try:
    with open('person.json', 'r') as file:
        data = json.load(file)
    print(data)
except FileNotFoundError:
    print("Erro: O arquivo 'person.json' não foi encontrado.")
except json.JSONDecodeError:
    print("Erro: O arquivo 'person.json' não contém um JSON válido.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
