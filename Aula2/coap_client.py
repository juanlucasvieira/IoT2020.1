#!/usr/bin/env python
import getopt
import socket
import sys
import time
import random
import string

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines

# Author: Juan Lucas Vieira

client = None

def usage(): # Display usage message
    print "Command:\tpython coap_client.py -a [-P] -t -p "
    print "Options:"
    print "\t-a, --ipaddress=\tSet the Server IP address"
    print "\t-P, --port=\t\tSet the Server Port (default: 5683)"
    print "\t-t, --temperature=\tSet the temperature threshold"
    print "\t-p, --pressure=\t\tSet the pressure threshold"

# Callback function for Threshold Resource observation
# This function is called when the CoAP Server notify a modification in the Threshold Resource
def observe_callback(response):
    if response and response.payload and "temp=" in response.payload:
        data = response.payload.split(",")
        received_temp = float(data[0].replace("temp=",""))
        received_press = float(data[1].replace("press=",""))
        if received_temp != temp_thres or received_press != press_thres:
            print "THRESHOLD CHANGED! Temperature:",received_temp,"Pressure:",received_press
            print "Overwrite the actual threshold with your threshold? [Type OVERWRITE] - ACTUAL: "+ str(received_temp)+ " C / " + str(received_press) + " mbar -> YOUR: "+ str(temp_thres)+ " C / " + str(press_thres) + " mbar"

# This function sends the temperature and pressure threshold to the CoAP Server
def send_threshold(client, path, temp_thres, press_thres):
    answer = client.put(path, "temp="+str(temp_thres)+",press="+str(press_thres), timeout=1)
    if answer and answer.code == defines.Codes.CHANGED.number:
        print "Your threshold was specified! Temperature:",temp_thres,"Pressure:",press_thres
    return answer

def main():
    global client
    global ip
    global ledOn
    global temp_thres
    global press_thres
    global ledURI

    ledOn = False
    ledURI = None
    ip = None
    path = None
    payload = None
    temp_thres = None
    press_thres = None
    port = 5683
    try: # Get Args 
        opts, args = getopt.getopt(sys.argv[1:], "a:P:t:p:h", ["ipaddress=","--port=","temperature=","pressure=","help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts: # Get values of args and put into variables
        if o in ("-a", "--ipaddress"):
            ip = a
        elif o in ("-P", "--port"):
            port = float(a)
        elif o in ("-t", "--temperature"):
            temp_thres = float(a)
        elif o in ("-p", "--pressure"):
            press_thres = float(a)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(2)
            
    if ip is None:
        print "IP address must be specified"
        usage()
        sys.exit(2)

    if temp_thres is None:
        print "Temperature threshold must be specified"
        usage()
        sys.exit(2)

    if press_thres is None:
        print "Pressure threshold must be specified"
        usage()
        sys.exit(2)

    host = None
    try:
        tmp = socket.gethostbyname(ip)
        host = tmp
    except socket.gaierror:
        pass
    client = HelperClient(server=(host, port))
    
    path = "threshold"
    
    reply = None
    
    print "Specified Temperature Threshold:", temp_thres
    print "Specified Pressure Threshold:", press_thres
    
    try:
        reply = send_threshold(client, path, temp_thres, press_thres) # Send Threshold to Server
        client.observe(path, observe_callback) # Observe Threshold Resource modifications
        print "Observing Threshold..."
        print "Press Ctrl+C to exit client."
        while 1: # Loop until Ctrl+C is pressed.
            value = raw_input("")
            if value and "overwrite" in value.lower(): # If User wants to overwrite the Threshold stored in the Server with Client's Threshold
                reply = send_threshold(client, path, temp_thres, press_thres) # Send Client's threshold again
    except KeyboardInterrupt: # If Ctrl+C is pressed:
        print "Cancelling observing..."
        if reply is not None:
            client.cancel_observing(reply, True) # Cancel Resource Observation
        print "Stopping Client..."
        client.close() # Stop Client
        print "Stopped."


if __name__ == '__main__':
    main()

