import os, sys, json, traceback, inspect;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname( CURRENTDIR );
sys.path.append(ROOT);

from api.process import Process;
from api.database import Database;








#db = ClientDatabase("teste");
#esquema = {"table" : "cliente", "fields" : [ 
#    {"name" : "id", "type" : "TEXT", "pk" : True},
#    {"name" : "nome", "type" : "TEXT", "pk" : False},
#    {"name" : "path3", "type" : "TEXT", "pk" : False} ]};
#
#retorno = db.schema( esquema );
#print( retorno );
#
#insert = db.execute("INSERT INTO cliente (id, nome) values(?, ?)", ["98jhjyghh7", "arquivo"]);
#print(insert);
#
#table = db.datatable( "SELECT * FROM cliente where id = ?" , ["aaaa"] );
#for row in table:
#    print( row );
