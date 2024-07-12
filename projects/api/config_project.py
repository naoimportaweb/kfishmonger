import os, json, sys;

class ConfigProject():
    def __init__(self, project, log=None):
        self.log = log;
        self.project = project;
        if not os.path.exists("/var/kfm/" + self.project):
            os.makedirs("/var/kfm/" + self.project);
            if self.log != None:
                self.log.info("Criando o diretório /var/kfm/" + self.project);
    def copy(self):
        js_opt = {};
        js_var = {};
        if os.path.exists( "/opt/kfishmonger/projects/" + self.project + "/resources/config.json" ):
            js_opt = json.loads(open("/opt/kfishmonger/projects/" + self.project + "/resources/config.json","r").read());
        if os.path.exists("/var/kfm/" + self.project + "/resources/config.json"):
            js_var = json.loads(open("/var/kfm/" + self.project + "/resources/config.json","r").read());
        for key in js_opt:
            if js_var.get( key ) == None:
                js_var[key] = js_opt[key];
        with open("/var/kfm/" + self.project + "/resources/config.json","w") as f:
            f.write( json.dumps( json_var ) );
            if self.log != None:
                self.log.info("Configuração salva em: /var/kfm/" + self.project + "/resources/config.json");
