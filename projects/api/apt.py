# Compatibilidade: a implementação foi movida para empacotador.py, onde Apt
#    virou um filho da classe base Empacotador (junto com Dnf). Este arquivo
#    só re-exporta Apt para não quebrar os "from api.apt import Apt" antigos.
#    Novo código deve usar:  from api.empacotador import Empacotador
#                            empacotador = Empacotador.detectar();
from .empacotador import Apt;
