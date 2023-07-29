def truth(x: int) -> bool:
    if x == 42:
        return True
    else:
        return False

if truth(input_int()):
    print(42)
else:
    print(0)
