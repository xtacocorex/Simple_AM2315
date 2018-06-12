#!/usr/bin/python

# COPYRIGHT 2016 Robert Wolterman
# MIT License, see LICENSE file for details

# MODULE IMPORTS
import time
import logging
from smbus2 import SMBus

# GLOBAL VARIABLES
AM2315_I2CADDR = 0x5C
AM2315_READREG = 0x03
MAXREADATTEMPT = 3

class AM2315:
	"""Base functionality for AM2315 humidity and temperature sensor. """

	def __init__(self, address=AM2315_I2CADDR, **kwargs):
		# if i2c is None:
		# 	import Adafruit_GPIO.I2C as I2C
		# 	i2c = I2C
		# self._device = i2c.get_i2c_device(address, **kwargs)
		self.bus = SMBus(1)
		self._logger = logging.getLogger('am2315.AM2315')
		self.humidity = 0
		self.temperature = 0
		self.error = False

	def calculate_crc(self,blength):
		crc = 0xFFFF
		w = 0
		while blength:
			blength = blength - 1
			crc = crc ^ buffer[w]
			w = w + 1
			for i in range(0,8):
				if crc & 0x01:
					crc = crc >> 1
					crc = crc ^ 0xA001
				else:
					crc = crc >> 1

		return crc

	def _read_data(self):
		count = 0
		tmp = None

		#Reset reading states to zero, so if it fails we realize it
		self.temperature = 0
		self.humidity = 0

		while count <= MAXREADATTEMPT:
			try:
				logging.debug('am2315: read attempt: %d',count)
				# WAKE UP
				# self._device.write8(AM2315_READREG,0x00)
				self.bus.write_byte_data(AM2315_I2CADDR,AM2315_READREG,0)
				time.sleep(0.09)
				# TELL THE DEVICE WE WANT 4 BYTES OF DATA
				# self._device.writeList(AM2315_READREG,[0x00, 0x04])
				self.bus.write_i2c_block_data(AM2315_I2CADDR,AM2315_READREG,[0x00,0x04])
				time.sleep(0.09)
				# tmp = self._device.readList(AM2315_READREG,8)
				tmp = self.bus.read_i2c_block_data(AM2315_I2CADDR,AM2315_READREG, 8)
				# IF WE HAVE DATA, LETS EXIT THIS LOOP
				if tmp != None:
					#Check crc for data errors
					if self.check_crc(tmp) == False:
						self.error = True
						print("crc_error")
						break
					else:
						self.error = False

					logging.debug('am2315: have data!')
					# GET THE DATA OUT OF THE LIST WE READ
					self.humidity = ((tmp[2] << 8) | tmp[3]) / 10.0
					self.temperature = (((tmp[4] & 0x7F) << 8) | tmp[5]) / 10.0
					if (tmp[4] & 0x80):
						self.temperature = -self.temperature
					logging.debug('am2315: humidity: %.3f, temperature: %.3f, errors: %r',self.humidity,self.temperature,self.error)
					break
			except Exception as e:
				print(e)
				count += 1
				time.sleep(0.01)
		
	def check_crc(self,dbuf):
		crc_res = self._calculate_crc(6)
		crc = (dbuf[7] << 8) + dbuf[6]

		# print("CRC_res:",crc_res)
		# print("CRC", crc)
		return crc==crc_res

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
	print(am2315.read_humidity_temperatureF() )
	
