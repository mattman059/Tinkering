import requests
from bs4 import BeautifulSoup as bs

url = "https://www.vulnhub.com/?page="
pageNum = "1"
vm_links = []
vms = {}


for pageNum in range(1,40):
    page = requests.get(url + str(pageNum))
    soup = bs(page.content,'html.parser')

    for a in soup.find_all('a',href=True):
        if "entry" in a['href']:
            if a['href'] not in vm_links:
                vm_links.append(a['href'])

print("Found : " + str(len(vm_links)) + " VMs")

for link in vm_links:
    vm_page = requests.get("https://www.vulnhub.com" + link)
    vm_soup = bs(vm_page.content,'html.parser')
    vm_size = vm_soup.find_all("small",class_="showhide")
    vms[link] = vm_size
    
    
    
print(vms)

'''
Split size line to grab all VM sizes : total ~130GB
print(str(value[0]).split(":")[1].split(" ")[1])

find download links for all VMs
x = vm_soup.find_all("a", href=True)
for item in x:
	if "download.vulnhub" in item['href']:
		print(item)
		
'''
