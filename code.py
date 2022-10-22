from iv_curve_tracer import IV_Curve_Tracer
from tmcs1108 import Tmcs1108
from pico_adc import Pico_ADC
from mcp4921 import Mcp4921
import RGB1602
import os

import board
import digitalio
import busio
import time

try:
    os.mkdir('/data')
except:
    pass

btn = digitalio.DigitalInOut(board.GP12)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

pv_voltage_sensor = Pico_ADC(board.GP26)

scale_factor = .2
voltage_offset_factor = 0.1
pv_adc = Pico_ADC(board.GP27)
pv_current_sensor = Tmcs1108(pv_adc, scale_factor, voltage_offset_factor)


dac_spi_clk_pin=board.GP2
dac_spi_cs_pin=board.GP5
dac_spi_data_pin=board.GP3
dac_latch_pin=board.GP1

dac_spi = busio.SPI(dac_spi_clk_pin, MOSI=dac_spi_data_pin)
dac_cs = digitalio.DigitalInOut(dac_spi_cs_pin)
dac_latch = digitalio.DigitalInOut(dac_latch_pin)

dac_cs.direction = digitalio.Direction.OUTPUT
dac_latch.direction = digitalio.Direction.OUTPUT

while not dac_spi.try_lock():
    pass
dac_spi.configure(baudrate=500_000, phase=0, polarity=0)

dac = Mcp4921(dac_spi, dac_cs, dac_latch)

iv_curve_tracer = IV_Curve_Tracer(pv_voltage_sensor,
                                  pv_current_sensor,
                                  dac)

led.value = True

lcd=RGB1602.RGB1602(16,2)
lcd.setRGB(255, 255, 255);
lcd.setCursor(0, 0)
lcd.printout("READY")

while True:

    if btn.value:
        continue

    lcd.setCursor(0, 0)
    lcd.printout("READING")
    led.value = False

    results = iv_curve_tracer.run()

    with open('num.txt') as f:
        num = f.read()
        num = num.strip()
        num = int(num)
        num += 1

    try:

        with open('num.txt', 'w') as f:
            f.write(str(num))

        with open(f'/data/reading{num}.csv', 'w') as fp:

            fp.write('Voltage, Current\n')

            for (voltage, current) in results:
                line = f'{voltage},{current}\n'
                fp.write(line)

            fp.flush()
    except Exception as e:

        print(e)
        lcd.setCursor(0, 0)
        lcd.printout(f"FILE WRITE ERROR")
        time.sleep(3)

    else:

        lcd.setCursor(0, 0)
        lcd.printout(f"WROTE {num}")
        led.value = True
        time.sleep(3)

    lcd.setCursor(0, 0)
    lcd.printout(f"READY")
