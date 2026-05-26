import smtpd, asyncore, traceback, sys, os;

class SMTPServerFake(smtpd.SMTPServer):
    def __init__(*args, **kwargs):
        smtpd.SMTPServer.__init__(*args, **kwargs);

    def process_message(*args, **kwargs):
        pass;

if __name__ == "__main__":
    smtp_server = SMTPServerFake(('localhost', 25), None);
    try:
        asyncore.loop();
    except KeyboardInterrupt:
        smtp_server.close();
        sys.exit(0);
    except:
        traceback.print_exc();
# https://muffinresearch.co.uk/fake-smtp-server-with-python/