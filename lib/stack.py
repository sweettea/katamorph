
class Stack:
    """
    A class representing a whole array of block devices with an
    optional filesystem on top. Th"""
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'path' in kwargs:
            self.path = kwargs['path'] 
        
        self.path = "/dev/mapper/" + self.name

