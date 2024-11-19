# Código original
with open('number.txt', 'r') as arquivo:
    num = list(map(int, arquivo.readlines()))

numeros_pares = filter(lambda x: x % 2 == 0, num)
maiores_num_pares = sorted(numeros_pares, reverse=True)[:5]
soma_maiores_num = sum(maiores_num_pares)

print(maiores_num_pares)
print(soma_maiores_num)
