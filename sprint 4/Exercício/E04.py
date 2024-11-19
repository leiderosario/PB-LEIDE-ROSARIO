def calcular_valor_maximo(operadores, operandos):
    """
    Calcula o maior resultado de uma série de operações.

    Args:
        operadores: Lista de operadores (+, -, *, /, %).
        operandos: Lista de tuplas com os operandos.

    Returns:
        O maior resultado das operações.
    """

    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else None,
        '%': lambda x, y: x % y if y != 0 else None
    }

    resultados = map(lambda x: operations[x[0]](*x[1]), zip(operadores, operandos))
    return max(resultados)