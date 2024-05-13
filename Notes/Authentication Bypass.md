- ## *Username Enumeration*
	- When trying to find authentication vulnerabilities, creating a list of valid usernames comes in handy.
	- Website error messages are great resources for collating this information to build our list of valid usernames.
	- Using `ffuf` with the found error messages to get valid usernames `ffuf -w /usr/share/wordlists/SecLists/Usernames/Names/names.txt -X POST -d "username=FUZZ&email=x&password=x&cpassword=x" -H "Content-Type: application/x-www-form-urlencoded" -u <url> -mr <error-message>`.
	- This makes the username variable while having static `email`, `password` and `cpassword`, to get already present usernames.
- ## *Brute Force*
	- With the found valid usernames, we can perform a brute-force attack on the login page.
	- `ffuf -w usernames.txt:W1,/usr/share/wordlists/SecLists/Passwords/Common-Credentials/10-million-password-list-top-100.txt:W2 -X POST -d "username=W1&password=W2" -H "Content-Type: application/x-www-form-urlencoded" -u <url> -fc 200`
		- Having multiple variables, we have to set names to each hence the `usernames.txt:W1` here W1 is the variable name which can be used later when forming the POST data.
		- `fc` to check for status code 200.
- ## *Logic Flaw*
	- A logic flaw is when the typical logical path of an application is either bypassed, circumvented or manipulated by a hacker. Logic flaws can exist in any area of a website.
	- For example
		- The below mock code example checks to see whether the start of the path the client is visiting begins with /admin and if so, then further checks are made to see whether the client is, in fact, an admin. If the page doesn't begin with /admin, the page is shown to the client.
			`if( url.substr(0,6) === '/admin') {`
				`# Code to check user is an admin`
			`} else {`
				`# View Page`
			`}`
		- Because the above PHP code example uses three equals signs `===`, it's looking for an exact match on the string, including the same letter casing.
		- The code presents a logic flaw because an unauthenticated user requesting `/adMin` will not have their privileges checked and have the page displayed to them, totally bypassing the authentication checks.
- ## *Cookie Tampering*
	- Examining and editing the cookies set by the web server during your online session can have multiple outcomes, such as unauthenticated access, access to another user's account, or elevated privileges.
	- #### *Plain Text*
		- The contents of some cookies can be in plain text, and it is obvious what they do. Take, for example, if these were the cookie set after a successful login:
			 - Set-Cookie: logged_in=true; Max-Age=3600; Path=/
			 - Set-Cookie: admin=false; Max-Age=3600; Path=/
		 - We see one cookie (logged_in), which appears to control whether the user is currently logged in or not, and another (admin), which controls whether the visitor has admin privileges. 
		 - Using `curl -H "Cookie: logged_in=true; admin=true" <url>` will result in a log in with elevated privilege.
	 - #### *Hashing*
		 - Sometimes cookie values can look like a long string of random characters; these are called hashes which are an irreversible representation of the original text.
		 - Using tools like [Crackstation](https://crackstation.net/) to try to get the plain text.
	 - #### *Encoding*
		 - It creates what would seem to be a random string of text, but in fact, the encoding is reversible.
		 - Encoding allows us to convert binary data into human-readable text that can be easily and safely transmitted over mediums that only support plain text ASCII characters.
		 - Using tools like [CyberChef](https://gchq.github.io/CyberChef/)to decode/encode data.
		 - 