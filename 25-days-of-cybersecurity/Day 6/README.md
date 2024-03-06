## **Exploring the website**
>	- Visited `http://ip:5000`.
>	- Did a random search to view the parameters sent in the request.
>	- Found parameter `q` sent.
## **OWASP Zap**
>	- Performed an `Active Scan` on `http://ip:5000` to scan for vulnerabilities in the website.![[zap-scan.png]]
>	- Found 2 *HIGH* risk XSS vulnerabilities.
>	- Used the following path `http://ip:5000#javascript:alert(5397)` for a POC.
