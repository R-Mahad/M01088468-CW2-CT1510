class Student:
    def __init__(self,MISIS,stdName,mark):
        self.__MISIS = MISIS
        self.__stdName =stdName
        self.__mark = mark
    
    def __str__(self):
        return f'Student info: {self.__MISIS},{self.__stdName},{self.__mark}'
    def result(self):
        if self.__mark > 40:
            return (f'{self.__stdName} is Passed')
        else:
            return (f'{self.__stdName} is Failed')
std3 = Student("M0122", "Saeed", 39)     
std1= Student("M0101", "Ali", 79)
std2= Student("M0111", "Bader", 80)
print(std1.result() )
print(std2.result() )
print(std3.result)


