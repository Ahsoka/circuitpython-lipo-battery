from ulab import numpy as np
from . import voltage_curves

import microcontroller
import analogio

try:
    import typing
except ImportError:
    pass


class Lipo:
    def __init__(
        self,
        voltage_pin: microcontroller.Pin,
        voltage_ratio: float,
        battery_type: typing.Literal['1S', '2S', '3S', '4S', '5S', '6S']
    ):
        if battery_type not in {'1S', '2S', '3S', '4S', '5S', '6S'}:
            raise ValueError(
                f"battery_type must be 1S, 2S, 3S, 4S, 5S, 6S, not '{battery_type}'"
            )
        self.adc = analogio.AnalogIn(voltage_pin)
        self.voltage_ratio = voltage_ratio
        self.battery_type = battery_type

    @property
    def voltage(self) -> float:
        return (np.interp(
            self.adc.value, [0, 2**16 - 1], [0, self.adc.reference_voltage]
        ) * self.voltage_ratio)[0]

    @property
    def percent(self) -> float:
        return np.interp(
            self.voltage,
            voltage_curves[self.battery_type],
            list(range(0, 101, 5))
        )[0]

    @property
    def low_battery(self) -> bool:
        return self.percent < 15
