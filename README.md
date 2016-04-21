# Simple_AM2315
Python code to use the AM2315 Temp and Humidity sensor with a CHIP, Raspberry Pi, or BeagleBone black.

This requires the Adafruit_Python_GPIO library to work:
[CHIP](https://github.com/xtacocorex/Adafruit_Python_GPIO)
[RPi/BBB](https://github.com/adafruit/Adafruit_Python_GPIO)

- To install:

 ```
 git clone https://github.com/xtacocorex/Simple_AM2315.git
 cd Simple_AM2315
 sudo python setup.py install
 ```

- To Use:

```
 from am2315 import AM2315
 sens = AM2315.AM2315()
 sens.read_temperature()
 sens.read_humidity()
 sens.read_humidity_temperature()
```

