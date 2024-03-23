
## *Enumeration*
>	- Using `nmap` to perform service, version, and vulnerability scan.
```
nmap -sVC -v 10.10.190.77
```
>	- ![](nmap-out.png)
>	- A quick google search will show that `robots.txt` file tells web crawlers which URLs is accessible.
>	- Going to `http://10.10.190.77/robots.txt`, a password can be found at the top.![](robots-pass.png)
>	- The `CMS` can be seen as well, which is `Umbraco`.
>	- The `nmap` scan shows the domain name `Anthem.com`.
>	- Going to this post.![](post-1.png)
>	- The poem is the clue, searching for it on google shows the answer `Solomon Grundy`
>	- Going to the other post.![](post-2.png)
>	- A possible naming convention could be used which is the initials of first and last name `SG@Anthem.com`.
>	- Inspecting the source code of the website gives us a the second flag.![](flag-2.png)
>	- Inspecting the first post page gives us the first flag.![](flag-1.png)
>	- Inspecting the second post pages gives us the fourth flag.![](flag-4.png)
>	- Going to John Doe's page, the third flag can be seen.![](flag-3.png)

## *Gaining Access*
>	 - Using the username `SG` and the found password to log in with `remmina`.![](user-content.png)
>	 - Going to the C directory and showing hidden files.![](hidden.png)
>	 - The `backup` directory contains a `restore.txt` file. The current user can't run it but can change the security permissions, add the user.![](perms-before.png)![](perms-after.png)
>	 - Access the `restore.txt` file and view it.![](admin-pass.png)
>	 - Now open `powershell` as administrator, view the user `administrator` directory.![](flag-5.png)