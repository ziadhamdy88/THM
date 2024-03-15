## **Enumeration**
>	- Accessing the machine using `ssh mcsysadmin@10.10.187.14` and the provided password.
>	- Get number of files using `ls | wc -l`.![](file-count.png)
>	- Get file containing string "password" using `grep -l -e "password" -f *`.![](string-pass.png)
>	- Get the IP in a file by using `cat file* | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}"`.![](ip.png)
>	- Get user counts by using `ls -la /home`.![](user-counts.png)
>	- Get `sha1` hash of `file8` using `sha1sum file8`.![](file8-hash.png)
>	- Since `/etc/shadow` isn't accessible by current user, search for a `shadow.bak` file and `cat` its content using the following.
```
cat `find / 2>/dev/null | grep "shadow.bak"` | grep "mcsysadmin"
```
>	![](mcsysadmin-hash.png)