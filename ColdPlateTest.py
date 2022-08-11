import time
from qinstruments import ColdPlate

if __name__ == '__main__':
    print(f"Testing the QInstrument ColdPlate 'Chiller'")

    # Initialize the ColdPlate object
    coldPlate = ColdPlate()

    # Initialization commands testing
    run_test = True if input("\n\aWould you like to run initialization tests [y/n]?\n") == 'y' else False
    if run_test:
        print(f"Firmware Version: {coldPlate.getVersion()}")
        print(f"Description: {coldPlate.getDescription()}")
        print(f"Version: {coldPlate.version()}")
        print(f"Info: {coldPlate.info()}")
        print(f"Serial Number: {coldPlate.getSerial()}")
        print(f"\nReset the device...{coldPlate.resetDevice()}\n")
        print(f"Error List: {coldPlate.getErrorList()}")
        led_on = True if coldPlate.getCLED() == 1 else False
        print(f"{coldPlate.getCLED(mode='str')}")
        if led_on:
            print(f"\t - Turning LED off perminently...")
            coldPlate.disableCLED()
            print(f"\t - Turning LED back on perminently...")
            coldPlate.enableCLED()
        else:
            print(f"\t - Turning LED on perminently...")
            coldPlate.enableCLED()
        led_on = True if coldPlate.getCLED() == 1 else False
        if led_on:
            print(f"\nFlashing the LEDs five times")
            coldPlate.flashLed()
        else:
            turn_on_led = True if input("Cannot test LED flashing with LED disabled, enable LED (takes about 5 seconds) [y/n]?\n") == 'y' else False
            if turn_on_led:
                coldPlate.enableCLED(warn=False)
                print(f"\nFlashing the LEDs five times")
                coldPlate.flashLed()
            else:
                print(f"LED flashing will not be tested since the LED is still disabled\n")

    # Temperature control tests
    run_test = True if input ("\n\aWould you like to test temperature control [y/n]?\n") == 'y' else False
    if run_test:
        print(f"Running detection of temperature control state")
        temp_control_enabled = True if coldPlate.getTempState() == 1 else False
        if temp_control_enabled:
            print(f"\tTemperature Control: {coldPlate.getTempStateAsString()}")
            print(f"\tTurning off temperature control for 2 seconds")
            coldPlate.tempOff()
            print(f"\tTemperature Control: {coldPlate.getTempStateAsString()}")
            time.sleep(2)
            print(f"\tTurning on temperature control")
            coldPlate.tempOn()
            print(f"\tTemperature Control: {coldPlate.getTempStateAsString()}")
        else:
            print(f"\tTemperature Control: {coldPlate.getTempStateAsString()}")
            print(f"\tTurning on temperature control")
            coldPlate.tempOn()
            print(f"\tTemperature Control: {coldPlate.getTempStateAsString()}")
        print("Current Temperature: {0} {1}C.".format(coldPlate.getTempActual(), u"\u00b0"))
        print("Running test on changing the temperature to {0} {1}C".format(30, u"\u00b0"))
        coldPlate.changeTemp(30)
        print("Running test on holding the temperature to {0} {1}C for 2 minute".format(35, u"\u00b0"))
        coldPlate.holdTempWithRuntime(value=35, runtime=120)