from functools import reduce

def calcula_saldo(transacoes) -> float:
    valores_modificados = map(lambda item: item[0] if item[1] == 'C' else -item[0], transacoes)
    
    saldo_atualizado = reduce(lambda acumulador, valor: acumulador + valor, valores_modificados)
    
    return saldo_atualizado

movimentacoes_financeiras = [
    (200, 'D'),
    (300, 'C'),
    (100, 'C')
]

saldo_final = calcula_saldo(movimentacoes_financeiras)
print(saldo_final)