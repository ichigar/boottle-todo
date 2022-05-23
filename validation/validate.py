class Validate:
    def __init__(selv, value):
        self._value = value
        
    def not_empty(self):
        return self._value != ''
