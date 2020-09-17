
'''
根据输入的参数，转成对应的keycode
1. 输入键盘按键
2. 查找hid_key_value.txt
3. 匹配对应的字母或是单词
4， 切分对应的字符串
5. 用with open
'''
def keyexchange(strings):
    with open("WInAutomation/hid_key_value.txt", "r") as fp:
        lines = fp.readlines()
        dict = {}
        for line in lines:
            line = line.strip('\n')
            ddict = line.split('<-->')
            dict[ddict[1]] = ddict[0]
    char = list(strings)
    print(char)
    keycode = []
    for i in char:
        keycode.append(dict[i])
        #print(keycode)
    #keycode = dict[string]
    return keycode

a = keyexchange("abcdefghijkl")
print(a)
print(type(a))



