#!/usr/bin/env python3
from gpiozero import Button, LED
import os 
from signal import pause
import subprocess

powerPin = 25
resetPin = 27 
ledPin = 24 
powerenPin = 26 
hold = 1
led = LED(ledPin)
led.on()
power = LED(powerenPin)
power.on()

#functions that handle button events
def when_pressed():
 led.blink(.2,.2)
 output = int(subprocess.check_output(['/opt/RetroFlag/multi_switch.sh', '--es-pid']))
 if output:
     os.system("/opt/RetroFlag/multi_switch.sh --es-poweroff")
 else:
     os.system("sudo shutdown -h now")
    
def when_released():
 led.on()

def reboot():
 output = int(subprocess.check_output(['/opt/RetroFlag/multi_switch.sh', '--es-pid']))
 output_rc = int(subprocess.check_output(['/opt/RetroFlag/multi_switch.sh', '--rc-pid']))
 if output_rc:
     os.system("/opt/RetroFlag/multi_switch.sh --closeemu")
 elif output:
     os.system("/opt/RetroFlag/multi_switch.sh --es-restart")
 else:
     os.system("sudo reboot")
 
btn = Button(powerPin, hold_time=hold)
rebootBtn = Button(resetPin)
rebootBtn.when_pressed = reboot 
btn.when_pressed = when_pressed
btn.when_released = when_released
pause()