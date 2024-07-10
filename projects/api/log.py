import logging, os, sys;
from logging import handlers

class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # relationship mapping

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s;%(levelname)s;%(message)s'):
        filename = '/var/kfm/log/' + filename + ".log";
        if not os.path.exists( '/var/kfm/log/' ):
            os.makedirs( '/var/kfm/log/' );
        self.logger = logging.getLogger(filename);
        format_str = logging.Formatter(fmt) ;
        self.logger.setLevel(self.level_relations.get(level));
        console_handler = logging.StreamHandler() ;
        console_handler .setFormatter(format_str);
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,encoding='utf-8') ;
        th.setFormatter(format_str);
        self.logger.addHandler(th)
    def info(self, message):
        self.logger.info( message );
    def warning(self, message):
        self.logger.warning( message );
    def error(self, message):
        self.logger.error( message );

class Log():
    def __init__(self, name):
        self.file = Logger( name );
    def warning(self, message):
        self.file.warning( message );
    def info(self, message):
        self.file.info( message );
    def error(self, message):
        self.file.error( message );
    def download(self, arquivo, url):
        self.file.info("Download da URL: " + url + " será salvo como " + arquivo);
