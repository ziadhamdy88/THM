
## **Enumeration**
>	- Running Nmap script to get open ports and scan for services and their vulnerabilities. ![](nmap-out-1.png) ![](nmap-out-2.png)
>	- Directory enumeration with `gobuster` didn't show any promising output. ![](gobuster-out.png)
>	- Used `smbclient -N -L \\<ip>` to view shares. ![](smbclient-out-1.png)
>	- Connecting to the `nt4wrksv` share using `smbclient \\\\10.10.82.106\\nt4wrksv`. ![](smbclient-out-2.png)
>	- The content of the passwords file is encoded. ![](passwords-txt.png)
>	- Using CyberChef to decode the passwords. ![](decoded-creds.png)

### **NOTE**: The machine keeps becoming unreachable, had to terminate it a couple of times.
## **Exploitation**
>	- From the previous Nmap, the machine is vulnerable to a variation of Eternal Blue (CVE-2017-0143).
>	- Creating a reverse shell using `msfvenom`. ![](msfvenom-out.png)
>	- Upload that shell using `smbclient`.
>	- Using metasploit's `multi/handler` to wait for the reverse shell. ![](msf_handler.png)
>	- Running the listener and then triggering the shell using `curl http://10.10.84.139:49663/nt4wrksv/rev_shell.aspx`. ![](reverse_shell.png)
>	- Searching for the user.txt file. ![](user-flag.png)

## **Privilege Escalation**
>	- Using `getsystem` functionality of meterpreter was able to escalate privileges using Named Pipe Impersonation. ![](root-txt.png)
>	- Documentation &rarr; [Rapid7's Github](https://github.com/rapid7/metasploit-framework/blob/master/documentation/modules/post/windows/escalate/getsystem.md#5---named-pipe-impersonation-print-spooler-variant) and [Red Team Notes](https://www.ired.team/offensive-security/privilege-escalation/windows-namedpipes-privilege-escalation)