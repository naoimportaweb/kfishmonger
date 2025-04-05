#!/bin/bash
# Script de instalação do KFM, que deverá ser alocado em /opt/
#    deste script sáo disparados as instalações de pacotes tanto
#    do Linux quanto do Python

# CORES para melhorar layout do instalador
export BLUE='\033[1;94m'
export GREEN='\033[1;92m'
export RED='\033[1;91m'
export RESETCOLOR='\033[1;00m'

DIR=/opt/kfishmonger    #Diretório padrão de instalação
auto=0                  #Se está no automático (1) ou manual (0), mas se for no
                        #      manual por command line e passar -y assume-se (1)

# Lista de pacotes Linux que serão instalados ou atualizados
packages=("python3-pip" "unzip" "conky-all" "tor" "openvpn" "jq" "iptables" "python3-pip")
#TODO: PARA CADA PROJETO TEM QUE DIZER QUAL PACOTE AQUI..... E DESCREVER CADA UM

# se é uma maquina de desenvolvedor, nao pode trazer do sourceforge
#    pois pode substituir arquivos novos por antigos, o programador pode
#    estar cansado e acabar errando, DESENVOLVERO só por github
if [ -L ${DIR} ] ; then
    echo "O diretório ${DIR} nao pode ser usado pois é um link simbólico."
    exit 0
fi

# Para evitar que pessoas desavisadas façam instalação sem 
#    poder para isso, o correto [e usar SUDO]
if [ "$EUID" -ne 0 ]
  then echo "Please run as root or sudo/Por favor, execute como root ou sudo"
  exit
fi

# Verifica se tem um -Y para não ficar pedindo autorizacao
for i; do 
   if [ $i = "-y" ] ; then
      auto=1
   fi 
done

# Vai sempre vai pegar a versão testada e estável
URL='https://sourceforge.net/projects/kfishmonger/files/latest/download'
printf "$BLUE[+]$RESETCOLOR A instalação será realizada pela URL $GREEN $URL $RESETCOLOR \r\n"

# a instalaçao em sí dos pacotes
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

    # kfm será um comando do linux, após a instalacao
    if [ -L /bin/kfm ] ; then
        rm /bin/kfm
    fi
    chmod +x ${DIR}/command/kfm.sh
    ln -s ${DIR}/command/kfm.sh /bin/kfm
    /bin/kfm -c install
    #salvar a URL como a ultima opção, vou fazer aqui em baixo pois sei que o processo de instalaçao acontecue.
    echo $URL > "/var/kfm/data/url.txt";
}

# verifica se existe o pacote no repositório
existspackage(){
    retorno="`apt-cache show $1`"
    SUB='No packages found'

    if grep -q "$retorno" <<< "$STR"; then
        return 1
    else
        return 0
    fi
}

# funçao que verifica se o pacote já está instalado na maquina
instaledpackage(){
    retorno="`dpkg-query -W $1`"
    SUB='no packages found matching'

    if grep -q "$retorno" <<< "$STR"; then
        return 1
    else
        return 0
    fi
}

# Sempre tem que atualizar a máquina, pois sempre estamos trabalhando
#    com os pacotes mais atualizados, estamos usando -y então vai no automático
#    senão, terá que perguntar se o cara requer atualizar, se não atualizar
#    nao podemos garantir nada.
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

# Dada a lista de pacotes para Linux, fazer laço que verifica tudo
#    nao pode passar se faltar alguma coisa
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

# se chegou ate aqui, tudo tem, entáo tem que agora instalar
for str in ${packages[@]}; do
    echo "[+] Instalação do pacote ${str}"
    apt install ${str} -y &> /dev/null
    
done

# vamos verificar se instalou tudo.....
for str in ${packages[@]}; do
    if ! instaledpackage ${str} ; then
        echo "[-] Não foi possível fazer a instalação do pacote ${str}"
        exit 1
    fi
done

# Aglumas versões do Debian exige um command line do PIP diferente
#     então ao utilizar este arquivo não será preciso isso.
touch /etc/pip.conf
echo '[global]' > /etc/pip.conf
echo 'break-system-packages = true' >> /etc/pip.conf

# Pacotes do python
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

# o projeto KFM guarda arquis em um diretório específico, é neste diretório
#    que os arquivos ficam difividos por módulos, então tem o módudo vpn que cria
#    o subdiretório /var/kfm/vpn/
#TODO: temos que ter um diretório de siglas
if [ ! -d "/var/kfm/" ] ; then
    mkdir "/var/kfm/"
fi

# Aqui ficam os arquivos de configuração geral do KFM
if [ ! -d "/var/kfm/data/" ] ; then
    mkdir "/var/kfm/data/"
fi

# aqui inicia a instalaçao do KFM, todas as dependencias estão
#    instaladas até o momento.
if [ -d ${DIR} ] ; then
    # o automático nunca pergunta para o usuário, vai direto
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