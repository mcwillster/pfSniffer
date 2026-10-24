$path1 = "C:\Program Files\Mozilla Firefox\distribution\policies.json"
$path2 = "C:\Program Files\Mozilla Firefox\distribution\cert.pem"

if (Test-Path -Path $path1 -PathType Leaf) {
    Write-Host "pfSniffer found"
} else {
    Write-Host "pfSniffer not found."
    New-Item -Path "C:\Program Files\Mozilla Firefox\distribution" -Name "MyFolder" -ItemType Directory
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mcwillster/pfSniffer/refs/heads/UB-Lockdown/Client/Firefox/Windows/policies.json" -OutFile "C:\Program Files\Mozilla Firefox\distribution\policies.json"
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mcwillster/pfSniffer/refs/heads/UB-Lockdown/Server/cert.pem" -OutFile "C:\Program Files\Mozilla Firefox\distribution\cert.pem"
    Import-Certificate -FilePath "C:\Program Files\Mozilla Firefox\distribution\cert.pem" -CertStoreLocation Cert:\LocalMachine\Root
}