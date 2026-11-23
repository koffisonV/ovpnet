# Self-Hosted VPN Analysis

Performance and security comparison of a self-hosted OpenVPN server on AWS EC2 vs NordVPN (WireGuard).

[Demo video](https://youtu.be/xHemKKHjR0s?si=WPD2a_4SGnNQTny4)

## Overview

I deployed an OpenVPN Access Server on AWS EC2 and compared it with NordVPN (WireGuard) and a plain connection, using `networkquality`, `traceroute` and Wireshark on macOS. Background and write-up: [research.md](research.md), [ProjectTopic.md](ProjectTopic.md).

## Setup (self-hosted server)

1. **Launch**: EC2 instance (`t2.micro`, region `eu-central-1`) from the OpenVPN Access Server image in the AWS Marketplace (Access Server v2.13.1, Linux). Using the Marketplace image avoided running unverified install scripts. ([instance screenshot](screenshots/deployedInstance.jpg), [Access Server status](screenshots/Screenshot%202024-05-17%20at%201.04.54%E2%80%AFPM.jpg))
2. **Administer**: connected to the instance over SSH to complete the Access Server setup and manage it.
3. **Client**: imported the generated client profile into OpenVPN Connect on macOS ([profile](screenshots/clientProfile.jpg), [connected](screenshots/openVPNClient.jpg)).
4. **Cost control**: stopped the instance whenever it was idle, since AWS bills by time and usage (see [research.md](research.md)).

Not recorded in this repo: the security-group port list and AMI ID. The instance has since been terminated, and identifying details (IP, instance ID, MAC addresses) are redacted in the screenshots.

## Results

One run per condition, on the same Mac and network.

### Throughput and latency (`networkquality`)

| Condition | Downlink | Uplink | Idle latency | Responsiveness |
|---|---|---|---|---|
| [Normal connection](analysis/speed/normal.jpg) | 180.731 Mbps | 32.665 Mbps | 31.792 ms | Medium (148.515 ms, 404 RPM) |
| [NordVPN (WireGuard)](analysis/speed/nordvpn.jpg) | 197.358 Mbps | 14.111 Mbps | 131.250 ms | Low (2.069 s, 29 RPM) |
| [Self-hosted (OpenVPN)](analysis/speed/self%20hosted%20vpn.jpg) | 107.742 Mbps | 9.099 Mbps | 118.250 ms | Low (555.556 ms, 108 RPM) |

The self-hosted path had the lowest downlink, consistent with a small `t2.micro`; a single run per condition is not enough to rank the two VPNs on latency.

### Path (`traceroute google.com`)

- [Normal](analysis/traceroute/normal%20connection.jpg): local ISP, exits in the New York area (`lga` hop).
- [Self-hosted](analysis/traceroute/self%20hosted%20vpn.jpg): traffic goes through AWS `eu-central-1` and exits in Frankfurt (`fra` hop); about 100 ms on early hops.
- [NordVPN](analysis/traceroute/nordvpn.jpg): every hop timed out and I cancelled it, so no path was obtained.

### What was visible on the wire (Wireshark on `en0`)

- [Normal](analysis/encryption/normal%20connection.jpg): QUIC/UDP, TLS, ICMP and plain TCP, visible per destination.
- [NordVPN](analysis/encryption/nordvpn.jpg): only WireGuard "Transport Data" packets to a single server.
- [Self-hosted](analysis/encryption/self%20hosted%20vpn.jpg): only OpenVPN `P_DATA_V2` packets to a single server (plus local IGMP).

This is a protocol-identification check: with either VPN the outer traffic shows the VPN protocol and the server endpoint, not the destinations or application protocols. I did not test DNS leaks, IPv6 leaks, or cipher settings.

## Scripts

Both are optional helpers for capture and summary; the screenshots above came from the macOS tools, not these scripts. I ran them on macOS.

- [analysis.sh](analysis.sh): `tcpdump` capture then `tshark` summaries (conversations, protocol hierarchy, endpoints). Needs `tcpdump`, `tshark` (Wireshark) and GNU `timeout` (`brew install coreutils`; `numfmt` optional). Needs `sudo` or BPF access. Uses `set -euo pipefail`; `-h` prints usage. Checked with ShellCheck.
- [networkCapture.py](networkCapture.py): Scapy sniffer that logs packet summaries and can write a pcap. Needs Python 3 and `pip install scapy`; needs `sudo`.

```bash
sudo ./analysis.sh -i en0 -d 60
sudo ./analysis.sh -i en0 -d 300 -f "udp port 1194" -v
sudo python3 networkCapture.py -i en0 -f "host <SERVER_IP>" -t 60 -w capture.pcap
```

## Project structure

```
myvpn/
├── analysis/            # screenshots of results
│   ├── encryption/      # Wireshark captures
│   ├── speed/           # networkquality output
│   └── traceroute/      # traceroute output
├── screenshots/         # server and client setup (redacted)
├── analysis.sh          # tcpdump/tshark capture + summary
├── networkCapture.py    # Scapy capture
├── ProjectTopic.md
├── research.md
├── LICENSE
└── README.md
```

## Author

Koffison Voumadi (sole contributor)

Licensed under the MIT License.
