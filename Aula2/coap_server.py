from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines
from threading import Thread # Import Thread
from sense_emu import SenseHat # Import SenseHat Emulator
import time

# Author: Juan Lucas Vieira

sense = SenseHat()
red = (255,0,0) # Instantiate RED pixel
black = (0,0,0) # Instantiate OFF pixel

class ThresholdResource(Resource):
    
    occupiedLeds = [] # List containing IDs of LEDs being used by clients
    
    def __init__(self, name="ThresholdResource", coap_server=None):
        super(ThresholdResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "temp=1000,press=10000"

    def render_GET(self, request):
        return self

    def render_PUT(self, request): # Called when a client wants to turn ON or OFF the LED allocated to him.
        #threshold = request.uri_path.split(",")
        #temp = int(threshold[0].replace("temp=",""))
        #pressure = int(threshold[1].replace("press=",""))
        self.payload = request.payload
        print "NEW THRESHOLD:",self.payload
        return self
    
class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        global threshRes
        threshRes = ThresholdResource()
        self.add_resource('threshold/', threshRes)
        
def checkValues():
    #lastTemp = -100
    #lastPress = -100
    while run:
        threshold = threshRes.payload.split(",")
        tempThreshold = float(threshold[0].replace("temp=",""))
        pressureThreshold = float(threshold[1].replace("press=",""))
        # Check if Temp. or Pressure has changed, ignoring small changes to avoid sending sensors noise.
        if (getTemperature() > tempThreshold and getPressure() > pressureThreshold): 
            sense.clear(red)
            #server.notify(threshRes) # Notify observers when Temperature or Pressure has changed.
        else:
            sense.clear()
        time.sleep(.5) # Reduce verification rate to every 500 milliseconds. 

def getTemperature():
    return float(sense.temperature)

def getPressure():
    return float(sense.pressure)

def main():
    global run
    run = True
    global server

    server = CoAPServer("0.0.0.0",5683)
    
    checkValuesTask = Thread(target = checkValues) # Create thread to check Sensor Temp./Pressure values
    checkValuesTask.start()
    try:
        print "Server Started"
        server.listen(10) # Start listening for incoming messages
    except KeyboardInterrupt: # Shutdown server when Ctrl+C is pressed
        print "Stopping Server..."
        run = False
        server.close()
        sense.clear()
        print "Stopped."

if __name__ == '__main__':
    main()


