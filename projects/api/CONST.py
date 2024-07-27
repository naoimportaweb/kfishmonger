PATH_SYSTEM             = "/opt/kfishmonger";

TOR_SERVICE             = "tor.service";
TOR_SOCKS_5_PORT        = 9050;
TOR_TRANSPORT_PORT      = 9040;
TOR_HTTP_TUNNEL         = 9051;
TOR_DNS_PORT            = 53;

DNS_DEFAULT_RESOLVER    = "1.1.1.1";
DNS_LISTEN_PORT         = "53";
DNS_SERVICE             = "kfm_dns.service"

VPN_SERVICE             = "kfm_vpn.service";
VPN_SERVICE_OLD         = "vpn.service";

DB_PORT                 = 20001;
DB_SERVICE              = "kfm_db.service";

NETWORK_SERVICE         = "kfm_network.service";

FAKE_SERVICE            = "kfm_fake.service";

PANICROOM_SERVICE       = "kfm_panicroom.service";
PANICROOM_PORT          = 20002;

JSON_PORT               = 20000;
JSON_SERVICE            = "kfm_json.service"
JSON_SERVICE_OLD        = "json.service"

MONERO_SERVICE_OLD      = "monerod.service";
MONERO_SERVICE          = "kfm_monerod.service";


IGNORE_PORT_SCAN = [80, 8080, 9050, 9040, 9051, 53, 20000, 20001, 20002];