import time
import random
from sudasphere import Sudasphere

# Don't forget to get your token and user ID from the platform
# sudasphere.sudatronix.com


# define a standalone devices
device = Sudasphere(userid="YOUR_USER_ID", token="YOUR_TOKEN", gateway_id="YOUR_GATEWAY_ID", node_id="YOUR_NODE_ID")


# demo while(true) loop program
try:

    while True:

        battery = random.randint(65, 100)

        # To add a sensor user device.add(sensor_type, value, unit)

        device.add(sensor_type="ambient_temperature", value=round(26.2, 2), unit="C")

        device.add(sensor_type="relative_humidity",value=round(60, 2),unit="%")

        device.add(sensor_type="battery_level", value=battery, unit="%" )

        device.publish()

        time.sleep(5)


except KeyboardInterrupt:

    print("\nStopping standalone device...")

    device.disconnect()

    print("Disconnected cleanly.")