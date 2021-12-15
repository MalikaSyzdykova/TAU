import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy
import numpy as np
import sympy
from numpy import linalg as LA
from sympy.solvers import solve
from sympy import Symbol

koc = .68

def stabilityTest(koc):
    # Исходные данные
    ky = 22
    tg = 8
    ty = 20
    # Турбина - гидро
    tgt = 1

    # Обратная связь
    toc = 3

    # Передаточная функция  обратной связи:
    woc = matlab.tf([koc], [toc, 1])

    # Передаточная функция генератора:
    wg = matlab.tf([1], [tg, 1])

    # Передаточная функция турбины:
    wt = matlab.tf([0.01 * tgt, 1], [0.05 * tg, 1])

    # Передаточная функция исполнительного устройства:
    wy = matlab.tf([ky], [ty, 1])

    # Эквивалентная передаточная функция
    equivalentLink = matlab.feedback(wy * wg * wt, woc, -1)
    print(equivalentLink)

    # Построение переходной характеристики
    [y, x] = matlab.step(equivalentLink)
    pyplot.plot(x, y)
    pyplot.title('Переходная характеристика')
    pyplot.ylabel('Амплитуда')
    pyplot.xlabel('Время, сек')
    pyplot.grid(True)
    pyplot.show()

    # Проверка устойчивости САУ

    sauPoles = matlab.pole(equivalentLink)
    sauZeros = matlab.zero(equivalentLink)
    print('Полюса передаточной функции:\n', sauPoles)
    print('Нули передаточной функции:\n', sauZeros)

    systemStability = True

    # Проверка устойчивости системы
    for i in sauPoles:
        if i.real > 0:
            systemStability = False
            break

    # Вывод сообщения о устойчивости / неустойчивости системы
    print('Система устойчива' if systemStability else 'Система неустойчива')

    # Проверка по критерию Найквиста

    # Размыкание САУ и оценка устойчивости по критерию Найквиста
    openSau = wt * wg * wy
    print(openSau)

    # Вывод диаграммы Найквиста
    matlab.nyquist(openSau)
    pyplot.grid(True)
    pyplot.title('Диаграмма Нейквиста')
    pyplot.xlabel('Re(s)')
    pyplot.ylabel('Im(s)')
    pyplot.show()

    # Определение запаса устойчивости

    # Снятие логарифмической амплитудно-частотной и логарифмической фазов-частотной характеристик разомкнутой системы
    matlab.bode(openSau, dB=False)
    pyplot.plot()
    axes = pyplot.gcf().get_axes()
    axes[0].set_title("ЛАЧХ")
    axes[1].set_title("ЛФЧХ")
    pyplot.xlabel('Частота, Гц')
    pyplot.show()

    # Проверка по критерию Михайлова

    # Суммирование числителя и знаменателя эквивалентной передаточной функции
    numeratorOfSAU = [float(x) for x in equivalentLink.num[0][0]]
    denominatorOfSAY = [float(x) for x in equivalentLink.den[0][0]]
    functionMikhailov = []
    print(functionMikhailov)
    for i in range(len(denominatorOfSAY) - len(numeratorOfSAU)):
        numeratorOfSAU.insert(0, 0)
    for i in range(len(numeratorOfSAU)):
        functionMikhailov.append(numeratorOfSAU[i] + denominatorOfSAY[i])
    functionGurvitz = functionMikhailov
    print(functionMikhailov)
    # Проверка устойчивости
    functionMikhailov = functionMikhailov[::-1]
    j = sympy.I
    omega = sympy.symbols("w")
    for i in range(len(functionMikhailov)):
        functionMikhailov[i] = functionMikhailov[i] * (j * omega) ** i
    x = numpy.arange(0, 1, 0.01)
    mc = []
    for i in x:
        summ = 0
        for k in functionMikhailov:
            summ += k.subs(omega, i)
        mc.append(summ)

    real = [sympy.re(x) for x in mc]
    imaginary = [sympy.im(x) for x in mc]
    numberOfAxisCrossings = 1
    flagCrossing = False
    flagPossibleCrossingX = True
    flagPossibleCrossingY = True
    for i in range(len(mc) - 1):
        if ((real[i] >= 0 and real[i + 1] <= 0) or (real[i] <= 0 and real[i + 1] >= 0)):
            if flagPossibleCrossingX:
                numberOfAxisCrossings += 1
                flagPossibleCrossingX = False
                flagPossibleCrossingY = True
            if imaginary[i] > 0:
                flagCrossing = True
        if ((imaginary[i] >= 0 and imaginary[i + 1] <= 0) or (imaginary[i] <= 0 and imaginary[i + 1] >= 0)):
            if flagPossibleCrossingY:
                numberOfAxisCrossings += 1
                flagPossibleCrossingX = True
                flagPossibleCrossingY = False
    if numberOfAxisCrossings >= 3 and flagCrossing:
        print('Система устойчива по критерию Михайлова')
    else:
        print('Система не устойчива по критерию Михайлова')

    # Построение годографа Михайлова
    pyplot.title('Годограф Михайлова')
    ax = pyplot.gca()
    ax.plot(real, imaginary)
    ax.grid(True)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    pyplot.xlim(-50, 200)
    pyplot.ylim(-50, 20)
    pyplot.xlabel("re")
    pyplot.ylabel("im")
    pyplot.show()

    # Проверка по критерию Гурвица
    # Построение матрицы и расчет ее определителя
    print('функц гурв', functionGurvitz)
    oddNumbersOfMatrix = []
    evenNumbersOfMatrix = []

    for i in range(0, len(functionGurvitz), 2):
        evenNumbersOfMatrix.append(functionGurvitz[i])
    for i in range(1, len(functionGurvitz), 2):
        oddNumbersOfMatrix.append(functionGurvitz[i])
    matrix = np.array([oddNumbersOfMatrix + [0],
                       evenNumbersOfMatrix,
                       [0] + oddNumbersOfMatrix])


    print('matrix[:2, :2]', matrix[:2, :2])
    print('matrix', matrix)

    det2 = LA.det(matrix[:2, :2])
    det3 = LA.det(matrix)

    print("det of minors:", det2, det3)

    # Проверка устойчивости по критерию Гурвица?
    if det2 < 0 or det3 < 0 or matrix[0][0] < 0 or matrix[1][0] < 0:
        print('Система неустойчива по критерию Гурвица')
    else:
        print('Система устойчива по критерию Гурвица')

    x = Symbol('x')
    a0, a1, a2, a3, a4 = functionGurvitz
    # a3 = 97.62 + koc * .22
    # a4 = koc * 22 + 23
    koc = solve(a1 * (a2 * (97.62 + x * .22) - a1 * (x * 22 + 23)) - (97.62 + x * .22)**2 * a0, x)
    print(koc)
    # Возвращение предельного значения koc
    return koc


koc_lst = stabilityTest(koc)

