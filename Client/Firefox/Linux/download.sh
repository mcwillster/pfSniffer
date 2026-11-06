mkdir /etc/firefox/policies
curl -o /etc/firefox/policies/cert.pem https://raw.githubusercontent.com/mcwillster/pfSniffer/refs/heads/IRSeC/Server/cert.pem
curl -o /etc/firefox/policies/policies.json https://raw.githubusercontent.com/mcwillster/pfSniffer/refs/heads/IRSeC/Client/Firefox/Linux/policies.json