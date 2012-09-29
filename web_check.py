#!/usr/bin/python
import httplib,sys,subprocess,smtplib,pickle
from email.mime.text import MIMEText
###############mail address##############
mailto_list=["abc@qq.com","abc@qq.com"]
###############init #####################
#domain = {}
#domain["www.eefocus.com"] = "ture"
#with open('status_check', 'wb') as f:
#        pickle.dump(domain, f)
###############send mail#################
mail_host="imap.eefocus.com"
mail_user="user"
mail_pass="passwd"
mail_postfix="imap.eefocus.com"
######################
time = subprocess.Popen("date +'%Y-%m-%d %H:%M:%S'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
date = time.stdout.read().rstrip()
def check_webserver(address, port, resource):
    time = subprocess.Popen("date +'%Y-%m-%d %H:%M:%S'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date = time.stdout.read().rstrip()
    #if not resource.startswith('/'):
    #    resource = '/' + resource
    try:
        conn = httplib.HTTPConnection(address, port, timeout=10)
        req = conn.request('GET', 'resource')
        response = conn.getresponse()
    except:
	    judge_tf('%s'%address,'false')
	    send_mail(mailto_list,'%s is not link' %address,'HTTP is not link :\n %s:%s\n %s\n' %(address, port, date))
	    return False
    finally:
        conn.close()
    if response.status in [200, 301, 302]:
	    with open('status_check', 'rb') as f:
            domain = pickle.load(f)
            if not domain[address] in "ture":
                 send_mail(mailto_list,'%s is ok ' %address,'HTTP response status:\n %s:%s status = %s\n %s\n' %(address, port, response.status, date))
                 with open('status_check', 'wb') as fw:
                      domain[address] = "ture"
                      pickle.dump(domain,fw)
    else:
	    judge_tf('%s'%address,'false')
	    send_mail(mailto_list,"%s is error" %address,'HTTP response status:\n %s:%s %s\n %s\n' %(address, port, response.status, date))
####################################################################################################
def send_mail(to_list,sub,content):
    time = subprocess.Popen("date +'%Y-%m-%d %H:%M:%S'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date = time.stdout.read().rstrip()
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText('%s\n' %(content))
    msg['Subject'] = '%s' %sub
    msg['From'] = me
    msg['date']= '%s' %date
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
####################################################################################################
def judge_tf(add,value1):
    with open('status_check', 'rb') as f:
        domain = pickle.load(f)
        if not domain[add] in '%s'%value1:
            with open('status_check', 'wb') as fw:
                domain[add] = '%s' %value1
                pickle.dump(domain,fw)
if __name__ == '__main__':
    page_list = open('web_check.txt', 'r')
    for line in page_list:
        host_port, res = line.rstrip().split("/")
        host, port = host_port.split(":")
        check_webserver(host, port, resource=res)
