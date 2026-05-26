import os, json, sys;

class ConfigProject():
    def __init__(self, project, log=None):
        self.log = log;
        self.js_var = {};
        self.project = project;
        self.PATH_VAR = "/var/kfm/" + self.project + "/config.json";
        self.PATH_OPT = "/opt/kfishmonger/projects/" + self.project + "/resources/config.json";
        if not os.path.exists("/var/kfm/" + self.project):
            os.makedirs("/var/kfm/" + self.project);
            if self.log != None:
                self.log.info("Criando o diretório /var/kfm/" + self.project);
    
    def copy(self):
        js_opt = {};
        self.js_var = {};
        if os.path.exists( self.PATH_OPT ):
            js_opt = json.loads(open( self.PATH_OPT ,"r").read());
        if os.path.exists(self.PATH_VAR):
            self.js_var = json.loads(open(self.PATH_VAR,"r").read());
        for key in js_opt:
            if self.js_var.get( key ) == None:
                self.js_var[key] = js_opt[key];
        self.save();
    
    def save(self):
        with open(self.PATH_VAR,"w") as f:
            f.write( json.dumps( self.js_var ) );
            if self.log != None:
                self.log.info("Configuração salva em: " + self.PATH_VAR);

    def load(self):
        self.js_var = json.loads(open(self.PATH_VAR,"r").read());
        for key in self.js_var:
            setattr(self, key, self.js_var[key]);
        
def main():
    c = ConfigProject("vpn");
    c.load();
    print( c.oui );
if __name__ == "__main__":
    main();