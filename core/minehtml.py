import sys
from io import StringIO
from re import match

class MimePart(object):

    def __init__(self, content="", **headers):
        self.headers = headers
        self.content = content

    @classmethod
    def parse_file(cls, filename):
        with open(filename, "r") as fp:
            part = cls()
            part.parse(fp)
            return part

    @classmethod
    def parse_string(cls, string):
        buf = StringIO(string)
        part = cls()
        part.parse(buf)
        return part

    def parse(self, reader):
        while True:
            line = reader.readline().strip()
            if len(self.headers) > 0 and not line:
                self.content = reader.read()
                break
            header, value = map(str.strip, line.split(":", 1))
            value = [value]
            if value[0].endswith(";"):
                value[0] = value[0][:-1]
                line = reader.readline().strip()
                while line.endswith(";"):
                    value.append(line[:-1])
                    line = reader.readline().strip()
                value.append(line)
            self.headers[header] = value


class MimeHtmlParser(MimePart):

    def __init__(self, content="", **headers):
        self.content = content
        self.parts = []
        super(MimeHtmlParser, self).__init__(content, **headers)

    def get_boundary(self):
        content_type = self.headers["Content-Type"]
        for field in content_type:
            matchstr = match("boundary=\"(.+?)\"", field)
            if matchstr:
                return "--" + matchstr.group(1)

    def parse(self, reader):
        super(MimeHtmlParser, self).parse(reader)
        boundary = self.get_boundary()
        if not boundary:
            sys.exit(1)
        start = False
        part_content = ""
        for line in self.content.splitlines():
            line = line.strip()
            if line == boundary:
                if start and part_content:
                    self.parts.append(MimePart.parse_string(part_content))
                part_content = ""
                start = True
                continue
            else:
                part_content += line + "\n"

    def __repr__(self):
        return "<{0}(filename='{1}')>".format(self.__class__.__name__, self.filename)
