import random
import time

from sudasphere import Sudasphere

device = Sudasphere(
    broker="178.128.101.114",
    userid="YOUR_USERNAME",
    token="YOUR_PASSWORD",
    gateway_id="home-gateway",
    node_id="kitchen-node"
)

while True:

    temperature = random.uniform(25, 32)
    humidity = random.randint(60, 90)

    device.add(
        "temperature",
        round(temperature, 2),
        "C"
    )

    device.add(
        "humidity",
        humidity,
        "%"
    )

    device.add(
        "status",
        "online"
    )

    device.publish(
        rssi=-52
    )

    time.sleep(5)