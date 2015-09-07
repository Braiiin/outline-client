from client.libs.base import Entity
from roman import toRoman, fromRoman

class Outline(Entity):
    """Sample object"""

    def format_content(self):
        """Format content
        assumes that heading types do not repeat"""
        lines = self.content.split('\n')
        html = ''
        headings, depth, numbering = [None], 0, {0: 0}
        for line in lines:
            words, current_heading = line.strip().split(), headings[-1]
            heading, words = self.typeof(
                words[0], numbering.get(depth, 0)), words[1:]
            if heading != current_heading:
                if heading in headings:
                    depth = headings.index(heading)
                    headings = headings[:depth+1]
                    current_heading = heading
                else:
                    depth += 1
                    current_heading = heading
                    headings.append(heading)
                    numbering[depth] = 0
            numbering[depth] += 1
            html += '&nbsp;'*((depth-1)*4) + self.translate(heading, numbering[depth]) + heading[2] + ' ' +' '.join(words) + '<br>\n'
        self.html = html
        return self

    @staticmethod
    def typeof(string, i):
        """Returns type of string, specifically for outline structures, as a
        three-element tuple specifying (type, upper_or_lower, delimiter)

        Example
        -------
        ('number', None, '.')
        ('roman numeral', 'upper', ')')
        """
        delimiter, string = string[-1], string[:-1]
        try:
            i = int(string)
            return ('number', None, delimiter)
        except ValueError:
            upper_or_lower = 'upper' if string.isupper() else 'lower'
            if len(string) != 1 or (
                ord(string) in (105, 73) and i != 8):
                return ('roman numeral', upper_or_lower, delimiter)
            return ('letter', upper_or_lower, delimiter)

    @staticmethod
    def translate(heading, i):
        """Converts integer i to a string according to the header"""
        typeof = heading[0]
        if typeof == 'number':
            return str(i)
        if typeof == 'letter':
            if heading[1] == 'upper':
                return chr(i+65)
            return chr(i+96)
        if typeof == 'roman numeral':
            roman = toRoman(i)
            if heading[1] == 'lower':
                return roman.lower()
            return roman


    @property
    def time(self):
        """calculates time needed to read outline"""
        return len(self.content.split()) // 33
