#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root/Por favor, execute como root"
  exit
fi

DIR=/opt/kfishmonger
printf "Se deseja instalar a versão estável digite (e), caso queira instalar a versão teste digite (t):"
read OPCAO
if [ $OPCAO = "e" ] ; then
    URL='https://sourceforge.net/projects/kfishmonger/files/latest/download'
else
    URL='https://codeload.github.com/naoimportaweb/kfishmonger/zip/refs/heads/main'
fi

install(){
        if [ -f /tmp/kfishmonger.zip ] ; then
            rm /tmp/kfishmonger.zip
        fi
        wget -O /tmp/kfishmonger.zip ${URL}
        if [ -d /tmp/kfishmonger-main/ ] ; then
            rm -r /tmp/kfishmonger-main
        fi
        unzip -qq /tmp/kfishmonger.zip -d /tmp/
        cp -r /tmp/kfishmonger-main/* ${DIR}
        if [ -L /bin/kfm ] ; then
            rm /bin/kfm
        fi
        chmod +x ${DIR}/command/kfm.sh
        ln -s ${DIR}/command/kfm.sh /bin/kfm
        /bin/kfm -c install
}

existspackage(){
    retorno="`apt-cache show $1`"
    SUB='No packages found'

    if grep -q "$retorno" <<< "$STR"; then
        return 1
    else
        return 0
    fi
}

instaledpackage(){
    retorno="`dpkg-query -W $1`"
    SUB='no packages found matching'

    if grep -q "$retorno" <<< "$STR"; then
        return 1
    else
        return 0
    fi
}

echo '[+] Atualizando o sisetma para instalação'
apt update -y &> /dev/null
apt upgrade -y &> /dev/null
packages=("python3-pip" "unzip" "conky-all" "tor" "openvpn" "jq" "iptables")
for str in ${packages[@]}; do
    if instaledpackage ${str} ; then
        echo "[.] Já possui ${str};"
    else
        if existspackage ${str} ; then
            echo "[+] Será instalado ${str};"
        else
            echo "O pacote ${str} não existe. Por isso não pode ser instalado. Consulte manual de sua distribuição ou instale manualmente"
            exit 1
        fi
    fi
done

for str in ${packages[@]}; do
    if ! instaledpackage ${str} ; then
        if existspackage ${str} ; then
            echo "[+] Instalação do pacote ${str}"
            apt install ${str} -y &> /dev/null
        fi
    fi
done

# após a instalacao, vamos fazer uma força bruta d etestes
for str in ${packages[@]}; do
    if instaledpackage ${str} ; then
        echo "[.] Já possui ${str};"
    else
        if ! existspackage ${str} ; then
            echo "O pacote ${str} não existe. Por isso não pode ser instalado. Consulte manual de sua distribuição ou instale manualmente"
            exit 1
        fi
    fi
done

touch /etc/pip.conf
echo '[global]' > /etc/pip.conf
echo 'break-system-packages = true' >> /etc/pip.conf

echo '[+] Instalando por PIP netifaces'
pip3 install netifaces &> /dev/null
echo '[+] Instalando por PIP psutil'
pip3 install psutil &> /dev/null
echo '[+] Instalando por PIP pycryptodome'
pip3 install pycryptodome &> /dev/null
echo '[+] Instalando por PIP Pysocks'
pip3 install Pysocks &> /dev/null
echo '[+] Instalando por PIP socks'
pip3 install socks &> /dev/null

if [ -L ${DIR} ] ; then
    echo "O diretório ${DIR} nao pode ser usado pois é um link simbólico."
    exit 0
fi

if [ ! -d "/var/kfm/" ] ; then
    mkdir "/var/kfm/"
fi

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