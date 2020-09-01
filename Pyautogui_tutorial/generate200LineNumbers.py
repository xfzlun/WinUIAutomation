# 生成1-200，并且换行的数列到剪贴簿中备用
import pyperclip
numbers = ''  #新建一个空字符串
for i in range(1, 200):
    numbers = numbers + str(i) + '\n'    #产生1-200的数字
pyperclip.copy(numbers)  #把1-200的数列拷贝到剪贴簿待会可以贴到文件中
