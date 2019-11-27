import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from threading import Thread

def get_userpass(username,password,subject,html,to):
	user = [line.rstrip('\n') for line in open(username)] # username file of smtp server to login to.
	passw = [line.rstrip('\n') for line in open(password)] # password file of smtp server to login to.
	rcept = [line.rstrip('\n') for line in open(to)] # list of recipients in filename to, you can divide this file into multiple files and use multi threading.
	sub = [line.rstrip('\n') for line in open(subject)] # subject line in file name subject, number of subjects in different line represents different subject lines
	htm = [line.rstrip('\n') for line in open(html)] # email body in file name html in one line, number of line represents different email.
	server = smtplib.SMTP_SSL('smtp.servername.com', 465) # change this.
	i=0;
	j=0;
	k=0;
	for j in range(len(user)): # this code sends bulk email to all recipients using single username , if you want multiple username you can use multithreading and multiple files
		server.login(user[j], passw[j])
		for k in range(len(sub)):
			for i in range(len(rcept)) :
				msg = MIMEMultipart('alternative')
				msg['Subject'] = sub[k]
				msg['From'] = user[j]
				msg['To'] = rcept[i]
				part1 = MIMEText(sub[k], 'plain')
				part2 = MIMEText(htm[k], 'html')
				msg.attach(part1)
				msg.attach(part2)
				print "\nthread: "+to+" sending mail to: "+''.join(rcept[i])+" from : "+''.join(user[j])+" subject : "+''.join(sub[k])
				server.sendmail(user[j], rcept[i], msg.as_string())
				time.sleep(1)
				f = open('logs.txt','a')
				f.write("\nmail sent:"+rcept[i])
			#	print "done!"
			#	print "all mail sent";
				server.quit()
	print "all users utilised!"
	exit()
#print time.time()-start

def Main():
	t1 = Thread(target=get_userpass, args=("username","password","subject","html","to",))
#	t2 = Thread(target=get_userpass, args=("username1","password1","subject1","html1","to1",)) # for this to run, create filename as given in arguments and put data according to it
	t1.start()
#	t2.start()
	print "main complete"
	
if __name__ == '__main__' :
	Main()
