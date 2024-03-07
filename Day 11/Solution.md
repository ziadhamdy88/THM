## ==**Enumeration**==
>	- Accessing the machine through `ssh cmnatic@10.10.79.127` with the provided password.
>	- There are multiple ways of finding `SUID` files:
>		1. Using `find / -perm -u=s -type f 2>/dev/null`
>		2. Using `LinEnum.sh` and hosting it on our own machine to be downloaded.
>	- Using the first method:
>		- ![[suid-method1.png]]
>		- `/bin/bash` and `/bin/ping` are interesting findings.
>	- Using the second method:
>		- Download `LinEnum.sh` from [GitHub](https://github.com/rebootuser/LinEnum/blob/master/LinEnum.sh).
>		- Start the HTTP server on the directory that contains the script.![[http-server.png]]
>		- Use `wget` to download the script on the vulnerable machine.![[wget-out.png]]
>		- Run the script using `./linenum.sh`.
>			- Since this tool scans the machine for various enumeration methods and misconfigurations the output can be large.![[script-out.png]]

## ==**Escalating Privileges**==
>	- Using `GTFObins` we can search for `bash`.
>	- Multiple options available, `reverse shell`, `file upload/download`, etc... The thing we are looking for is `SUID`.![[GTFObins.png]]
>	- Using `install -m =xs $(which bash) .` to maintain a privileged access.![[privesc.png]]
>	- Flag can be found in `/root/flag.txt`.![[rooms/25-days-of-cybersecurity/Day 11/flag.png]]
