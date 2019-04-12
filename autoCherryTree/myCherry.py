import subprocess
DEBUG = False
def main():
    fh = open("/root/Desktop/myNotes.ctd",'w')

    #DEBUG
    targets = "10.1.1.1-70"
    #DEBUG
    
    header(fh)
    pingScan(fh,targets)
    #Enum(fh)
    footer(fh)
    fh.close()
    
def header(handle):
    handle.write("<?xml version='1.0' ?>\n")
    handle.write("<cherrytree>\n")

def pingScan(handle, targets):

    handle.write("<node custom_icon_id='0' is_bold='True' name='Hosts' prog_lang='custom-colors' >\n") #START HOSTS  NODE
    SWEEP = "nmap -n -sP %s" % (targets)
    results = subprocess.check_output(SWEEP, shell=True)
    lines = str(results).encode("utf-8").split("\n")
    liveHosts = [line.split()[4] for line in lines if "Nmap scan report for" in line]

    #Create a new page for each live host
    for curIP in liveHosts:
        handle.write("<node custom_icon_id='0' is_bold='False' name='" + curIP + "' prog_lang='custom-colors' >\n") #START IP NODE
        #tcp scan
        handle.write("<node custom_icon_id='0' is_bold='False' name='TCP Service Scan' prog_lang='custom-colors'>\n") #START TCP NODE
        handle.write("<rich_text>\n") #START TCP NODE TEXT
        SCAN = "nmap -sC -sV -vvv %s" % (curIP)
        print("[SCAN] " + SCAN)
        SCAN_result = subprocess.check_output(SCAN, shell=True)
        SCAN_lines = str(results).encode("utf-8").split("\n")
        if DEBUG :
            print(" NMAP COMMAND ")
            print("[DEBUG] " + SCAN)
            print(" NMAP RESULT ")
            print("[DEBUG] " + str(SCAN_result))
            print(" NMAP LIST RESULT")
            print("[DEBUG] " + str(SCAN_lines))
        handle.write(SCAN_result)
        handle.write("</rich_text>\n") #END TCP NODE TEXT
        handle.write("</node>\n") #END TCP NODE
        handle.write("</node>\n") #END IP NODE
        
    handle.write("</node>\n") #END HOSTS NODE


def footer(handle):
    handle.write("</cherrytree>\n")

    

main()
