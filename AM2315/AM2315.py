#!/usr/bin/python

# COPYRIGHT 2016 Robert Wolterman
# MIT License, see LICENSE file for details

# MODULE IMPORTS
import time

# GLOBAL VARIABLES
AM2315_I2CADDR = 0x5C
AM2315_READREG = 0x03

class AM2315(object):
    """Base functionality for AM2315 humidity and temperature sensor. """

    def __init__(self, address=AM2315_I2CADDR, i2c=None, **kwargs):
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        self.humidity = 0
        self.temperature = 0

    def _read_data(self):
        print "READ DATA"
        # TELL THE DEVICE WE WANT 4 BYTES OF DATA
        self._device.writeList(AM2315_READREG,[0x00, 0x04])

        # QUICK SLEEP
        time.sleep(0.1)

        # DOING 4 RAW READS TO GET OUR DATA
        msb_rh = self._device.readRaw8()
        lsb_rh = self._device.readRaw8()
        msb_t  = self._device.readRaw8()
        lsb_t  = self._device.readRaw8()

        # DO MATH
        self.humidity = ((msb_rh << 8) | lsb_rh) / 10.0
        self.temperature = (((msb_t & 0x7F) << 8) | lsb_t) / 10.0
        if (msb_t >> 7):
            self.temperature = -self.temperature

    def read_temperature(self):
        self._read_data()
        return self.temperature

    def read_humidity(self):
        self._read_data()
        return self.humidity

    def read_humidity_temperature(self):
        self._read_data()
        return (self.humidity, self.temperature)

if __name__ == "__main__":
    am2315 = AM2315()
    print am2315.read_temperature()
    print am2315.read_humidity()
    print am2315.read_humidity_temperature()
    
