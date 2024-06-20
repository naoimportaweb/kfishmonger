#!/bin/bash

DIR=/opt/kfishmonger

install(){
        if [ -f /tmp/kfishmonger.zip ] ; then
            rm /tmp/kfishmonger.zip
        fi
        wget -O /tmp/kfishmonger.zip 'https://sourceforge.net/projects/kfishmonger/files/latest/download'
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