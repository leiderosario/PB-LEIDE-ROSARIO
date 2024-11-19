def pares_ate(n: int):
    """Gera um gerador para os valores pares no intervalo [2, n].

    Args:
        n: O limite superior do intervalo.

    Yields:
        O próximo número par.
    """

    for numero in range(2, n+1, 2):
        yield numero