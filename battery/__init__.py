import json

# NOTE: I'm pretty sure that the current working directory
# will always be at the root level so it should be okay to
# do this.
with open('lib/battery/voltage_curves.json') as file:
    voltage_curves = json.load(file)
    for battery_type in voltage_curves:
        voltage_curves[battery_type] = list(reversed(voltage_curves[battery_type]))

from .battery import Lipo
