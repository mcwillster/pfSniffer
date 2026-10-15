# pfSense Logger

## Introduction
Logs pfSense control panel session IDs from the client side

## Installation

### Step 1: Pre-Ansible Setup (Unneeded if Ansible is already usable)
Run these 2 commands in an **Administrator Powershell**

(New-Object -TypeName System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1", "$env:temp\ConfigureRemotingForAnsible.ps1")
powershell.exe -ExecutionPolicy ByPass -File "$env:temp\ConfigureRemotingForAnsible.ps1"


### Step 2: Certificate Generation
You must generate new cert.pem and key.pem files as my key.pem file is not included in this repository (I'm not that stupid).
I used this command to generate them, it will ask a few questions about location and org info. You don't have to answer anything

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem

## Usage