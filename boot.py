import board
import digitalio
import storage

write_pin = digitalio.DigitalInOut(board.GP13)
write_pin.direction = digitalio.Direction.INPUT
write_pin.pull = digitalio.Pull.UP

# GND is programming mode
# Floating is run mode
if write_pin.value:
    storage.remount("/", readonly=False)
