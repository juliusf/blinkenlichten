
upload:
	ampy --port /dev/ttyUSB0 --baud 115200 put main.py
	ampy --port /dev/ttyUSB0 --baud 115200 put test.py
run:
	ampy --port /dev/ttyUSB0 --baud 115200 run test.py

all:
	upload run
