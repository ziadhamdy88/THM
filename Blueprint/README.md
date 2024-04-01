
## *Enumeration*
>	- Use the `nmap` script to get open ports and then scan these ports for services' versions, and vulnerabilities.![](nmap-script.png)
>	- ![](nmap-out-1.png)![](nmap-out-2.png)![](nmap-out-3.png)
>	- Accessing `http://10.10.135.85:80` gives a 404 error.![](404-error.png)
>	- Accessing `https://10.10.135.85`.![](apache-443.png)![](oscommerce-catalog.png)
>	- The same website is accessible through `http://10.10.135.85:8080/oscommerce-2.3.4/catalog/`
>	- `OsCommerce` is an ERP application, checking for vulnerabilities for the found version.![](oscommerce-vuln.png)
## *Exploitation*
>	- Checking the RCE scripts.![](rce-script-1.png)![](rce-script-2.png)![](rce-script-3.png)
>	- The script takes the URL as an argument, execute the script using `python rce.py http://10.10.135.85:8080/oscommerce-2.3.4/catalog/`.![](rce-script-out.png)

## *Enumeration*
>	- `NTLM` hashes are located in the SAM.
>	- Using `reg.exe` to save the three files `SAM`, `SYSTEM`, and `SECURITY` from binary store located in `System32/config`.![](ntlm-files.png)
>	- These files can be found at `http://10.10.135.85:8080/oscommerce-2.3.4/catalog/install/includes/`.![](ntlm-files-web.png)
>	- Download them to be used to crack the hash.
>	- Using `samdump2 SAM SYSTEM` to get the hash values.![](sam-hashes.png)
>	- Using the found hash for `Lab` user in `crackstation`.![](lab-hash-cracked.png)
>	- 
>	- Exploring the machine, we can access the `/Administrator` directory.
>	- The `root.txt.txt` which contains the flag is located in the `Desktop`.![](flag-1.png)
>	- 