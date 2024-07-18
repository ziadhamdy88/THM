
## **Enumeration**
>	- Running nmap script to get the open ports, their services and vulnerabilities. ![](nmap-out-1.png) ![](nmap-out-2.png)
>	- Using `gobuster` to enumerate directories. ![](gobuster-out.png)
>	- Visiting the pages found.
>	- `/blog` page loads. ![](blog-page.png)
>	- `/javascript` page requires permissions, and `/phpmyadmin` loads but default credentials don't work. ![](phpmyadmin.png)
>	- From the nmap scan, a login page could be found at `/blog/wp-login.php`. ![](wp-login.png)

## **Exploitation**
>	- Using `wpscan` to scan the login page. ![](wpscan-out-1.png) ![](wpscan-out-2.png)
>	- A user `admin` was found, trying to get the password using `wpscan --url internal.thm/blog -U admin -P /usr/share/wordlists/rockyou.txt `. ![](wpscan-pwd.png)
>	- Changing the `404` page to load a reverse shell. ![](rev-shell.png)
>	- Opening an `nc` listener and loading the page by visiting `/`.![](gained-access.png)

## **Enumeration v2**
>	- Spawning a bash shell using `python3 -c 'import pty;pty.spawn("/bin/bash")`.
>	- After traversing the machine, credentials were found in `/opt/wp-save.txt`. ![](aubreanna-creds.png)
>	- `SSH`ing into the machine with the found credentials.
>	- `User.txt` is found. ![](user-txt.png)
>	- The `jenkins.txt` file shows an internal server. ![](jenkins-txt.png)
>	- Using SSH Port Forwarding using `ssh -L 8000:172.17.0.2:8080 aubreanna@internal.thm` to make the server available to us. ![](port-fwd.png)
>	- Now visiting `localhost:8000` should show us the internal server. ![](internal-srv.png)
>	- Getting the post request through burp and saving it. ![](burp-req.png)
>	- Changing the password parameter to be fuzzable and keeping the username as admin. ![](fuzz-payload.png)
>	- Using `ffuf` to fuzz the credentials. ![](ffuf-out.png)
>	- No correct password, figured I would try another tool. Using `hydra localhost -f http-form-post "/j_acegi_security_check:j_username=^USER^&j_password=^PASS^&from=%2F&Submit=Sign+in&Login=Login:Invalid username or password" -s 8000 -V -l admin -P /usr/share/wordlists/rockyou.txt `. ![](hydra-out.png)
>	- ![](jenkins-out.png)

## **Privilege Escalation**
>	- After searching online for jenkins reverse shell, found a script to be run in `Manage Jenkins > Tools and Actions > Script Console`. ![](hacktricks-jenkins.png)![](jenkins-rev-shell.png)
>	- After traversing the machine, root credentials were found in `/opt/note.txt`. ![](root-creds.png)
>	- `SSH`ing into the machine with root credentials and getting the flag. ![](root-txt.png)