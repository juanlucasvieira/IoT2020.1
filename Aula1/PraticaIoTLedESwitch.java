
import com.pi4j.io.gpio.*;
import com.pi4j.io.gpio.event.GpioPinDigitalStateChangeEvent;
import com.pi4j.io.gpio.event.GpioPinListenerDigital;

//Juan Lucas Vieira
public class PraticaIoTLedESwitch {

	public static void main(String[] args) throws InterruptedException {

		// GPIO Controller
		final GpioController gpio = GpioFactory.getInstance();

		// GPIO 01 pin to control the LED
		final GpioPinDigitalOutput ledPin = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_01, "LED", PinState.HIGH);
		
		// GPIO 02 pin to read switch state
		final GpioPinDigitalInput switchStatePin = gpio.provisionDigitalInputPin(RaspiPin.GPIO_02, "SWITCH", PinPullResistance.PULL_DOWN);
		
		ledPin.setShutdownOptions(true, PinState.LOW);
		switchStatePin.setShutdownOptions(true);
		
		// Switch listener to toggle LED light when the switch is flipped.
		switchStatePin.addListener(new GpioPinListenerDigital() {
		    @Override
		    public void handleGpioPinDigitalStateChangeEvent(GpioPinDigitalStateChangeEvent event) {
			ledPin.toggle();
		    }

		});
	}
}


