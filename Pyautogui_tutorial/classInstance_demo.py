# coding:utf-8
class Horse(object):
    variety = "大辕马"  #是Horse类的变量，可以通过Horse.variety在类的内部或者外部任意位置被访问
    '''    
    #__init__函数是Horse类的实例对象的构造函数，每次创建一个Horse类的实例对象时，这个函数均会被调用执行
    #其下以self.开头的变量是每个实例对象的成员变量，用来标记这个实例对象的属性以及特征使用的
    '''    
    def __init__(self, name = "green", height = "0.5", length = "1.3", sex= "male"):
        #self.name是成员变量，name是形参，局部变量
        self.name = name
        self.height = height
        self.length = length
        self.sex = sex
        print("A baby horse is born called", self.name)
    
    def print_into(self):
        print(self.name, self.height, self.length, self.sex, Horse.variety)
        Horse.print_variety() #这步是在对象方法里通过类调用类方法， 应该避免
        Horse().print_ci(200, 100) #对象调用静态方法
        Horse.print_ci(200,100) #类调用静态方法
    
    @classmethod  #修饰器，表示用修饰器修饰底下的pp函数
    def pp(cls):
        print(cls.variety, Horse.variety, cls.address) #Horse.variety是类使用类变量
        print(Horse().name)  #对象使用对象的成员变量
    '''
    修饰器@classmethod修饰的两个函数，pp & print_variety是类Horse的类函数，类函数只可以通过类或是cls调用
    在类的内部，类变量的使用需要前缀类名， 或是cls.
    我们可以在print语句中，看到cls.variety, 以及 Horse.variety
    '''
    @classmethod
    def print_variety(cls):
        cls.address = "xi'an"
        print("type", type(cls.address))  
        print(cls.variety, Horse.variety, cls.address)
        Horse.pp()  #类调用类方法
        Horse().print_ci(100,100)  #对象调用静态方法
    '''
    在类的内部，可以通过类调用类的方法函数  Horse.pp()
    '''    

    def print_info(self):
        print(self.name, self.height, self.length, self.sex, Horse.variety) #Horse.address)
        Horse.print_variety()

    @staticmethod
    def print_ci(x, y):
        print(x, y)
    '''
    用staticmathod修饰的print_ci函数是静态函数，它的第一个参数不是特殊的self或者cls，
    静态函数可以在类的内部，外部被调用，也可以被类的对象调用
    '''

a = Horse("xiaoxuanfeng")
b = Horse("pilhuo", sex = "female")
a.print_info()
b.print_info()
Horse.print_variety()
print("*" * 20)
Horse.pp() #类调用类方法
Horse.print_ci(12,23)  #类外类调用静态方法
a.print_ci(23,31)  #类外对象调用静态方法

