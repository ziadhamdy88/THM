## ==**Enumeration**==
>	- Using `nmap` to scan services, versions, and vulnerabilities.
```
nmap -Pn -sC -sV -vv -script vuln 10.10.97.39
```
>	![[nmap-1.png]]
>	![[nmap-2.png]]
>	- Web server version found to be `Apache Tomcat 9.0.17`.

## ==**Accessing the machine**==
>	- Using `Exploit-DB` to search with the found server version for possible vulnerabilities. 
>	- The found `CVE-2019-0232` script can be found in `msfconsole` through `windows/http/tomcat_cgi_cmdlineargs`.
>	- Setting the `RHOSTS` and `TARGETURI` parameters.![[msfconsole-params.png]]
>	- ==Important:== If a VPN is used, make sure that the acquired IP is the one in `LHOST`.![[gained-access.png]]
>	- Flag is found.![[flag1.png]]

## ==**(Optional) Privilege Escalation**==
>	- Using metasploit's post exploit suggester, `run post/multi/recon/local_exploit_suggester`.![[privesc-1.png]]
>	- COULDN'T CONTINUE...