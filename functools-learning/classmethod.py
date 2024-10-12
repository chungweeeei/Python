

'''
    NOTE
    classmethod use cls bind function itself on the class object, so it can call the member in the class object via cls
    staticmethod only can operate the input arguments. 
'''

from datetime import date
# random Person
class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    @classmethod
    def fromBirthYear(cls, name, birthYear):
        
        '''
            NOTE 
            return cls(name, date.today().year - birthYear) is equivalent to Person(name, date.today().year - birthYear)
        '''
        
        return cls(name, date.today().year - birthYear)

    def display(self):
        print(self.name + "'s age is: " + str(self.age))
        
if __name__ == "__main__":
    
    person = Person('Adam', 19)
    person.display()

    person1 = Person.fromBirthYear('John',  1985)
    person1.display()
