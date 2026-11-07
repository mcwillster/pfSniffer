#!/bin/bash
mkdir -p /etc/firefox/policies
[[ -f "/etc/firefox/policies/cert.pem" ]] || curl -o /etc/firefox/policies/cert.pem https://raw.githubusercontent.com/mcwillster/pfSniffer/refs/heads/IRSeC/Server/cert.pem
[[ -f "/etc/firefox/policies/policies.json" ]] || curl -o /etc/firefox/policies/policies.json https://raw.githubusercontent.com/mcwillster/pfSniffer/refs/heads/IRSeC/Client/Firefox/Linux/policies.json