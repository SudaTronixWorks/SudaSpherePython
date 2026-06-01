import json
import uuid
from datetime import datetime, timezone
import paho.mqtt.client as mqtt


class Sudasphere:

    def __init__(
        self,
        userid,
        token,
        gateway_id,
        node_id,
        port=1883,
        gateway_fw="1.0.0",
        node_fw="1.0.0",
        auto_connect=True
    ):

        self.broker ="app.sudatonix.com",
        self.port = port

        self.gateway_id = gateway_id
        self.node_id = node_id

        self.gateway_fw = gateway_fw
        self.node_fw = node_fw

        self.topic = f"gw/{gateway_id}/node/{node_id}/data"

        self.client = mqtt.Client(
            client_id=f"sudasphere-{uuid.uuid4()}"
        )

        self.client.username_pw_set(userid, token)

        self.sensors = []

        if auto_connect:
            self.connect()

    def connect(self):

        self.client.on_connect = self._on_connect

        self.client.connect(
            self.broker,
            self.port
        )

        self.client.loop_start()

    def disconnect(self):

        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client, userdata, flags, rc):

        if rc == 0:
            print("[SUDASPHERE] Connected")
        else:
            print(f"[SUDASPHERE] Failed: {rc}")


    def add(self, sensor_type, value, unit="-", sensor_id=None):

        if sensor_id is None:
            sensor_id = f"s{len(self.sensors)+1}"

        self.sensors.append({
            "id": sensor_id,
            "type": sensor_type,
            "value": value,
            "unit": unit
        })

    def clear(self):

        self.sensors = []


    def publish(self, rssi=None):

        payload = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "gateway_id": self.gateway_id,
            "gateway_fw": self.gateway_fw,

            "node_id": self.node_id,
            "node_fw": self.node_fw,

            "rssi": rssi,
            "sensors": self.sensors
        }

        payload_json = json.dumps(
            payload,
            separators=(",", ":")
        )

        result = self.client.publish(
            self.topic,
            payload_json
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print("[SUDASPHERE] Published")
        else:
            print("[SUDASPHERE] Publish Failed")

        self.clear()