def fibonacci(n):
    """Вычисляет n-е число Фибоначчи (начиная с 0 для n=1)."""
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a
