import sys
(str_ipaddr, str_cidr) = sys.argv[1].split("/")
octet = str_ipaddr.split(".") #No way to avoid having to split string?
cidr = int(str_cidr)          #Convert the cidr to INT
netmask = [0,0,0,0]
for net in range(cidr):
    netmask[(net//8)] = netmask[(net//8)] + (1 << (7 - net % 8)) # switch octets every 8 loops, calculates network mask
network = []
for netID in range(4):
    network.append(int(octet[netID]) & netmask[netID])
broadcast = list(network)
broadcast_range = 32-cidr
for bcast in range(broadcast_range):
    broadcast[3-(bcast//8)] = broadcast[3 - (bcast//8)] + (1 << (bcast%8)) # // performs integer division, takes floor
print("\nNetwork Information : " + str_ipaddr + "/" + str_cidr)
print("-------------------")
print("Netmask: %s" % ".".join(map(str,netmask)))
print("Network: %s" % ".".join(map(str,network)))
print("Broadcast: %s" % ".".join(map(str,broadcast)))














'''
NOTES
MOD takes precedence over subtraction order of operations is:
x -> (i % 8)
y -> (7 - (x))
1 << y == 2**y
>>> for i in range(0,64):
	print("i -> " + str(i) + " = " + str(1 << (7 - i % 8)))

i -> 0 = 128     2^7
i -> 1 = 64      2^6
i -> 2 = 32      2^5
i -> 3 = 16      2^4
i -> 4 = 8       2^3
i -> 5 = 4       2^2
i -> 6 = 2       2^1
i -> 7 = 1       2^0

Equivalent
    netmask[math.floor(i/8)] = netmask[math.floor(i/8)] + (1 << (7 - i % 8))
    netmask[math.floor(i/8)] = netmask[math.floor(i/8)] + (math.pow(2,(7-61%8))) # Requires math library
    
    (i//8) -> Integer Division, takes floor
    math.floor(i/8) Floating point division, uses math library to take floor # Requires math library
'''
