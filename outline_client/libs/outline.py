from client.libs.base import Entity


class Outline(Entity):
    """Sample object"""

    def struct_content():
        """Structure content"""

    def format_content():
        """Format content"""

    def typeof(string):
        """Returns type of string, specifically for outline structures, as a
        three-element tuple specifying (type, upper_or_lower, value,
        delimiter)

        Example
        -------
        ('number', None, 1, '.')
        ('roman numeral', 'upper', 3, ')')
        """
