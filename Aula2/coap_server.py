from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines
from threading import Thread # Import Thread
from sense_emu import SenseHat # Import SenseHat Emulator
import time

# Author: Juan Lucas Vieira

sense = SenseHat() # Instantiate SenseHat Emulator
red = (255,0,0) # Instantiate RED pixel

class ThresholdResource(Resource):
    
    def __init__(self, name="ThresholdResource", coap_server=None):
        super(ThresholdResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "temp=1000,press=10000"

    def render_GET(self, request): # Returns the threshold information
        return self

    def render_PUT(self, request): # Called when a client wants to specify the threshold.
        self.payload = request.payload
        print "NEW THRESHOLD:",self.payload
        return self
    
class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        global threshRes
        threshRes = ThresholdResource()
        self.add_resource('threshold/', threshRes) # Adds /threshold resource to the CoAP Server
        
# Checks whether the temperature and pressure reported by the sensor are above the Threshold
def checkValues(): 
    while run:
        threshold = threshRes.payload.split(",")
        tempThreshold = float(threshold[0].replace("temp=","")) # Get temperature of the Threshold resource
        pressureThreshold = float(threshold[1].replace("press=","")) # Get pressure of the Threshold resource
        if (getTemperature() > tempThreshold and getPressure() > pressureThreshold): # Sensor Temperature and Pressure > Threshold ?
            sense.clear(red) # Set LEDs red if above threshold
        else:
            sense.clear() # Turn of LEDs
        time.sleep(.5) # Reduce verification rate to every 500 milliseconds. 

# Get Sensor's Temperature
def getTemperature():
    return float(sense.temperature)

# Get Sensor's Pressure
def getPressure():
    return float(sense.pressure)

def main():
    global run
    run = True
    global server

    server = CoAPServer("0.0.0.0",5683)
    
    checkValuesTask = Thread(target = checkValues) # Create thread to check Sensor Temperature/Pressure values
    checkValuesTask.start() # Start Thread
    try:
        print "Server Started"
        server.listen(10) # Start listening for incoming messages
    except KeyboardInterrupt: # Shutdown server when Ctrl+C is pressed
        print "Stopping Server..."
        run = False
        server.close() # Stop Server
        sense.clear() # Turn off LEDs
        print "Stopped."

if __name__ == '__main__':
    main()


