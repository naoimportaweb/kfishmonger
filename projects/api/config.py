import os, sys;

class Config():
    def __init__(self, path):
        self.directory = os.path.dirname( path );
        self.path = path;
        self.lines = [];
        self.comment = "#";

    def open(self):
        with open(self.path, "r") as f:
            self.lines = f.readlines();
            for i in range(len(self.lines)):
                self.lines[i] = self.lines[i].rstrip();

    def save(self):
        with open(self.path, "w") as f:
            for line in self.lines:
                f.write( line + os.linesep );

    def findattribute(self, attribute):
        for line in self.lines:
            if line.strip().lower().find(attribute.lower()) == 0:
                return line;
        return None;

    def addattribute(self, attribute):
        self.lines.append( attribute );

