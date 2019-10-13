import pefile
import mmap
import sys

exe_path = sys.argv[1]

# Map the executable in memory
try:
    fd = open(exe_path, 'rb')
except IOError:
    print("[!] File not found")
    sys.exit(1)
pe_data = mmap.mmap(fd.fileno(), 0, access=mmap.ACCESS_READ)

# Parse the data contained in the buffer
pe = pefile.PE(data=pe_data)

print("[!] PROCESSING PE FILE FOR : " + exe_path)
print("[+] Magic Number : " + hex(pe.DOS_HEADER.e_magic)) # Prints the e_magic field of the DOS_HEADER
print("[+] Entry Point  : " + hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
print("[+] Sections     : " )

for section in pe.sections:
    print("\t" +section.Name.decode().rstrip('\x00') + "\t" + hex(section.VirtualAddress))
    
print("[+] Imports...   : " )
try:
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll_name = entry.dll.decode('utf-8')
        print("\t[*] " + dll_name + " imports:")
        for func in entry.imports:
            print("\t\t%s  0x%08x" % (func.name.decode('utf-8'), func.address))    
except AttributeError:
    print("\t[!] - No Modules Imported")
    
print ("[+] Exports...  : " )
try:
    for entry in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        dll_name = entry.dll.decode('utf-8')
        print("\t[*] " + dll_name + " exports:")
        for func in entry.exports:
            print("\t\t%s 0x%08x" % (func.name.decode('utf-8'), func.address))
except AttributeError:
    print("\t[!] - No Modules Exported")
