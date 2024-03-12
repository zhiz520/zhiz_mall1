# Define user name rules
from atexit import register
from sqlite3 import register_converter


class UsernameConverter:
    regex = r'^[a-zA-Z0-9_-]{4,15}$'

    def to_python(self, value):
        return value
    
# register_converter('username', UsernameConverter)