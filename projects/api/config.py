import os, sys, hashlib;

from api.process import Process;

class Config():
    def __init__(self, path):
        self.directory = os.path.dirname( path );
        self.path = path;
        self.realpath = path;
        if os.path.islink(self.path):
            self.realpath = os.path.realpath( self.path );
        self.lines = [];
        self.comment = "#";

    def open(self):
        with open(self.path, "r") as f:
            self.lines = f.readlines();
            for i in range(len(self.lines)):
                self.lines[i] = self.lines[i].rstrip();
    def clear(self):
        self.lines = [];

    def add(self, line):
        self.lines.append(line);

    def equal(self, path):
        if not os.path.exists(path):
            return False;
        texto = "";
        with open(self.path, "w") as f:
            for line in self.lines:
                texto += line + os.linesep;
        return hashlib.md5( texto.encode() ).hexdigest() == hashlib.md5( open( path, "r" ).read().encode() ).hexdigest();

    def save(self):
        is_blocked_file = self.isblock();
        if is_blocked_file:
            self.unblock();
        with open(self.path, "w") as f:
            for line in self.lines:
                f.write( line + os.linesep );
        #if is_blocked_file:
        #    self.block();
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
            if self.lines[i][:1].strip() == self.comment:
                continue;
            partes = self.lines[i].strip().split(" ");
            if partes[0] == key:
                self.lines[i] = self.comment + self.lines[i].strip(); 

    def uncomment(self, key):
        for i in range(len(self.lines)):
            if self.lines[i][:1].strip() != self.comment:
                continue;
            partes = self.lines[i].strip()[1:].split(" ");
            if partes[0] == key:
                self.lines[i] = self.lines[i].strip()[1:]; 
    
    def isblock(self):
        p = Process("lsattr " + self.realpath );
        output = p.run();
        return output[:22].find("i");
    
    def block(self):
        p = Process("chattr +i " + self.realpath);
        output = p.run();
        return self.isblock();

    def unblock(self):
        p = Process("chattr -i " + self.realpath);
        output = p.run();
        return not self.isblock();
