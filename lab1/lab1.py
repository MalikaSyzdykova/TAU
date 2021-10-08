import matplotlib.pyplot as plt
from control import matlab
import numpy as numpy
import math


def choise():
    inertialessUnitName = 'Безынерционое звено'
    aperiodicUnitName = 'Апериодическое звено'
    integUnitName = 'Интегрирующее звено'
    idifUnitName = 'Идеальное дифференцирующее звено'
    rdifUnitName = 'Реальное дифференцирующее звено'

    needNewChoise = True

    while needNewChoise:
        userInput = input('Введите номер команды: \n' +
                          '1- ' + inertialessUnitName + '\n' +
                          '2- ' + aperiodicUnitName + '\n' +
                          '3- ' + integUnitName + '\n' +
                          '4- ' + idifUnitName + '\n' +
                          '5- ' + rdifUnitName + '\n')
        if userInput.isdigit():
            needNewChoise = False
            userInput = int(userInput)
            if userInput == 1:
                name = 'Безынерционное звено'
            elif userInput == 2:
                name = 'Апериодическое звено'
            elif userInput == 3:
                name = 'Интегрирующее звено'
            elif userInput == 4:
                name = 'Идеальное дифференцирующее звено'
            elif userInput == 5:
                name = 'Реальное дифференцирующее звено'
            else:
                print('Недопустимое значение')
                needNewChoise = True

        else:
            print('\n Пожалуста введите числовое значение!\n')
            needNewChoise = True
    return name


def getUnit(name):
    k = input('пожалуймта введите k :')
    t = input('пожалуймта введите t :')
    unit = None

    if k.isdigit() and t.isdigit():
        k = int(k)
        t = int(t)

        if name == 'Безынерционное звено':
            unit = matlab.tf([k], [1])
        elif name == 'Апериодическое звено':
            unit = matlab.tf([k], [t, 1])

        elif name == 'Интегрирующее звено':
                unit = matlab.tf([1], [t, 0])

        elif name == 'Идеальное дифференцирующее звено':
                unit = matlab.tf([t, 0], [1e-5, 1])
        elif name == 'Реальное дифференцирующее звено':
            unit = matlab.tf([k, 0], [t, 1])
    else:
        print('\n Пожалуста введите числовое значение!\n')

    return unit


def graph(num, title, y, x):
    plt.subplot(2, 1, num)
    plt.grid(True)
    if title == 'Переходная характеристика':
        plt.plot(x, y, 'purple')
    elif title == 'Импульсная характеристика':
        plt.plot(x, y, 'green')
    plt.title(title)
    plt.ylabel('Амплитуда')
    plt.xlabel('Время, c')


if __name__ == '__main__':

    unitName = choise()
    unit = getUnit(unitName)
    if unit is None:
        raise ValueError("Что-то пошло не так")

    print(unit)

    timeLine = []
    for i in range(0, 10000):
        timeLine.append(i / 1000)

    [y, x] = matlab.step(unit, timeLine)
    graph(1, 'Переходная характеристика', y, x)
    [y, x] = matlab.impulse(unit, timeLine)
    graph(2, 'Импульсная характеристика', y, x)

    plt.show()
    matlab.bode(unit, dB=False)
    plt.plot()
    plt.xlabel('Частота, Гц')
    plt.show()
