#!/bin/bash

TOR_UID=debian-tor
TOR_PORT=9040
TOR_EXCLUDE="192.168.0.0/16 172.16.0.0/12 10.0.0.0/8"

export BLUE='\033[1;94m'
export GREEN='\033[1;92m'
export RED='\033[1;91m'
export RESETCOLOR='\033[1;00m'

# alterar a table NAT
iptables -t nat -A OUTPUT -m owner --uid-owner $TOR_UID -j RETURN
iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 53
iptables -t nat -A OUTPUT -p tcp --dport 53 -j REDIRECT --to-ports 53
iptables -t nat -A OUTPUT -p udp -m owner --uid-owner $TOR_UID -m udp --dport 53 -j REDIRECT --to-ports 53

#resolver enderecos .onion
iptables -t nat -A OUTPUT -p tcp -d 10.192.0.0/10 -j REDIRECT --to-ports 9050
iptables -t nat -A OUTPUT -p udp -d 10.192.0.0/10 -j REDIRECT --to-ports 9050

#excluir dados para a rede local e localnet
for NET in $TOR_EXCLUDE 127.0.0.0/9 127.128.0.0/10; do
	iptables -t nat -A OUTPUT -d $NET -j RETURN
done

#redirecionar todas as outras saídas através do TOR
iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports $TOR_PORT
iptables -t nat -A OUTPUT -p udp -j REDIRECT --to-ports $TOR_PORT
iptables -t nat -A OUTPUT -p icmp -j REDIRECT --to-ports $TOR_PORT

#accept already established connections
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

#excluir os enderecos de localhost
for NET in $TOR_EXCLUDE 127.0.0.0/8; do
	iptables -A OUTPUT -d $NET -j ACCEPT
done

#permitir somente as comunicacoes de saida do TOR
iptables -A OUTPUT -m owner --uid-owner $TOR_UID -j ACCEPT
iptables -A OUTPUT -j REJECT

echo -e "$GREEN *$BLUE All traffic was redirected through Tor$RESETCOLOR\n"
echo -e "$GREEN[$BLUE i$GREEN ]$BLUE You are under Anonymous tunnel$RESETCOLOR\n"
