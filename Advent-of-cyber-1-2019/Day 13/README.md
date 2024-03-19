
## **Enumeration**
>	- Using `nmap` to scan for services and their versions.
```
nmap -Pn -sV 10.10.1.110
```
>	![](nmap-out.png)
>	- A web server can be found running on port `80`.
>	- Using `gobuster dir -u http://10.10.1.110/ -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt --no-error` to search for hidden directories.![](gobuster-out.png)
>	- Going through the posts on the blog, it seems that the user `Wade` owns this website. Digging deeper through his posts and comments, one blog comment seems interesting.![](wade-pass.png)
>	- Performing another `gobuster` search on the found path.![](retro-gobuster-out.png)
>	- *Interesting* directories found :
>		- `wp-admin`, `wp-content`, and `wp-includes` had no permissions to access them.
>		- `wp-login.php`
>		- `wp-signup` which redirects to a `localhost` website.
>	- Using the credentials `wade:parzival` to access the `wp-admin` dashboard.![](wp-admin-page.png)
>	- Didn't find anything of interest.
>	- Trying to `RDP` using `remmina` on the host.![](rdp-access.png)
>	- `User.txt` file found.![](user-content.png)

## **Privilege Escalation**
>	- From the given hint, check the web history which shows that the user tried to search for a patch for `CVE-2019-1388`.
>	- A quick search on the CVE shows the vulnerability.![](cve-2019-1388.png)
>	- The vulnerability exploits the Windows Certificate Dialog process to open up a system process that opens a web page, which can be abused by trying to save the page and while in the `Save file` dialog open up `cmd` as administrator.![](privesc-1.png)
>	- ![](privesc-2.png)
>	- ![](privesc-3.png)
>	- ![](privesc-4.png)
>	- ![](privesc-5.png)