import os, sys, subprocess, platform, netifaces;

class Distro():
    def name(self):
        distro_name = platform.version();
        if distro_name.find("Debian") > 0:
            return "debian";
        elif distro_name.find("Ubuntu") > 0:
            return "ubuntu";
        else:
            print("Nao foi possivel detectar.");
    
    def user(self):
        tags = ["SUDO_USER", "USERNAME", "USERNAME", "USER"];
        for tag in tags:
            if os.environ.get( tag ) != "" and os.environ.get( tag ) != "root":
                return os.environ.get( tag );

    def graphical(self):
        return self.__detect_desktop_environment__();
    
    def __detect_desktop_environment__(self):
        desktop_environment = 'gnome'
        if os.environ.get('KDE_FULL_SESSION') == 'true':
            desktop_environment = 'kde'
        elif os.environ.get('GNOME_SHELL_SESSION_MODE'):
            desktop_environment = 'gnome'
        else:
            try:
                info = subprocess.getoutput('xprop -root')
                if info.find("XFCE_DESKTOP_WINDOW") > 0:
                    desktop_environment = 'xfce'
            except (OSError, RuntimeError):
                pass
        return desktop_environment
    def interfaces(self):
        return netifaces.interfaces()
        
def main():
    d = Distro();
    print(d.name());
    print(d.graphical());

if __name__ == "__main__":
    main();

