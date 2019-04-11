import subprocess

def main():
    fh = open("/root/Desktop/myNotes.ctd",'w')

    #DEBUG
    targets = "10.1.1.1-90"
    #DEBUG
    
    header(fh)
    pingScan(fh,targets)
    #serviceScan(fh)
    #Enum(fh)
    footer(fh)
    fh.close()
    
def header(handle):
    handle.write("<?xml version='1.0' ?>\n")
    handle.write("<cherrytree>\n")

def pingScan(handle, targets):

    handle.write("<node custom_icon_id='0' is_bold='True' name='Hosts' prog_lang='custom-colors' >\n")
    SWEEP = "nmap -n -sP %s" % (targets)
    results = subprocess.check_output(SWEEP, shell=True)
    lines = str(results).encode("utf-8").split("\n")
    liveHosts = [line.split()[4] for line in lines if "Nmap scan report for" in line]

    #Create a new page for each live host
    for curIP in liveHosts:
        handle.write("<node custom_icon_id='0' is_bold='False' name='" + curIP + "' prog_lang='custom-colors' >\n")
        handle.write("</node>\n")


    handle.write("</node>\n")



def footer(handle):
    handle.write("</cherrytree>\n")
    
    

main()
