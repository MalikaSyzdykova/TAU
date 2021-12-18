import control.matlab as matlab
import matplotlib.pyplot as pyplot
import numpy as numpy
import sympy
from sympy import *
import control
import math


wl = matlab.tf([1], [1])
w2 = matlab.tf([1], [10, 1])
w3 = matlab.tf([0.01 * 2, 1], [0.05 * 10, 1])
w4 = matlab.tf([20], [5, 1])

w5 = w2 * w3 * w4

# Обозначаем коэфф. для П регулятора
Kp1 = float(input('Введите коэф. Кр1 для П регулятора: '))

Wp1 = control.tf([Kp1], [1])
print(Wp1)
Wpid1 = control.parallel(Wp1)
print(Wpid1)

# Задаем размкнутую передаточную функцию
print("Paзомкнутая передаточная функция")
Wposl_pid1 = control.series(Wpid1, w5)
print(Wposl_pid1)

# Задаем замкнутую передаточную функцию
print("Замкнутая передаточная функция")
Wsum_pid1 = control.feedback(Wposl_pid1, wl)
print(Wsum_pid1)

# Обозначаем коэфф. для ПИД регулятора
Kp = float(input('Введите коэф. Кр для ПИД регулятора: '))
Ki = float(input('Введите коэф. Кi для ПИД регулятора: '))
Kd = float(input('Введите коэф. Кd для ПИД регулятора: '))

Wp = control.tf([Kp], [1])
print(Wp)
Wi = control.tf([Ki], [1, 0])
print(Wi)
Wd = control.tf([Kd, 0], [1])
print(Wd)

Wpid = control.parallel(Wp, Wi, Wd)
print(Wpid)



# Задаем размкнутую передаточную функцию
print("Paзомкнутая передаточная функция")
Wposl_pid = control.series(Wpid, w5)
print(Wposl_pid)

# Задаем замкнутую передаточную функцию
print("Замкнутая передаточная функция")
Wsum_pid = control.feedback(Wposl_pid, wl)
print(Wsum_pid)


time = []
for i in range(0, 2500):
    time.append(i / 100)



# Строим переходную характеристику для ПИД
pyplot.subplot()
pyplot.grid(True)
y, x = matlab.step(Wsum_pid, time)
pyplot.plot(x, y)
pyplot.title("Переходна характеристика ПИД")
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Bpeмя')
pyplot.show()

# Строим переходную характеристику для П
pyplot.subplot()
pyplot.grid(True)
y, x = matlab.step(Wsum_pid1, time)
pyplot.plot(x, y)
pyplot.title("Переходна характеристика П")
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Bpeмя')
pyplot.show()


# находим корни характеристичкского уравнения и определяем устойчивость системы
korny = matlab.pzmap(Wposl_pid)
pyplot.axis([-3, 1, -1, 1])
pyplot.show()
pole = matlab.pole(Wposl_pid)
print(pole)

roots = control.pole(Wsum_pid)
bestRoot = -1000
for i in roots:
    if i.real >= bestRoot:
        bestRoot = i.real

timReg = math.fabs(3/ bestRoot) #Время регулирования

max = 0
for i in roots:
    actual = math.fabs(sympy.im(i) / sympy.re(i))
    if actual > max:
        max = actual

perereg = (math.e**(-math.pi / max))*100 #Перерегулирование
kolebat = 1 - math.e**(-2 * math.pi / max) #Колебательность

print('Bpемя регулирования равно ', timReg)
print("Степень колебательности равна ", max)
print("Перерегулирование меньше, чем ", perereg)
print("Kолебательность равна ", kolebat)


#ДЛЯ П регулятора
def graph():
    mag, phase, omega = matlab.bode(Wposl_pid)
    pyplot.plot()

graph()
pyplot.show()

step = 0.1
Q = 0
for i in range(len(y)):
    Q = (Q + math.fabs(y[i] - y[2499]) * step)
print('Интеграл равен: ', Q)

# находим корни характеристичкского уравнения и определяем устойчивость системы
korny1 = matlab.pzmap(Wposl_pid1)
pyplot.axis([-3, 1, -1, 1])
pyplot.show()
pole = matlab.pole(Wposl_pid1)
print(pole)

roots1 = control.pole(Wsum_pid1)
bestRoot1 = -1000
for i in roots1:
    if i.real >= bestRoot1:
        bestRoot1 = i.real

timReg1 = math.fabs(3/ bestRoot1) #Время регулирования

max1 = 0
for i in roots1:
    actual = math.fabs(sympy.im(i) / sympy.re(i))
    if actual > max1:
        max1 = actual

perereg1 = (math.e**(-math.pi / max1))*100 #Перерегулирование
kolebat1 = 1 - math.e**(-2 * math.pi / max1) #Колебательность

print('Bpемя регулирования равно ', timReg1)
print("Степень колебательности равна ", max1)
print("Перерегулирование меньше, чем ", perereg1)
print("Kолебательность равна ", kolebat1)
