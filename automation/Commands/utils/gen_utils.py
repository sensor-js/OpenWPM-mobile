import smtplib
import os
from time import sleep


def get_last_crawled(log_file):
    last_line = ""
    for line in open(log_file):
        if "EXECUTING COMMAND: ('GET'" in line:
            last_line = line
    return int(last_line.split(", ")[-1].split(")")[0])


def poll_openwpm_log(log_file="~/openwpm/openwpm.log"):
    POLL_LOG_FREQ = 900  # sec
    log_file = os.path.expanduser(log_file)
    while True:
        last_crawled = get_last_crawled(log_file)
        print("last_crawled %s" % last_crawled)
        send_alert_email("Crawled %s sites" % last_crawled)
        sleep(POLL_LOG_FREQ)


def send_alert_email(msg="Cannot reach the phone"):
    fromaddr = 'appmonit@gmail.com'
    toaddrs = 'appmonit@gmail.com'
    msg = 'Subject: %s\n\n%s' % ("[appmonit-alert]", msg)
    # Credentials (if needed)
    username = 'appmonit'
    password = 'appmonit1'  # TODO change it
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


if __name__ == '__main__':
    poll_openwpm_log()

