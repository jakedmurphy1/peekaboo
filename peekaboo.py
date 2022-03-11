# Peekaboo -> Screenshot port 80 and 443
# For Nmap Parsing, creds to: https://github.com/laconicwolf/Nmap-Scan-to-CSV
# Created by Jake Murphy


import xml.etree.ElementTree as etree
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os, sys, webbrowser, pathlib


def get_host_data(root):
    """ Parses Nmap XML output and grabs hosts with port 80 and 443 """
    host_data = []
    hosts = root.findall('host')
    
    for host in hosts:

        # Ignore hosts that are not 'up'
        if not host.findall('status')[0].attrib['state'] == 'up':
            continue
        
        # Get IP address and host info
        ip_address = host.findall('address')[0].attrib['addr']
        
        # Get information on ports and services
        try:
            port_element = host.findall('ports')
            ports = port_element[0].findall('port')
            for port in ports:
                port_data = []

                # Ignore ports that are not 'open'
                if not port.findall('state')[0].attrib['state'] == 'open':
                    continue
                
                port_id = port.attrib['portid']
		
		# If port 80, store in array
                if int(port_id) == 80:
                    host_data.append("http://" + ip_address + ":" + port_id)
                elif int(port_id) == 443:
                    host_data.append("https://" + ip_address + ":" + port_id)
                
        except IndexError:
            print("IndexError")
    return host_data


def parse_xml(filename):
    """ Turn XML into Tree """
    try:
        #XML to tree
        tree = etree.parse(filename)
    except Exception as error:
        print("[-] A an error occurred. The XML may not be well formed.")
        exit()
    # Get root of tree
    root = tree.getroot()
    scan_data = get_host_data(root)
    return scan_data
    
    
def take_screenshots(hosts):
    """ Create HTML file and screenshot web interfaces """
    # Open HTML file for results
    f = open("screenshots/peekaboo.html", "a")
    f.write("<html><center><br><br>")
    
    # Configure webdriver to be silent
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    
    count = 0
    for host in hosts:
        count = count + 1
        print()
        print()
        print("----------------------------------------------------")
        print("Screenshotting --> " + host)
        print("----------------------------------------------------")
        try:
            # Attempt to screenshot, add to HTML results file
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options, service_log_path=None)
            driver.get(host)
            screenshot = driver.save_screenshot('screenshots/screenshot' + str(count) + '.png')
            f.write("<div><h2>" + host + "</h2><a href='" + host + "' target='_BLANK'><img style='border: 4px solid #555;width:50%' src='screenshot" + str(count) + ".png'></img></a></div><br><br><br><hr><br><br>")
        except:
            print("Could not screenshot " + host)
            continue
        driver.quit()
        
    f.write("</html></center>")
    f.close()
    
    try:
        # Attempt to automatically open HTML results file
        webbrowser.open('screenshots/peekaboo.html')
        print()
        print()
        print("Successfully Finished.")
    except:
        print()
        print()
        print("FINISHED, HTML FILE AVAILABLE IN " + str(pathlib.Path().resolve()) + "/screenshots/peekaboo.html")
 
 
if __name__ == '__main__':
    """ Let's get it started in here """
    
    # Get IP's with port 80 and 443
    hosts = parse_xml(sys.argv[1])
    
    # Clear old data, else create new results directory
    if os.path.isdir("screenshots"):
        os.system("rm screenshots/*")
    else:
        os.system("mkdir screenshots")
        
    # Screenshot and add to HTML file
    take_screenshots(hosts)     
    
