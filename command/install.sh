#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root/Por favor, execute como root"
  exit
fi

DIR=/opt/kfishmonger
# Url do projeto em desenvolvimento
URL='https://codeload.github.com/naoimportaweb/kfishmonger/zip/refs/heads/main'
# Url da ultima versao estavel e testada no Debian e Ubuntu.
#URL='https://sourceforge.net/projects/kfishmonger/files/latest/download'
install(){
        if [ -f /tmp/kfishmonger.zip ] ; then
            rm /tmp/kfishmonger.zip
        fi
        wget -O /tmp/kfishmonger.zip ${URL}
        if [ -d /tmp/kfishmonger-main/ ] ; then
            rm -r /tmp/kfishmonger-main
        fi
        unzip /tmp/kfishmonger.zip -d /tmp/
        cp -r /tmp/kfishmonger-main/* ${DIR}
        if [ -L /bin/kfm ] ; then
            rm /bin/kfm
        fi
        chmod +x ${DIR}/command/kfm.sh
        ln -s ${DIR}/command/kfm.sh /bin/kfm
        /bin/kfm -c install
}

apt install update -y
apt install python3-pip -y
apt install unzip -y
apt install python3-netifaces -y
apt install conky -y
apt install jp -y
apt install dnscrypt-proxy -y
apt install proxychains -y
apt install tor -y
apt install openvpn -y

touch /etc/pip.conf
echo '[global]' > /etc/pip.conf
echo 'break-system-packages = true' >> /etc/pip.conf

pip3 install netifaces
pip3 install netifaces
pip3 install psutil
pip3 install pycryptodome
pip3 install Pysocks
pip3 install socks

if [ -L ${DIR} ] ; then
    echo "O diretório ${DIR} nao pode ser usado pois é um link simbólico."
    exit 0
fi

apt install unzip

if [ -d ${DIR} ] ; then
    echo 'O diretório já existe, deseja continuar (y|n)?:'
    read OPCAO
    if [ $OPCAO = "y" ] ; then
        install
    else
        exit 0
    fi
else
    mkdir ${DIR}
    install
fi