import os, sys, hashlib;

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
    
    def equal(self, path):
        if not os.path.exists(path):
            return False;
        texto = "";
        with open(self.path, "w") as f:
            for line in self.lines:
                texto += line + os.linesep;
        return hashlib.md5( texto.encode() ).hexdigest() == hashlib.md5( open( path, "r" ).read().encode() ).hexdigest();

    def save(self):
        with open(self.path, "w") as f:
            for line in self.lines:
                f.write( line + os.linesep );
    
    def saveas(self, path):
        with open(path, "w") as f:
            for line in self.lines:
                f.write( line + os.linesep );
    
    def findattribute(self, attribute):
        for line in self.lines:
            if line.strip().lower().find(attribute.lower()) == 0:
                return line;
        return None;

    def addattribute(self, attribute):
        self.lines.append( attribute );

    def replace(self, key, value):
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].replace(key, value);
    
    def commentattr(self, key):
        for i in range(len(self.lines)):
            if self.lines[i][:1].strip() == "#":
                continue;
            partes = self.lines[i].strip().split(" ");
            if partes[0] == key:
                self.lines[i] = "#" + self.lines[i].strip(); 
    def uncomment(self, key):
        for i in range(len(self.lines)):
            if self.lines[i][:1].strip() != "#":
                continue;
            partes = self.lines[i].strip()[1:].split(" ");
            if partes[0] == key:
                self.lines[i] = self.lines[i].strip()[1:]; 