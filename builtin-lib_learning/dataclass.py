from dataclasses import dataclass

@dataclass(frozen=False)
class User:
    id: int
    name: str
    
@dataclass(frozen=True)
class TestUser:
    id: int
    name: str
    
if __name__ == "__main__":
    
    user = User(id=0, name="Test0")
    print("user: {}".format(user))
    
    user.id = 1
    user.name = "Test1"
    print("user: {}".format(user))
    
    test_user = TestUser(id=0, name="Test0")
    print("test_user: {}".format(test_user))
    
    '''
        NOTE
        Creating a dataclass with (frozen=True) means its instances are frozen and cannot be changed.
    '''
    
    try:
        test_user.name = "Test1"
    except Exception as e:
        print("[ERROR] e: {}".format(e))