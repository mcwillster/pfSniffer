# pfSense Logger

## Introduction
Logs pfSense control panel session IDs from the client side

## Installation

### Step 1: Pre-Ansible Setup (Unneeded if Ansible is already usable)
Run these 2 commands in an **Administrator Powershell**
'''(New-Object -TypeName System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1" "$env:temp\ConfigureRemotingForAnsible.ps1")
powershell.exe -ExecutionPolicy ByPass -File "$env:temp\ConfigureRemotingForAnsible.ps1"'''

## Usage