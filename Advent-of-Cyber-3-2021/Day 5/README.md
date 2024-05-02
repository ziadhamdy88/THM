## *XSS*
>	- Accessing the website and logging in with the provided credentials.![](first-login.png)
>	- Going to the Settings page and trying to change password, shows the new password as a query in the URL.![](url-pass.png)
>	- Visiting the threads and trying to embed an html tag in a comment using `Hello <b>World</b>`.![](comment-bold.png)
>	- Now using the found vulnerability in the Settings page to change The Grinch's password.
>	- Adding a comment `<script>fetch('/settings?new_password=pass123');</script>` which would send a request for anyone that views the thread with that comment to change their password to `pass123`.![](stored-script.png)
>	- After a couple of seconds, Try to login with the credentials `grinch:pass123`.
>	- Going to the Settings page, the plugins are present, disable the `Christams to Buttmas` plugin.![](buttmas-plugin.png)
>	- The flag can be seen after disabling the plugin.![](flag.png)