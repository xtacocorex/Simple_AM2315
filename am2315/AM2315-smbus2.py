from smbus2 import SMBus
from time import sleep

AM2315_I2CADDR = 0x5C
AM2315_READREG = 0x03

def calculate_crc(buffer,blength):
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

# uint16_t am2315_crc16(unsigned char *ptr, unsigned char len) {
# 	unsigned short crc = 0xFFFF;
# 	unsigned char i;
	
# 	while(len--) {
# 		crc ^= *ptr++;
# 		for(i = 0; i < 8; i++) {
# 			if(crc & 0x01) {
# 				crc >>= 1;
# 				crc ^= 0xA001;
# 			} else {
# 				crc >>= 1;
# 			}
# 		}
		
# 	}
# 	return crc;
# }


bus = SMBus(1)

while True:
	try:
		bus.write_byte_data(AM2315_I2CADDR,AM2315_READREG,0)
		sleep(0.09)
		bus.write_i2c_block_data(AM2315_I2CADDR,AM2315_READREG,[0x00,0x04])
		sleep(0.09)
		tmp = bus.read_i2c_block_data(AM2315_I2CADDR,AM2315_READREG, 8)
		print(tmp)
		humidity = ((tmp[2] << 8) | tmp[3]) / 10.0
		temperature = (((tmp[4] & 0x7F) << 8) | tmp[5]) / 10.0
		print("t/f",temperature,humidity)

		crc_res = calculate_crc(tmp,6)
		crc = (tmp[7] << 8) + tmp[6]

		print("CRC_res:",crc_res)
		print("CRC", crc)
		print(crc==crc_res)

		sleep(8)

	except Exception as e:
		print(e)


# uint16_t crc_res = am2315_crc16(buf, 6);
# 	uint16_t crc = (buf[7] << 8) + buf[6];
		
# 	DEBUG("tmp: %f\n", *temperature);
# 	DEBUG("hum: %f\n", *humidity);
# 	DEBUG("crc: %i\n", crc);
# 	DEBUG("crc_res: %i\n", crc_res);
# 	DEBUG("crc_ok: %i\n", crc_res == crc);
		
# return crc_res == crc;



def calculate_crc(buffer,blength):
	crc = 0xFFFF
	blength = blength - 1 
	while blength:
		blength = blength - 1
		if crc & 0x01:
			crc = crc >> 1
			crc = crc ^ 0xA001
		else:
			crc = crc >> 1

	return crc
