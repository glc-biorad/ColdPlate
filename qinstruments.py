from urllib import response
import serial
import time
import sys

import utils

class ColdPlate():
    def __init__(self):
        self._BAUD_RATE = 9600
        self._PARITY = None
        self._DATA_BITS = 8
        self._STOP_BITS = 1
        self._HANDSHAKE = False

        self._TEMPERATURE_VALUE_UNITS = 'celsius'
        self._MIN_WAIT_TIME_UNITS = 'seconds'

        self._MIN_WAIT_TIME_GET = 0.1

        self._MAX_WAIT_TIME_CHANGE_TEMP = 300 # 10 min

        # Serial port connection (Check Device Manger 'Ports' on Windows)
        self._serial_port = serial.Serial(port='COM6')

    def _write_command_and_wait(self, cmd, flush_buffers=True, timeout=0.2, as_string=True):
        if flush_buffers:
            utils.flush_buffers(self._serial_port)
        self._serial_port.write(cmd + b'\r')
        time_start = time.time()
        while time.time() - time_start < timeout:
            time.sleep(0.1)
        response_bstring = self._serial_port.read(self._serial_port.in_waiting)
        if as_string:
            try:
                return response_bstring.decode('utf-8')
            except:
                return response_bstring.decode("ISO-8859-1")
        return response_bstring

    # --------------------------------------------------------------------------------
    # Initialization Commands
    # --------------------------------------------------------------------------------

    def getVersion(self):
        '''
        Returns the current firmware version number as a string.
        '''
        return self._write_command_and_wait(b'getVersion')

    def getDescription(self):
        '''
        Returns the current model information as a string.
        '''
        return self._write_command_and_wait(b'getDescription')

    def version(self):
        '''
        Returns the current model information followed by the version number as a string.
        '''
        return self._write_command_and_wait(b'v')

    def info(self):
        '''
        Returns the boot screen text (withou device self-test information) as a string.
        '''
        return self._write_command_and_wait(b'info')

    def getSerial(self):
        '''
        Returns the device serial number as a string.
        '''
        return self._write_command_and_wait(b'getSerial')

    def resetDevice(self, warn=True):
        '''
        Restarts the controller. This takes about 5 sec.
        '''
        if warn:
            reset = True if input("\n\aWarning (ColdPlate.resetDevice): restarting the controller takes about 5 seconds, continue [y/n]?\n") == 'y' else False
            if reset:
                return self._write_command_and_wait(b'reset', timeout=5)
            else:
                print("\nDevice NOT reset\n")
                return None
        else:
            return self._write_command_and_wait(b'reset', timeout=5)

    def getErrorList(self):
        '''
        Returns a list with errors and warnings wich can occur during processing.
        Note: See also section "Error Control" in the ColdPlate Integration Manual.
        '''
        return self._write_command_and_wait(b'gel')

    def enableCLED(self, warn=True):
        '''
        Perminent activation of the LED indication lights.
        The instrument will reset after this command.
        '''
        if warn:
            reset = True if input("\n\aWarning (ColdPlate.enableCLED): preminently activating the LED lights will cause the device to reset which takes about 5 seconds, continue [y/n]?\n") == 'y' else False
            if reset:
                return self._write_command_and_wait(b'enableCLED', timeout=5)
            else:
                print("\nLEDs NOT perminently enabled\nDevice NOT reset\n")
                return None
        else:
            return self._write_command_and_wait(b'enableCLED', timeout=5)

    def disableCLED(self, warn=True):
        '''
        Perminent deactivation of the LED indication lights.
        The instrument will reset after this command.
        '''
        if warn:
            reset = True if input("\n\aWarning (ColdPlate.disableCLED): preminently deactivating the LED lights will cause the device to reset which takes about 5 seconds, continue [y/n]?\n") == 'y' else False
            if reset:
                return self._write_command_and_wait(b'disableCLED', timeout=5)
            else:
                print("\nLEDs NOT perminently disabled\nDevice NOT reset\n")
                return None
        else:
            return self._write_command_and_wait(b'disableCLED', timeout=5)

    def getCLED(self, mode='int'):
        '''
        Returns the status of the LED state as an int or string.
            value   1   LED is enabled
            value   2   LED is disabled
        '''
        modes = ['int', 'str']
        values = {
            1: "LED is enabled",
            2: "LED is disabled",
            }

        response = self._write_command_and_wait(b'getCLED')
        if mode == 'int':
            return int(response)
        elif mode == 'str':
            return values[int(response)]

    def flashLed(self):
        '''
        User device flashes LED five times.
        '''
        return self._write_command_and_wait(b'fld', timeout=2)

    def setBuzzer(self, value):
        '''
        Let's the buzzer beep for the given time in seconds.
        '''
        return None

    def enableBootScreen(self):
        '''
        Permanent activation of the boot screen startup text.
        '''
        return None

    def disbaleBootScreen(self):
        '''
        Permanent deactivation of the boot screen startup text.
        '''
        return None

    # --------------------------------------------------------------------------------
    # Temperature Control Commands
    # --------------------------------------------------------------------------------

    def tempOn(self):
        '''
        Activates the temperature control and starts heating/cooling.
        '''
        return self._write_command_and_wait(b'ton')

    def tempOff(self):
        '''
        Switches off the temperature control and stops heating/cooling.
        '''
        return self._write_command_and_wait(b'toff')

    def getTempState(self):
        '''
        Returns the state of the temperature function.
            value   0   Temperature control is disabled
            value   1   Temperature control is enabled
        '''
        values = {
            0: "Temperature control is disabled",
            1: "Temperature control is enabled",
            }

        return int(self._write_command_and_wait(b'gts'))

    def getTempStateAsString(self):
        '''
        Returns the state of the temperature function as a string.
            value off   Temperature control is disabled
            value on    Temperature control is enabled
        '''
        values = {
            'off': "Temperature control is disabled",
            'on': "Temperature control is enabled",
            }

        return self._write_command_and_wait(b'gtsas')

    def getTempTarget(self):
        '''
        Returns the target temperature as a float.
        '''
        return float(self._write_command_and_wait(b'gtt'))

    def setTempTarget(self, value):
        '''
        Sets the target temperature in 1/10 C between -20 and 99.9 C.
        Note: <value> range: -200 to 999 (3-digit value wihtout commas)
        Note: temperature values are automatically limited to the min/max value
        '''
        response = self._write_command_and_wait(b'stt' + str.encode(str(int(value * 10))))

        # Check to make sure the temperature target was set.
        temp_target_check = self.getTempTarget()
        if temp_target_check != value:
            print("Warning (ColdPlate.setTempTarget): target temperature of {0} {1}C was not set.".format(value, u"\u00b0"))
        else:
            return response

    def getTempActual(self):
        '''
        Returns the current temperature as a float.
        '''
        return float(self._write_command_and_wait(b'gta'))

    def getTempMin(self):
        '''
        Returns the minimum of the possible temperature set point as a float.
        Note: this command is used for information only
        '''
        return float(self._write_command_and_wait(b'gtmin'))

    def getTempMax(self):
        '''
        Returns the maximum of the possible temperature set point
        Notes: this command is used for information only
        '''
        return float(self._write_command_and_wait(b'gtmax'))

    def getTempLimiterMin(self):
        '''
        Returns the minimum of the temperature set point as a float.
        Note: can be adjusted with the setTempLimiterMin
        '''
        return float(self._write_command_and_wait(b'gtlmin'))

    def getTempLimiterMax(self):
        '''
        Returns the maximum of the temperature set point as a float.
        '''
        return float(self._write_command_and_wait(b'gtlmax'))

    def setTempLimiterMin(self, value):
        '''
        Limits the minimum temperature set point.
        Note: <value> range: -200 to 999 (3-digit value without a comma)
        Note: <value> must not be greater than the maximum limit
        '''
        # Make sure the minimum limit is not greater than the maximum limit.
        temp_limiter_max_check = self.getTempLimiterMax()
        if temp_limiter_max_check < value:
            print("\aWarning (ColdPlate.setTempLimiterMin): minimum temperature limit of {0} {1}C must be less than the maximum temperature limit of {2} {1}C.".format(value, u"\u00b0", temp_limiter_max_check))
            return None
        response = self._write_command_and_wait(b'stlmin' + str.encode(str(int(value * 10))))

        # Check to make sure the temperature limiter minimum was set.
        temp_limiter_min_check = self.getTempLimiterMin()
        if temp_limiter_min_check != value:
            print("\aWarning (ColdPlate.setTempLimiterMin): minimum temperature limit of {0} {1}C was not set.".format(value, u"\u00b0"))
        else:
            return response

    def setTempLimiterMax(self, value):
        '''
        Limits the maximum temperature set point.
        Note: <value> ranges: -200 to 999 (3-digit value without a comma)
        Note: value must not be lower than the minimum limit.
        '''
        # Make sure the maximum limit is not less than the minimum limit.
        temp_limiter_min_check = self.getTempLimiterMin()
        if temp_limiter_min_check > value:
            print("\aWarning (ColdPlate.setTempLimiterMax): maximum temperature limit of {0} {1}C must be greater than the minimum temperature limit of {2} {1}C.".format(value, u"\u00b0", temp_limiter_min_check))
            return None
        response = self._write_command_and_wait(b'stlmax' + str.encode(str(int(value * 10))))

        # Check to make sure the temperature limiter maximum was set.
        temp_limiter_max_check = self.getTempLimiterMax()
        if temp_limiter_max_check != value:
            print("\aWarning (ColdPlate.setTempLimiterMax): maximum temperature limit of {0} {1}C was not set.".format(value, u"\u00b0"))
        else:
            return response

    def changeTemp(self, value, delta=1):
        '''
        Change the temperature of the ColdPlate, input temperature and delta value in Celsius.
        '''
        # Check that the input value is within the minimum and maximum bounds.
        within_bounds = True if (value >= self.getTempLimiterMin() and value <= self.getTempLimiterMax()) else False
        if not within_bounds:
            sys.exit("Error (ColdPlate.changeTemp): {0} {1}C is not within the temperature bounds [{2}, {3}], exiting".format(value, u"\u00b0", self.getTempLimiterMin(), self.getTempLimiterMax()))

        # Make sure the temperature control is on.
        temp_control_enabled = True if self.getTempState() == 1 else False
        if not temp_control_enabled:
            self.tempOn()

        # Change the temperature.
        self.setTempTarget(value)
        time_start = time.time()
        while time.time() - time_start < self._MAX_WAIT_TIME_CHANGE_TEMP:
            # Check the actual temperature
            temp_actual = self.getTempActual()

            # Stop if heating/cooling if the target temperature has been reached.
            if ((temp_actual <= value + delta) and (temp_actual >= value - delta)):
                print("Temperature Reached: {0} {1}C".format(temp_actual, u"\u00b0"))
                self.tempOff()
                break
            else:
                print("Current Temperature: {0} {1}C".format(temp_actual, u"\u00b0"))
            time.sleep(0.1)

    def holdTempWithRuntime(self, value, runtime, verbose=True, delta=1):
        '''
        Holds the temperature for a given runtime in seconds.
        '''
        # Check that the input value is within the minimum and maximum bounds.
        within_bounds = True if (value >= self.getTempLimiterMin() and value <= self.getTempLimiterMax()) else False
        if not within_bounds:
            sys.exit("Error (ColdPlate.holdTempWithRuntime): {0} {1}C is not within the temperature bounds [{2}, {3}], exiting".format(value, u"\u00b0", self.getTempLimiterMin(), self.getTempLimiterMax()))

        # Make sure the temperature control is on.
        temp_control_enabled = True if self.getTempState() == 1 else False
        if not temp_control_enabled:
            self.tempOn()

        # Change the temperature if needed
        self.changeTemp(value)

        # Hold the temperature
        time_start = time.time()
        i = 1
        while time.time() - time_start < runtime:
            self.setTempTarget(value)
            if self.getTempActual() < value - delta:
                print("HERE")
                self.changeTemp(value)
            if verbose and i % 10 == 0:
                print("\tCurrent Holding Temperature: {0} {1}C".format(self.getTempActual(), u"\u00b0"))
                print(f"\tTime Left: {runtime - (i * 10)}s")
            i = i + 1
            time.sleep(1)