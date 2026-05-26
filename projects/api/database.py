import sqlite3, json, traceback, socket

class Database:
    def __init__(self, name):
        self.name = name;
        self.DIR_SQLITE = "/var/kfm/db/"+ name +".db"
        self.conn_sql = sqlite3.connect( self.DIR_SQLITE, check_same_thread=False );
        self.conn_sql.row_factory = sqlite3.Row

    def execute(self, sql, values):
        try:
            cur = self.conn_sql.cursor();
            cur.execute(sql, values);
            self.conn_sql.commit();
            return cur.lastrowid;
        except KeyboardInterrupt:
            sys.exit(0);
        except:
            traceback.print_exc();
        return -1;

    def datatable(self, sql, values):
        try:
            cursor = self.conn_sql.cursor();
            cursor.execute(sql, values);
            rows = cursor.fetchall();
            return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON
        except KeyboardInterrupt:
            sys.exit(0);
        except:
            traceback.print_exc();
        return [];

    def schema(self, schema_json):
        columns = [];
        cursor = self.conn_sql.execute("select name, type from pragma_table_info('"+ schema_json["table"] +"');");
        for row in cursor:
            columns.append( { "name" : row[0], "type" : row[1] } );
        if len(columns) == 0:
            sql = "CREATE TABLE " + schema_json["table"]  + "(";
            for i in range(len(schema_json["fields"])):
                field = schema_json["fields"][i];
                sql += " " + field["name"] + " " + field["type"];
                if field["pk"]:
                    sql += " PRIMARY KEY     NOT NULL ";
                if i < len(schema_json["fields"]) - 1:
                    sql += ", ";
            sql += ");";
            self.conn_sql.execute(sql);
        else:
            for row in schema_json["fields"]:
                match = next((d for d in columns if d['name'] == row["name"]), None )
                if match == None:
                    sql = "ALTER TABLE "+ schema_json["table"] +" ADD "+ row["name"] +" "+ row["type"] +";"
                    self.conn_sql.execute(sql);
        return columns;

class ClientDatabase():
    def __init__(self, database):
        self.database = database;
        self.HOST = "127.0.0.1";
        self.PORT = 20001;
    
    def execute(self, sql, values):
        js = {"method" : "insert", "database" : self.database, "sql" : sql, "values" : values};
        return self.__send__( js );
    
    def datatable(self, sql, values):
        js = {"method" : "select", "database" : self.database, "sql" : sql, "values" : values};
        return json.loads(self.__send__( js ));
    
    def schema(self, schema_json):
        js = {"method" : "schema", "database" : self.database, "schema" : schema_json};
        return self.__send__( js );
    
    def __send__(self, js):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT));
            dados = "00000000000000000000" + json.dumps(js);
            s.sendall( dados.encode() );
            return json.loads( s.recv(40960) );
        return None;
