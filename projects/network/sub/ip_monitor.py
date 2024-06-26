    # Versao futura implementar isso em uma thread
    #db = ClientDatabase("connections");
    #esquema = {"table" : "requests", "fields" : [  {"name" : "ip", "type" : "TEXT", "pk" : True}, {"name" : "risk", "type" : "INT", "pk" : False}, {"name" : "info", "type" : "TEXT", "pk" : False} ]};
    #db.schema( esquema );
    #while True:
    #    try:
    #        #print("Count (IP requests):", len(db.datatable( "SELECT * FROM requests", [])));
    #        process = Process("netstat -tn 2>/dev/null");
    #        linhas = process.run().split("\n");
    #        for linha in linhas:
    #            ip_candidates = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", linha)
    #            if len(ip_candidates) < 2 or ip_candidates[1] == "127.0.0.1":
    #                continue;
    #            if len(db.datatable( "SELECT * FROM requests where ip = ?" , [ ip_candidates[1] ] )) == 0:
    #                db.execute("INSERT INTO requests (ip, risk, info) values(?, ?, ?)", [ip_candidates[1], 0, ""]);
    #    except KeyboardInterrupt:
    #        sys.exit(0);
    #   except:
    #        traceback.print_exc();
    #    finally:
    #        time.sleep(30);