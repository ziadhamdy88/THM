## ==**Discovering Samba**==
>	- Using `enum4linux` we can discover both the `users` that can access the share and the `shared folders`.
>	- Using `enum4linux -U 10.10.206.70`.![[Samba-users.png]]
>	- Using `enum4linux -S 10.10.206.70`.![[Samba-shared.png]]

## ==**Accessing share**==
>	- Testing the found shares with `smbclient`.
>	- Access to `//10.10.206.70/tbfc-santa` doesn't require a password.![[santa-access.png]]
>	- Downloaded the file using `get note_from_mcskidy.txt`.![[file-down.png]]
>	- Reading the note gives us the clue to the answer `jingle-tunes`.![[final-clue.png]]