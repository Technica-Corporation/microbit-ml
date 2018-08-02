import radio
from microbit import display,Image,sleep
radio.on()
while True:
 incoming=radio.receive()
 if incoming=='flash':
  display.show(Image.SKULL)
  sleep(1000)
  display.clear()
