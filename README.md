# Peekaboo

Peekaboo is a Python script that screenshots every service running on port 80 and 443, taking Nmap XML as input. It's a simple and quick alternative to other similar tools. In the HTML results file, the images can be clicked to open up the service in a new tab.

# Setup
### Ensure Google Chrome is Downloaded
```
sudo apt update
```
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```
```
sudo apt install ./google-chrome-stable_current_amd64.deb
```
### Install Requirements
```
python3 -m pip install -r requirements.txt
```

# Usage
Peekaboo takes Nmap XML as input, so first run an Nmap scan and use '-oX' to create the XML file.
```
nmap 10.10.200.12 -oX nmap_results.xml
```
```
python3 peekaboo.py nmap_results.xml
```
