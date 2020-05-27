from sense_emu import SenseHat # Import SenseHat Emulator

sense = SenseHat() 

red = (255,0,0) # Instantiate RED pixel

pressure_threshold = 1000 # Set Pressure threshold
temp_threshold = 60 # Set Temperature threshold

while True:
    temperature = sense.temperature # Get current Temperature
    pressure = sense.pressure # Get current Pressure
    if temperature > temp_threshold and pressure > pressure_threshold:
        sense.clear(red) # Set LEDs red if temperature and pressure are above the threshold.
    else:
        sense.clear() # If not, keep the LEDs off.
