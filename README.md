# Peekaboo

Peekaboo is a Python script that screenshots every service running on port 80 and 443, taking Nmap XML as input. It's a simple and quick alternative to other similar tools.

# Setup
```
python3 -m pip install -r requirements.txt
```

# Usage
Peekaboo takes Nmap XML as input, so first run an Nmap scan and use '-oX' to create the XML file.
```
python3 peekaboo.py nmap_results.xml
```
