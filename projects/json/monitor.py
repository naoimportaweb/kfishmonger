import sys, os, shutil, inspect, traceback, time;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname( CURRENTDIR );
sys.path.append(ROOT);

from api.process import Process;

def callback(process, retorno):
    print(retorno);
def main():
    while True:
        try:
            files = os.listdir( CURRENTDIR + "/sub");
            for file in files:
                p = Process( "python3 " + CURRENTDIR + "/sub/" + file );
                if not p.exists():
                    p.asThread(callback);
        except:
            traceback.print_exc();
        finally:
            time.sleep(30);

if __name__ == "__main__":
    main();



