def func(a: int, b: int, c: int, d: int, e: int, f: int, g: int, h: int) -> int:
    if h == 0:
        return 42
    else:
        return func(a, b, c, d, e, f, g, h)

print(func(0, 0, 0, 0, 0, 0, 0, 0))
