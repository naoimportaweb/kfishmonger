#!/bin/bash

export BLUE='\033[1;94m'
export GREEN='\033[1;92m'
export RED='\033[1;91m'
export RESETCOLOR='\033[1;00m'

if [ "$EUID" -ne 0 ]
  then echo "Please run as root/Por favor, execute como root"
  exit
fi

DIR=/opt/kfishmonger

auto=0
for i; do 
   if [ $i = "-y" ] ; then
      auto=1
   fi 
done

if [ $auto -eq 1 ] ; then
    URL=`cat /var/kfm/data/url.txt`
else
    #printf "Se deseja instalar a versão estável digite (e), caso queira instalar a versão teste digite (t):"
    echo -e "\n\n $BLUE Temos dois repositórios, são estes: $RESETCOLOR"
    echo -e "  -$GREEN Repositório estável,$RESETCOLOR para instalar a versão estável digite e. É a recomendada."
    echo -e "  -$RED Repositório de testes,$RESETCOLOR para instalar a versão teste digite t. É a versão de testes de novas funcionalidades."
    printf "  Qual a$BLUE opção: $RESETCOLOR"
    read OPCAO
    if [ $OPCAO = "e" ] ; then
        URL='https://sourceforge.net/projects/kfishmonger/files/latest/download'
    else
        URL='https://codeload.github.com/naoimportaweb/kfishmonger/zip/refs/heads/main'
    fi
fi

install(){
        if [ -f /tmp/kfishmonger.zip ] ; then
            rm /tmp/kfishmonger.zip
        fi
        echo "[+] Download do arquivo: ${URL}" 
        wget -q -O /tmp/kfishmonger.zip ${URL}
        if [ -d /tmp/kfishmonger-main/ ] ; then
            rm -r /tmp/kfishmonger-main
        fi
        echo "[+] Descompactando /tmp/kfishmonger.zip" 
        unzip -qq /tmp/kfishmonger.zip -d /tmp/
        cp -r /tmp/kfishmonger-main/* ${DIR}
        if [ -L /bin/kfm ] ; then
            rm /bin/kfm
        fi
        chmod +x ${DIR}/command/kfm.sh
        ln -s ${DIR}/command/kfm.sh /bin/kfm
        /bin/kfm -c install
        #salvar a URL como a ultima opção, vou fazer aqui em baixo pois sei que o processo de instalaçao acontecue.
        echo $URL > "/var/kfm/data/url.txt";
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

if [ $auto -eq 1 ] ; then
    apt update -y 
    apt upgrade -y  
else
    printf 'Deseja atualizar o sistema para fazer a instalação, é recomendado? (y|n): '
    read OPCAO
    if [ $OPCAO = "y" ] ; then
        echo '[+] Atualizando o sisetma para instalação (* ISSO PODE DEMORAR)'
        apt update -y 
        apt upgrade -y 
    fi
fi

packages=("python3-pip" "unzip" "conky-all" "tor" "openvpn" "jq" "iptables" "python3-pip")
for str in ${packages[@]}; do
    if instaledpackage ${str} ; then
        echo "[.] Já possui ${str};"
    else
        if existspackage ${str} ; then
            echo "[+] Será instalado ${str};"
        else
            echo "$RED [*]O pacote ${str} não existe. Por isso não pode ser instalado. Consulte manual de sua distribuição ou instale manualmente$RESETCOLOR"
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
            echo "$RED [*]O pacote ${str} não existe. Por isso não pode ser instalado. Consulte manual de sua distribuição ou instale manualmente$RESETCOLOR"
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

if [ ! -d "/var/kfm/data/" ] ; then
    mkdir "/var/kfm/data/"
fi

if [ -d ${DIR} ] ; then
    if [ $auto -eq 1 ] ; then
        install
    else
        printf 'O diretório já existe, deseja continuar (y|n)?: '
        read OPCAO
        if [ $OPCAO = "y" ] ; then
            install
        else
            exit 0
        fi
    fi
else
    mkdir ${DIR}
    install
fi