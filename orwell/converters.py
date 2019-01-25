class DigestConverter:
    regex = '\w{64}'

    def to_python(self, value):
        return str(value)