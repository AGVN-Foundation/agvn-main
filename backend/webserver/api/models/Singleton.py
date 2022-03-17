'''
    Class used for Singleton Pattern.

    Credit: 
    Goutom Roy
    https://gist.github.com/goutomroy/c925b1316bd9e7ec2cf9b1e4c183f5f4#file-singleton-py
    https://betterprogramming.pub/singleton-in-python-5eaa66618e3d
'''

class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)