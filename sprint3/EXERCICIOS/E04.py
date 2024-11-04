#Escreva um código Python para imprimir todos os números primos entre 1 até 100. Lembre-se que você deverá desenvolver o #cálculo que identifica se um número é primo ou não.
#Importante: Aplique a função range().

def primo(numero):
    if numero < 2:
        return False
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False
    return True

for num in range(1, 101):
    if primo(num):
        print(num)