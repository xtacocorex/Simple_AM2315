#!/usr/bin/python

# COPYRIGHT 2016 Robert Wolterman
# MIT License, see LICENSE file for details

# MODULE IMPORTS
import time
import logging

# GLOBAL VARIABLES
AM2315_I2CADDR = 0x5C
AM2315_READREG = 0x03
MAXREADATTEMPT = 3

class AM2315:
	"""Base functionality for AM2315 humidity and temperature sensor. """

	def __init__(self, address=AM2315_I2CADDR, i2c=None, **kwargs):
		if i2c is None:
			import Adafruit_GPIO.I2C as I2C
			i2c = I2C
		self._device = i2c.get_i2c_device(address, **kwargs)
		self._logger = logging.getLogger('am2315.AM2315')
		self.humidity = 0
		self.temperature = 0

	def _read_data(self):
		count = 0
		tmp = None
		while count <= MAXREADATTEMPT:
			try:
				logging.debug('am2315: read attempt: %d',count)
				# WAKE UP
				self._device.write8(AM2315_READREG,0x00)
				time.sleep(0.09)
				# TELL THE DEVICE WE WANT 4 BYTES OF DATA
				self._device.writeList(AM2315_READREG,[0x00, 0x04])
				time.sleep(0.09)
				tmp = self._device.readList(AM2315_READREG,8)
				# IF WE HAVE DATA, LETS EXIT THIS LOOP
				if tmp != None:
					logging.debug('am2315: have data!')
					print(tmp)
					# GET THE DATA OUT OF THE LIST WE READ
					self.humidity = ((tmp[2] << 8) | tmp[3]) / 10.0
					self.temperature = (((tmp[4] & 0x7F) << 8) | tmp[5]) / 10.0
					if (tmp[4] & 0x80):
						self.temperature = -self.temperature
					logging.debug('am2315: humidity: %.3f, temperature: %.3f',self.humidity,self.temperature)
					break
			except:
				count += 1
				time.sleep(0.01)
		
		# # GET THE DATA OUT OF THE LIST WE READ
		# self.humidity = ((tmp[2] << 8) | tmp[3]) / 10.0
		# self.temperature = (((tmp[4] & 0x7F) << 8) | tmp[5]) / 10.0
		# if (tmp[4] & 0x80):
		# 	self.temperature = -self.temperature
		# logging.debug('am2315: humidity: %.3f, temperature: %.3f',self.humidity,self.temperature)
 
	def read_temperature(self):
		logging.debug('am2315: read_temperature called')
		self._read_data()
		return self.temperature

	def read_humidity(self):
		logging.debug('am2315: read_humidity called')
		self._read_data()
		return self.humidity

	def read_humidity_temperature(self):
		logging.debug('am2315: read_humidity_temperature called')
		self._read_data()
		return (self.humidity, self.temperature)

	def read_humidity_temperatureF(self):
		logging.debug('am2315: read_humidity_temperature called')
		self._read_data()
		return (self.humidity, (self.temperature*(9/5))+32 )

if __name__ == "__main__":
	am2315 = AM2315()
	print(am2315.read_temperature() )
	print(am2315.read_humidity() )
	print(am2315.read_humidity_temperature() )
	
