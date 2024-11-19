import csv

with open('estudantes.csv') as arquivo_estudantes:
    leitor_csv = csv.reader(arquivo_estudantes, delimiter=',')

    for cont in sorted(leitor_csv):
        notas = list(map(int, cont[1:]))
        notas_ord = sorted(notas, reverse=True)[:3]
        media = round(sum(notas_ord)/3, 2)
        print(f"Nome: {cont[0]} Notas: {notas_ord} Média: {media}")
        