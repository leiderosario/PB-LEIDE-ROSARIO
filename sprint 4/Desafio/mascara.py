import hashlib

while True:
    entrada = input("Digite uma palavra para mascarar ou digite sair para encerrar: ")
    if entrada.lower() == 'sair':
        break
    mascara = hashlib.sha1(entrada.encode())
    print("Hash SHA-1:", mascara.hexdigest())