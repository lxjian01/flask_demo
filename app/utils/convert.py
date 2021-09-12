
class Convert:

    @staticmethod
    def to_bool(value):
        if type(value) is bool:
            return value
        if value.lower() == "true" or value == "1":
            return True
        elif value.lower() == "false" or value == "0":
            return False
        else:
            raise Exception("Value is not a bool.")