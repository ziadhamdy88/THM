
- ## *Port States*
	- **Open**
		- Indicates that a service is listening on the port.
	- **Closed**
		- Indicates that no service is listening on the port, although the port is accessible (reachable and not blocked by a firewall).
	- **Filtered**
		- Indicates that nmap cannot determine if the port is open or closed because the port is not accessible, usually due to firewall preventing nmap from reaching that port or the responses are blocked from reaching nmap's host.
	- **Unfiltered**
		- Indicates that nmap cannot determine if the port is open or closed, although the port is accessible, usually encountered when using an ACK scan `-sA`.
	- **Open|Filtered**
		- Indicates that nmap cannot determine if the port is open or filtered.
	- **Closed|Filtered**
		- Indicates that nmap cannot determine if the port is closed or filtered.

- ## *TCP Header Flags*
	- **URG**
		- Indicates that the urgent pointer filed is significant, the incoming data is urgent and that the the TCP segment should be processed immediately without consideration of having to wait on previous segments.
	- **ACK**	
		- Indicates that the acknowledgement number is significant, used to acknowledge the receipt of a TCP segment.
	- **PSH**
		- Ask TCP to pass the data to the application promptly.
	- **RST**
		- Used to reset the connection, another device like firewall could use it to tear a TCP connection.
	- **SYN**
		- Initiates a TCP 3-way handshake and synchronize numbers with the other host.
		- The sequence number should be set randomly during TCP connection establishment.
	- **FIN**
		- No more data to send.

- ## *TCP Connect Scan*
	- Works by completing the TCP 3-way handshake.
	- `nmap -sT <ip>`
	- Doesn't require privilege.

- ## *TCP SYN Scan*
	- Default scan mode but requires the user to be root or in sudoers.
	- Doesn't complete the TCP 3-way handshake, tears down the connection after the SYN/ACK is received from target.
	- This decreases the chances of the scan being logged.
	- `nmap -sS <ip>`

- ## *UDP Scan*
	- Since UDP is connectionless, it doesn't require a handshake hence we can't guarantee that a service listening on a UDP port would respond. **But if a UDP packet is sent to a closed port, an ICMP port unreachable error (type 3,code 3) is returned.**
	- `nmap -sU <ip>` and can be combined with another TCP scan.

- ## *NULL Scan*
	- Doesn't set any flag, all six flag bits are set to zero.
	- It will not trigger any response if port is open or filtered, but if a response with RST is sent, it means that the port is closed.
	- `nmap -sN <ip>`

- ## *FIN Scan*
	- It will not trigger any response if port is open or filtered, but if a response with RST is sent, it means that the port is closed.
	- `nmap -sF <ip>`

- ## *XMAS Scan*
	- Sets the FIN, PSH, and URG flags.
	- It will not trigger any response if port is open or filtered, but if a response with RST is sent, it means that the port is closed.
	- `nmap -sX <ip>`

- ## *NOTE*
	- **NULL, FIN, XMAS scans can be efficient when scanning a target behind a stateless firewall. However, a stateful firewall will block them.**

- ## *Maimon Scan*
	- Sets the FIN and ACK bits.
	- The target should respond with a RST packet. However, certain BSD-derived systems drop the packet if it is an open port exposing the open ports.
	- This scan won't work on most targets in modern networks.
	- `nmap -sM <ip>`

- ## *ACK Scan*
	- Set the ACK flag, the target would respond with a RST regardless of the state of the port because a TCP packet with ACK flag should be sent in response to a received TCP packet.
	- This scan is useful when there is a firewall in front of target, because the when the firewall blocks connection to an open port, no response is sent back.
	- Used to discover firewall rule sets and configuration.

- ## *Window Scan*
	- Almost the same as the ACK scan, however, it examines the TCP window field of the RST packets returned.
	- On specific systems, this can reveal that the port is open.
	- `nmap -sW <ip>`

- ## *Custom Scan*
	- Build your own TCP flag combination.
	- Using `--scanflags`, for example, set the SYN, RST, and FIN flags with `--scanflags SYNRSTFIN`.

- ## *NOTE*
	- **For the ACK and Window Scans, just because a firewall isn't blocking a specific port, doesn't necessarily mean that a service is listening on that port. For example there is a possibility that the firewall rules need to be updated to reflect recent service changes, hence they are exposing the firewall rules not the services.**

- ## *Spoofing & Decoys*
	- In some networks you can use a spoofed MAC or IP address to scan a target, this is only beneficial in a situation where you can guarantee to capture the response.
	- `nmap -e <net-interface> -Pn -S <spoofed-ip> <target-ip>`, the target will send the response to the spoofed IP address, so the attacker needs to monitor the network traffic to analyze the replies.
	- When the attacker is on the same subnet as target, spoofing MAC address is possible.
	- `nmap --spoof-mac <spoofed-mac> <ip>`
	- `nmap -D <decoy-ip-1>,<decoy-ip-2>,<decoy-ip-3>,<attacker-ip> <target-ip>` will  make the scan appear to be coming from 4 different IPs.
	- `nmap -D <decoy-ip-1>,RND,RND,<attacker-ip> <target-ip>`, the `RND` sets a randomly generated IP.

- ## *Fragmented Packets*
	- Adding `-f` to the nmap scan would divide the IP data into 8 bytes or less, adding another `-f -f` or `-ff` will split the data into 16 byte-fragments instead of 8.
	- Change the default value by setting the `--mtu`, should always choose a multiple of 8.
	- Increase the size of the packets to make them look not harmful by using `--data-length <size>`.

- ## *Idle/Zombie Scan*
	- Since spoofing can only work in certain network setups which requires the attacker to be in a position where he's able to monitor traffic, Idle or Zombie scans can be an upgrade.
	- It requires an idle system connected to the network that the attacker can communicate with, nmap will make each probe as if it is coming from the idle host then it will check for indicators where the idle system received any response to the spoofed probe by checking the IP identification value in the IP header.
	- `nmap -sI <zombie-ip> <target-ip>`.
	- For this to work, the attacker have to
		- Trigger the idle host to respond so that he can record the current IP ID on the idle host.
		- Send a SYN packet to a TCP port on the target. The packet should be spoofed to appear to be coming from the idle host IP address.
		- Trigger the idle host to respond again so that the attacker can compare the new IP ID with the one received earlier.
	- Different cases can occur
		- A common thing between the cases is that the attacker first sends a SYN/ACK packet to the idle host in which the idle host responds with a RST containing the IP ID, then the attacker sends a SYN packet to the TCP port of the target spoofing the idle host IP address.
		- Case 1
			- Port is closed, the target machine responds to the idle host with an RST packet and the idle host doesn't respond; hence its IP ID is not incremented.
		- Case 2
			- Port is open, the target machine responds with a SYN/ACK to the idle host and the idle host responds to this unexpected packet with an RST packet, incrementing its IP ID.
		- Case 3
			- The target machine doesn't respond at all due to firewall rules, this leads to the same result as the closed port; the idle host doesn't increase his IP ID.
		- The final step, the attacker sends  another SYN/ACK to the idle host, the idle host responds with an RST packet, incrementing his IP ID by one again, then the attacker compares the IP ID of the RST packer received in the beginning with the IP ID received in this step. if the difference is 1, then the port on the target machine was closed or filtered, if the difference is 2, then then the port is open.
	- **NOTE:**
		- **This scan requires an idle host that is not busy to allow the attacker to correctly and accurately compare IP IDs**

- ## *Getting More Details*
	- Adding `--reason` to make nmap provide more details about the conclusions.
	- `-v` for verbosity and `-vv` for more verbosity.
	- If that doesn't satisfy, add `-d` for debugging details or `-dd` for even more details.

- ## *Fine-Tuning Scope and Performance*
	- Limit the scope of the search by specifying certain ports.
	- Using `-F` for Fast Mode to scan only the most common 100 ports.
	- Using `--top-ports 10` to scan the most common 10 ports.
	- Control timing using `-T<0-5>`. `-T0` is the slowest (5 minutes between each probe), while `-T5` is the fastest, the slower, the less likely to be caught by IDS/IPS, however the faster the less accurate the scan results.
	- `-T4` is often used in CTFs and `-T1` is often used in real engagements where stealth is more important.
	- Control packet rate using `--min-rate <number>` and `--max-rate <number>`.
	- Control probing parallelization using `--min-parallelism <num-probes>` and `--max-parallelism <num-probes>`.