def conta_vogais(texto:str)-> int:
    vogais = 'aeiouAEIOU'

    vogais_identificadas = filter(lambda char: char in vogais, texto)
    
    return len(list(vogais_identificadas))

resultado = conta_vogais(" ")
print(resultado)