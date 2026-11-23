# Project Topic

## Goal
The goal of the project is to analyze network traffic through VPNs using Wireshark, to see the efficiency of different vpn protocols used in existing VPN software like NordVPN as well as a self-hosted VPN built from scratch. I will also conduct experiments to see whether there are pieces of information that could leak from the network traffic such as geolocations, etc.

## Initial plan for technical implementation
For the technical phase, I will use 2 sorts of VPNs. A pre-built VPN from a provider (NordVPN —paid subscription), a self-hosted VPN using a virtual private server from either AWS EC2, Linode, or Vultr, and a VPN protocol. I will rent a virtual machine from the previous server providers to host my VPN server online which will use the OpenVPN open-source protocol. After successfully setting up my VPN, we will analyze traffic with Wireshark pre-captured packets from public libraries.

## Author
Koffison Voumadi (sole contributor)