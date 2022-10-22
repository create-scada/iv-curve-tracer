import analogio

class Pico_ADC:

    def __init__(self, pin):

        self.pin = pin
        self.adc = analogio.AnalogIn(self.pin)

    def get_vref(self):

        return self.adc.reference_voltage

    def get_voltage(self):

        result = self.adc.value / 65535 * self.adc.reference_voltage

        return result