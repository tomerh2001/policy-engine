class boolConverter:
    regex = 'false|False|True|true|0|1'

    def to_python(self, value):
        if value.lower() == 'false':
            return False
        elif value.lower() == 'true':
            return True
        else:
            return bool(int(value))
    def to_url(self, value):
        return str(value)