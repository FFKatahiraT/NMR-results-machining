#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import matplotlib.axes
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def func(x, D, p):
	return p*np.exp(-D*x)

def func1(x_new, D1, p1):
	return p1*np.exp(-D1*x_new)

def func2(x_new2, D2, p2):
	return p2*np.exp(-D2*x_new2)

def func3(x_new3, D3, p3):
	return p3*np.exp(-D3*x_new3)

gamma = 4.258
LD = 3
BD = 55
gradient, experiment, x = [], [], []
NAME_list= 'il20_293K_D_2'
NAME = str(NAME_list)
png = '.png'
NAME_png_list = NAME_list+png
NAME_png = str(NAME_png_list)
with open(NAME, 'r') as data:
	data_new = data.readlines()[26:74] 
	i =0
	while i < len(data_new):
		elements = data_new[i].strip().split('    ')
		gradient.append(float(elements[1]))
		experiment.append(float(elements[2]))
		i += 1

x=[]
i=0
while i<len(gradient):
	x.append(((2.0*np.pi*gamma*gradient[i]*LD)**2*(BD - LD/3))/10**11)
	i+=1
m = np.amax(experiment)
i = 0
while i < len(experiment):
	experiment[i] = experiment[i]/m
	i+=1

x_new = list(x)
exp_new = list(experiment)	
while True:
	try:
		popt, pcov = curve_fit(func1, x_new, exp_new) 
		D1, p1 = popt 
		break
	except:
		print('Runtime')
		del(x_new[0])
		del(exp_new[0])
perr = np.sqrt(np.diag(pcov))
perr_m=[]
perr1_m=[]
popt_m=[]
i=4
while i<len(x_new):
	popt, pcov = curve_fit(func1, x_new, exp_new) 
	perr = np.sqrt(np.diag(pcov))
	perr_m.append(perr[0])
	perr1_m.append(perr[1])
	popt_m.append(popt)
	del(x_new[0])
	del(exp_new[0])
i = np.argmin(perr_m)
perr1=perr_m[i]
perr1p = perr1_m[i]
D1, p1 = popt_m[i]
del(perr_m)
del(perr1_m)
del(popt_m)
x_new=list(x)
exp_new = list(experiment)
del(x_new[:i])
del(exp_new[:i])
print(len(x_new), 'x_new')

x_new2 = list(x)
exp_new2 = list(experiment)
i=0
while i<len(x):
	exp_new2[i]=exp_new2[i]-p1*np.exp(-D1*x[i])
	i+=1
i=0
while i<len(x_new2) :
	if exp_new2[i]<experiment[47]:
		del(exp_new2[i:])
		del(x_new2[i:])
	i+=1
while True:
	try:
		popt, pcov = curve_fit(func2, x_new2, exp_new2) 
		D2, p2 = popt 
		break
	except:
		print('Runtime')
		del(x_new2[0])
		del(exp_new2[0])
perr_m=[]
perr1_m=[]
popt_m=[]
i=4
while i<len(x_new2):
	popt, pcov = curve_fit(func2, x_new2, exp_new2) 
	perr = np.sqrt(np.diag(pcov))
	perr_m.append(perr[0])
	perr1_m.append(perr[1])
	popt_m.append(popt)
	del(x_new2[0])
	del(exp_new2[0])
count = np.argmin(perr_m)
perr2=perr_m[count]
perr2p=perr1_m[count]
D2, p2 = popt_m[count]
x_new2 = list(x)
exp_new2 = list(experiment)
i=0
while i<len(x):
	exp_new2[i]=exp_new2[i]-p1*np.exp(-D1*x[i])
	i+=1
i=0
while i<len(x_new2) :
	if exp_new2[i]<experiment[47]:
		del(exp_new2[i:])
		del(x_new2[i:])
	i+=1
del(x_new2[:count])
del(exp_new2[:count])
del(count)
print(len(x_new2), 'x_new2')
del(perr_m)
del(perr1_m)
del(popt_m)


x_new3 = list(x)
exp_new3 = list(experiment)
if len(x_new)+len(x_new2)>len(x)-3:
	D3 =0
	p3=0
	perr3=0
	perr3p=0
else:
	i=0
	while i<len(x):
		exp_new3[i]=exp_new3[i]-p1*np.exp(-D1*x[i])-p2*np.exp(-D2*x[i])
		i+=1
	i=0
	while i<len(x_new3) :
		if exp_new3[i]<0.001:
			del(exp_new3[i:])
			del(x_new3[i:])
		i+=1
	while True:
		try:
			popt, pcov = curve_fit(func3, x_new3, exp_new3) 
			D3, p3 = popt 
			break
		except:
			print('Runtime')
			if len(x_new3)<3:
				print('approximation failed #3')
				'''
				x_new3 = list(x)
				exp_new3 = list(experiment)
				del(x_new3x_new3 = list(x)
				exp_new3 = list(experiment)[(len(x_new3)-len(x_new)):])
				del(exp_new3[(len(exp_new3)-len(x_new)):])
				i=0
				while i<len(x):
					exp_new3[i]=exp_new3[i]-p1*np.exp(-D1*x[i])-p2*np.exp(-D2*x[i])
					i+=1
				popt, pcov = curve_fit(func3, x_new3, exp_new3) 
				'''
				break
			del(x_new3[0])
			del(exp_new3[0])
	print(len(x_new3), 'x_new3')
	perr3=perr[0]
	perr3p=perr[1]
	D3, p3 = popt

print(D1,D2,D3, 'D ',p1,p2,p3,'p')
print(perr1, perr2, perr3, 'perr')
plt.ylabel("experiment") #Обозначем оси
plt.semilogy()
plt.xlabel('x')
plt.grid()

format1=str('data.txt')
file_name = NAME+format1
file1 = open(file_name,"w") 
file1.write(str(D1))
file1.write(' D1 +-')
file1.write(str(perr1))
file1.write(' ,\n')
file1.write(str(p1))
file1.write(' p1 +-')
file1.write(str(perr1p))
file1.write('\n')
file1.write(str(D2))
file1.write(' D2 +-')
file1.write(str(perr2))
file1.write(' ,\n')
file1.write(str(p2))
file1.write(' p2 +- ')
file1.write(str(perr2p))
file1.write('\n')
file1.write(str(D3))
file1.write(' D3 +-')
file1.write(str(perr3))
file1.write(' ,\n')
file1.write(str(p3))
file1.write(' p3 +-')
file1.write(str(perr3p))
file1.write('\n \n \n')

i=0
while i<len(experiment):
	file1.write(str(x[i]))
	file1.write(' ')
	file1.write(str(experiment[i]))
	file1.write('\n')
	i+=1
file1.close()

plt.scatter(x, experiment, s=10, color='black') #Выводим массив точек на график
plt.scatter(x_new, exp_new, s=10, color='blue')
plt.scatter(x_new2, exp_new2, s=10, color='orange')
plt.scatter(x_new3, exp_new3, s=10, color='green')
y_sum_m=[]
i=0
while i<len(x):
	y_sum=p1*np.exp(-D1*x[i])+ p2*np.exp(-D2*x[i])+ p3*np.exp(-D3*x[i])
	y_sum_m.append(y_sum)
	i+=1
plt.scatter(x, y_sum_m, s=10, color='red', label='sum')
x_new=np.array(x_new)
popt=D1,p1
plt.plot(x_new, func1(x_new, *popt), label='1')
x_new2=np.array(x_new2)
popt=D2, p2
plt.plot(x_new2, func2(x_new2, *popt), label='2')
x_new3=np.array(x_new3)
popt=D3, p3
plt.plot(x_new3, func3(x_new3, *popt), label='3')
plt.title(NAME_list)
plt.legend(loc='best')
plt.savefig(NAME_png)

#gradient = np.arange(0, 180, 1)  #делаем функцию гладкой
#plt.plot(gradient, experiment) #Рисуем гладкую аппроксимирующую функцию
plt.show()
