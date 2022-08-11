# ColdPlate
ColdPlate "Chiller" definition and testing

# Current State:
Currently is capable of testing the initialization and temperature control of the ColdPlate "Chiller"

# Commands Overview:
- Initialization
  - getVersion: returns the current firmware version number.
  - getDescription: returns the current model information.
  - version: returns the current model information followed by the version number.
  - info: returns the boot screen text (without device self-test information).
  - getSerial: returns the device serial number.
  - resetDevice: restarts the controller (this takes about 5 seconds).
  - getErrorList: returns a list with errors and warnings which can occur during processing.
  - enableCLED: permanently activates the LED indication light (the device will reset after this command).
  - disableCLED: permanently deactivates the LED indication light (the device will reset after this command).
  - getCLED: returns the status LED state
    - 1: LED is enabled
    - 2: LED is disabled
  - flashLed: device LED flashes 5 times
  - setBuzzer: lets the buzzer beep for the given time in milliseconds.
  - enableBootScreen: permanent activation of the boot screen startup text.
  - disableBootScreen: permanent deactivation of the boot screen startup text.
- Temperature Control
  - tempOn: activates the temperature control and starts heating/cooling
  - tempOff: switches off the temperature control and stops heating/cooling
  - getTempState: returns the state of the temperature function.
    - 0: Temperature control is disabled
    - 1: Temperature control is enabled
  - getTempStateAsString: return the state of the temperature function as a string.
    - off: Temperature control is disabled
    - on: Temperature control is enabled
  - getTempTarget: returns the target temperature.
  - setTempTarget: sets the target temperature in 1/10 C between -20 and 99.9 C.
    - Note: <value> range: -200 to 999 (3-digit value without a comma)
    - Note: temperature values are automatically limited to the min/max value (I set the program to exit if outside the bounds)
  - getTempActual: returns the current temperature
  - getTempMin: returns the minimum of the possible temperature set point
  - getTempMax: reeturns the maximum of the possible temperature set point
  - getTempLimiterMin: returns the minimum of the temperature set point
  - setTempLimiterMin: limits the minimum temperature set point
    - Note: <value> range: -200 to 999 (3-digit value without a comma)
    - Note: value must not be greater than the maximum limit
  - getTempLimiterMax: returns the maximum of the temperature set point
  - setTempLimiterMax: limits the maximum temperature set point
    - Note: <value> range: -200 to 999 (3-digit value without a comma)
    - Note: value must not be greater than the maximum limit
