# DMD-raspberry
DMD library for Raspberry PI

Instructions:

Connection pins: https://pinout.xyz/pinout/spi#
(GPIO 10, GPIO 11 SPI)
OE - GPIO12
A - GPIO26
B - GPIO20
SCLK - GPIO19

If for some reason SPI does not work for you, restart with 
sudo dtparam spi = off
sudo dtparam spi = off
