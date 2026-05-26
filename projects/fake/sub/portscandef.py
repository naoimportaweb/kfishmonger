#!/usr/bin/env python
import socket, sys, time, os, subprocess, signal, optparse, traceback, inspect;
from struct import *
from collections import OrderedDict

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR));
sys.path.append(ROOT);
sys.path.append(ROOT + "/panicroom/");

from api.log import Log;
from api.CONST import *;
from api.panicroomclient import PanicRoomClient;

log = Log("fake_port_scan");
panicroom = PanicRoomClient();

class bgcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

global threewayhandshake, waiting, fullscandb, halfscandb, xmasscandb, nullscandb, finscandb, scannedports, blacklist, stop, IGNORE_IP_SCAN;

blacklist = []
fullscandb = {}
halfscandb = {}
xmasscandb = {}
nullscandb = {}
finscandb = {}
waiting = []
threewayhandshake = []
scannedports = {}
stop = False;
IGNORE_IP_SCAN = ["127.0.0.1"];

def convert(dec):
    final = []
    flags = OrderedDict([("128","CWR"),("64","ECE"),("32","URG"),("16","ACK"),("8","PSH"),("4","RST"),("2","SYN"),("1","FIN")])
    for i in flags.keys():
        if(dec>=int(i)):
            dec = dec-int(i)
            final.append(flags[i])
    return final

def show_ports(signum,frm):
    global stop;
    for ips in scannedports:
        for single in scannedports[ips]:
            while(scannedports[ips].count(single)!=1):
                scannedports[ips].remove(single);
    print ("\n\n");
    for ip in blacklist:
        print ("Ataque do IP", ip, "portas escaneadas: "+ ",".join( scannedports[ip] ) );
    stop = True;

def threewaycheck(sip,dip,sport,dport,seqnum,acknum,flags):
    data = sip+":"+str(sport)+"->"+dip+":"+str(dport)+"_"+str(seqnum)+"_"+str(acknum)+"_"+"/".join(flags);
    if("SYN" in flags and len(flags)==1):
        if(seqnum>0 and acknum==0):
            waiting.append(str(seqnum)+"_"+str(acknum)+"_"+sip+":"+str(sport)+"->"+dip+":"+str(dport));
    elif("SYN" in flags and "ACK" in flags and len(flags)==2):
        for i in waiting:
            pieces = i.split("_");
            ack_old = pieces[1];
            seq_old = pieces[0];
            if(acknum==int(seq_old)+1):
                del waiting[waiting.index(i)];
                waiting.append(str(seqnum)+"_"+str(acknum)+"_"+sip+":"+str(sport)+"->"+dip+":"+str(dport));
                break;

    elif("ACK" in flags and len(flags)==1):
        for i in waiting:
            pieces = i.split("_");
            ack_old = pieces[1];
            seq_old = pieces[0];
            if(seqnum==int(ack_old) and acknum==int(seq_old)+1):
                index_i = waiting.index(i);        
                del waiting[index_i];
                threewayhandshake.append(sip + ":" + str(sport) + "->" + dip + ":" + str(dport)); # Fez um ACK          
                break

def scancheck(sip,dip,sport,dport,seqnum,acknum,flags):
    global data, dataforthreewaycheck, dbdata, reverse;
    data = sip + ":" + str(sport) + "->" + dip + ":" + str(dport) + "_" + str(seqnum) + "_" + str(acknum) + "_" + "/".join(flags);
    dataforthreewaycheck = sip + ":" + str(sport) + "->" + dip + ":" + str(dport);
    revthreeway = dip + ":" + str(dport) + "->" + sip + ":" + str(sport);
    dbdata =  sip + "->" + dip;
    reverse = dip + "->" + sip;

    if dport in IGNORE_PORT_SCAN or sip in IGNORE_IP_SCAN:
        return;
    
    returned = halfconnectscan(sip, dip, sport, dport, seqnum, acknum, flags);
    if returned:
        if(isinstance(returned,(str))):
            print( returned ); # HALF CONNECTION DETECTADO
            panicroom.send_alert("ALERT", "Conexão HALF realizada.");
            log.info(returned);
        else:
            print (bgcolors.BOLD + bgcolors.OKBLUE + revthreeway + bgcolors.ENDC); # Tentativa de conexão em uma porta fechada
            panicroom.send_alert("ALERT", "Tentativa de conexão em uma porta fechada.");
        return;
    returned = fullconnectscan(sip,dip,sport,dport,seqnum,acknum,flags)
    if returned:
        if(isinstance(returned,(str))):
            print(returned); #conexãso bem sucedida, FULL CONNECT 
            panicroom.send_alert("ALERT", "Conexão FULL realizada.");
            log.info(returned);
        else:
            print(bgcolors.BOLD + bgcolors.OKBLUE + revthreeway + bgcolors.ENDC); # Tentativa de conexão em uma porta fechada
            panicroom.send_alert("ALERT", "Tentativa de conexão em uma porta fechada.");
        return;
    returned = xmasscan(sip,dip,sport,dport,seqnum,acknum,flags);
    if returned:
        print(bgcolors.BOLD + bgcolors.OKBLUE + dataforthreewaycheck + bgcolors.ENDC); # Detectado XMAS
        panicroom.send_alert("ALERT", "Tentativa de conexão XMAS.");
        log.info(returned);
        return;
    returned = finscan(sip,dip,sport,dport,seqnum,acknum,flags);
    if returned:
        print(bgcolors.BOLD + bgcolors.OKBLUE + dataforthreewaycheck + bgcolors.ENDC); # Detectado o FIM
        panicroom.send_alert("ALERT", "Tentativa de conexão FIN.");
        log.info(returned);
        return;
    returned = nullscan(sip,dip,sport,dport,seqnum,acknum,flags);
    if returned:
        print(bgcolors.BOLD + bgcolors.OKBLUE + dataforthreewaycheck + bgcolors.ENDC); #Detectado o NULL scan
        panicroom.send_alert("ALERT", "Tentativa de conexão NULL.");
        log.info(returned);
        return;

def fullconnectscan(sip,dip,sport,dport,seqnum,acknum,flags):
    if(scannedports.get(dip)):
        scannedports[dip].append(str(sport))
    else:
        scannedports[dip] = []
        scannedports[dip].append(str(sport))
    
    if(dataforthreewaycheck in threewayhandshake):
        if("ACK" in flags and "RST" in flags and len(flags)==2):
            if(fullscandb.get(dbdata)):
                counter = int(fullscandb[dbdata])
                if(counter>=3):
                    
                    if(str(dip) not in blacklist):
                        blacklist.append(str(dip))
                    return bgcolors.BOLD + bgcolors.OKBLUE + dip + ":" + str(dport) + "->" + sip + ":" + str(sport) + bgcolors.ENDC; #conexãso bem sucedida, FULL CONNECT              
                else:
                    counter = counter + 1
                    fullscandb[dbdata] = str(counter)
            else:
                counter = 0
                fullscandb[dbdata] = str(counter)
                
    else:
        if("SYN" in flags and len(flags)==1):
            if(seqnum>0 and acknum==0):
                fullscandb[dbdata+"_SYN"] = str(seqnum)+"_"+str(acknum)+"_"+str(sport)+"_"+str(dport)
                
        elif("RST" in flags and "ACK" in flags and len(flags)==2):
            if(fullscandb.get(dip+"->"+sip+"_SYN")):
                manage = fullscandb[dip+"->"+sip+"_SYN"]
                pieces = manage.split("_")
                old_acknum = int(pieces[1])
                old_seqnum = int(pieces[0])
                if(seqnum==0 and acknum==old_seqnum+1):
                    if(fullscandb.get(dbdata)):
                        counter = int(fullscandb[dbdata])
                        if(counter>=3):
                            
                            if(str(dip) not in blacklist):
                                blacklist.append(str(dip))
                            return True
                        else:
                            counter = counter + 1
                            fullscandb[dbdata] = str(counter)
                    else:
                        counter = 0
                        fullscandb[dbdata] = str(counter)
    return False            

def halfconnectscan(sip,dip,sport,dport,seqnum,acknum,flags):
    if(scannedports.get(dip)):
        scannedports[dip].append(str(sport))
    else:
        scannedports[dip] = []
        scannedports[dip].append(str(sport))
    
    if("SYN" in flags and seqnum>0 and acknum==0 and len(flags)==1):
        halfscandb[dbdata+"_"+str(seqnum)] = dbdata+"_SYN_ACK_"+str(seqnum)+"_"+str(acknum)
    elif("RST" in flags and "ACK" in flags and len(flags)==2):
        if(halfscandb.get(reverse+"_"+str(acknum-1))):
            del halfscandb[reverse+"_"+str(acknum-1)]
            if(str(dip) not in blacklist):
                blacklist.append(str(dip))
            return True    
    elif("SYN" in flags and "ACK" in flags and len(flags)==2):
        if(halfscandb.get(reverse+"_"+str(acknum-1))):
            del halfscandb[reverse+"_"+str(acknum-1)]
            halfscandb[reverse+"_"+str(acknum)] = dbdata+"_RST_"+str(seqnum)+"_"+str(acknum)
    elif("RST" in flags and len(flags)==1):
        if(halfscandb.get(dbdata+"_"+str(seqnum))):
            if(str(dip) not in blacklist):
                blacklist.append(str(dip))
            return bgcolors.BOLD + bgcolors.OKBLUE + sip + ":" + str(sport) + "->" + dip + ":" + str(dport) + bgcolors.ENDC; # HALF CONNECTION DETECTADO
    return False

def xmasscan(sip,dip,sport,dport,seqnum,acknum,flags):
    if(scannedports.get(dip)):
        scannedports[dip].append(str(sport))
    else:
        scannedports[dip] = []
        scannedports[dip].append(str(sport))
    
    if("FIN" in flags and "URG" in flags and "PSH" in flags and len(flags)==3):
        
        if(str(sip) not in blacklist):    
            blacklist.append(str(sip))
        return True
    return False

def finscan(sip,dip,sport,dport,seqnum,acknum,flags):
    if(scannedports.get(dip)):
        scannedports[dip].append(str(sport))
    else:
        scannedports[dip] = []
        scannedports[dip].append(str(sport))
    
    if(dataforthreewaycheck not in threewayhandshake):
        if("FIN" in flags and len(flags)==1):            
            if(str(sip) not in blacklist):    
                blacklist.append(str(sip))
            return True
    return False

def nullscan(sip,dip,sport,dport,seqnum,acknum,flags):
    if(scannedports.get(dip)):
        scannedports[dip].append(str(sport))
    else:
        scannedports[dip] = []
        scannedports[dip].append(str(sport))
    if(len(flags)==0):
        if(str(sip) not in blacklist):    
            blacklist.append(str(sip))
        return True
    return False

def ackscan(sip,dip,sport,dport,seqnum,acknum,flags):
    if(scannedports.get(dip)):
        scannedports[dip].append(str(sport))
    else:
        scannedports[dip] = []
        scannedports[dip].append(str(sport))

    if(dataforthreewaycheck not in threewayhandshake):
        if("ACK" in flags and len(flags)==1):
            
            if(str(sip) not in blacklist):    
                blacklist.append(str(sip))
            return True
    return False

def main():
    global stop;
    try:
        s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003));
    except KeyboardInterrupt:
        print("Fechando a aplicação.");
        sys.exit(0);
      
    now = time.time();
    protocol_numb = {"1":"ICMP","6":"TCP","17":"UDP"}

    while True:
        try:
            if stop:
                break;
            try:
                packet = s.recvfrom(65565);
                packet = packet[0];
                eth_length = 14;
                eth_header = packet[:eth_length];
                eth = unpack('!6s6sH' , eth_header);
                eth_protocol = socket.ntohs(eth[2]);
            except KeyboardInterrupt:
                print("Fechando a aplicação.");
                break;
            except:
                time.sleep(1);
                continue;

            if eth_protocol == 8 :
                ip_header = packet[eth_length:20+eth_length];
              
                iph = unpack('!BBHHHBBH4s4s' , ip_header);
         
                version_ihl = iph[0];
                version = version_ihl >> 4;
                ihl = version_ihl & 0xF;
         
                iph_length = ihl * 4;
                protocol = iph[6];
                if(str(iph[6]) not in protocol_numb.keys()):
                    protocol_name = str(iph[6]);
                else:
                    protocol_name = protocol_numb[str(iph[6])];
                s_addr = socket.inet_ntoa(iph[8]);
                d_addr = socket.inet_ntoa(iph[9]);
                timestamp = time.time();
                elave=None;
              
                #TCP protocol
                if protocol == 6 :
                    t = iph_length + eth_length;
                    tcp_header = packet[t:t+20];
                    tcph = unpack('!HHLLBBHHH' , tcp_header);
           
                    source_port = tcph[0];
                    dest_port = tcph[1];
                    seq_numb = tcph[2];
                    dest_numb = tcph[3];
                    tcp_flags = convert(tcph[5]);
                    testdata = s_addr+":"+str(source_port)+"->"+d_addr+":"+str(dest_port);
                    if(testdata not in threewayhandshake):
                        threewaycheck(s_addr,d_addr,source_port,dest_port,seq_numb,dest_numb,tcp_flags);
                    scancheck(s_addr,d_addr,source_port,dest_port,seq_numb,dest_numb,tcp_flags);
                try:
                    signal.signal(signal.SIGINT,show_ports);    
                except KeyboardInterrupt:
                    print("Fechando a aplicação.");
                    break; 
                except:
                    traceback.print_exc();
        except KeyboardInterrupt:
            print("Fechando a aplicação.");
            sys.exit(1);
        except:
            traceback.print_exc();

if __name__ == "__main__":
    main();

