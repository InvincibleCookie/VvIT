import math
a, b, c = map(int, input().split())
D = b * b - 4 * a * c
if a != 0 and b != 0 and c != 0:
    if D > 0 :
        print(f'x1 = {(-b + math.sqrt(D)) / (2 * a)}\n'
              f'x2 = {(-b - math.sqrt(D)) / (2 * a)}')
    elif D == 0:
        print(f'x = {(-b + math.sqrt(D)) / (2 * a)}')
    else:
        print('Корней нет')
elif a != 0 and b != 0:
    print(f'x1 = {0}\n'
          f'x2 = {-b/a}')
elif a != 0 and c != 0:
    if ((a > 0 and c < 0) or (a < 0 and c > 0)):
        print(f'x1 = {math.sqrt(abs(c)/abs(a))}\n'
              f'x2 = -{math.sqrt(abs(c)/abs(a))}')
    else:
        print('Корней нет')
elif b != 0:
    print(f'x = {-c/b}')
else:
    print('x - Любое число')
    
