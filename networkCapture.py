#!/usr/bin/env python3
"""Capture packets with Scapy and log a one-line summary per packet.

Requires: Python 3, scapy (pip install scapy). Needs root/BPF access to sniff,
e.g. sudo python3 networkCapture.py -i en0 -f "udp" -t 30 -w out.pcap
"""
import argparse
import logging
import sys

from scapy.all import PcapWriter, sniff


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("-f", "--filter", default="",
                   help='BPF filter, e.g. "host <SERVER_IP>" (default: none)')
    p.add_argument("-i", "--iface", default=None)
    p.add_argument("-c", "--count", type=int, default=0, help="0 means infinite")
    p.add_argument("-t", "--timeout", type=int, default=None,
                   help="seconds before stop")
    p.add_argument("-w", "--write", help="write to pcap file")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s:%(message)s")
    writer = PcapWriter(args.write, append=False, sync=True) if args.write else None

    def packet_handler(pkt):
        logging.info(pkt.summary())
        if writer:
            writer.write(pkt)

    try:
        sniff(filter=args.filter or None, iface=args.iface, prn=packet_handler,
              count=args.count or None, timeout=args.timeout, store=False)
    except PermissionError:
        sys.exit("Permission denied: run with sudo (packet capture needs root/BPF access).")
    finally:
        if writer:
            writer.close()


if __name__ == "__main__":
    main()
