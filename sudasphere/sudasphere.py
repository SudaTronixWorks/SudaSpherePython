# MIT LICENCE
# GW FW version and node FW version is totally optional

import json
import uuid
from datetime import datetime, timezone,timedelta
import paho.mqtt.client as mqtt


class Sudasphere:

    def __init__(self, userid: str, token: str, gateway_id: str | None = None, node_id: str | None = None, gateway_fw: str = "1.0.0",
        node_fw:    str        = "1.0.0",
        device_id:  str | None = None,
        device_fw:  str        = "1.0.0",
        port:         int  = 1883,
        auto_connect: bool = True,
    ):
 
        if device_id is not None:
            self.mode      = "standalone"
            self.device_id = device_id
            self.device_fw = device_fw
            self.topic     = f"sl/{device_id}/data"

        elif gateway_id is not None and node_id is not None:
            self.mode       = "p2p"
            self.gateway_id = gateway_id
            self.node_id    = node_id
            self.gateway_fw = gateway_fw
            self.node_fw    = node_fw
            self.topic      = f"gw/{gateway_id}/node/{node_id}/data"

        else:
            raise ValueError(
                "Provide device_id for standalone mode, "
                "or gateway_id + node_id for P2P mode."
            )

        self.broker  = "app.sudatronix.com"
        self.port    = port
        self.sensors = []


        self.client = mqtt.Client(client_id=f"sudasphere-{uuid.uuid4()}")
        self.client.username_pw_set(userid, token)

        if auto_connect:
            self.connect()

    def connect(self):

        self.client.on_connect = self._on_connect
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def disconnect(self):

        self.client.loop_stop()
        self.client.disconnect()


    def _on_connect(self, client, userdata, flags, rc):

        if rc == 0:

            print(f"[SUDASPHERE] Connected  mode={self.mode}  topic={self.topic}")
        else:

            print(f"[SUDASPHERE] Connection failed  rc={rc}")


    def add(self, sensor_type: str, value, unit: str = "-", sensor_id: str | None = None):
       
        if sensor_id is None:
            sensor_id = f"s{len(self.sensors) + 1}"

        self.sensors.append({"id": sensor_id, "type":  sensor_type, "value": value, "unit":  unit})

    def clear(self):
      
        self.sensors = []


    def publish(self, rssi: int | None = None):

        if not self.sensors:
            print("[SUDASPHERE] Nothing to publish — call add() first")
            return

        now = datetime.now(timezone.utc).isoformat()

        if self.mode == "standalone":
            payload = {"timestamp": now, "device_id": self.device_id, "device_fw": self.device_fw, "sensors":   self.sensors }

        else:
            payload = {"timestamp":  now, "gateway_id": self.gateway_id, "gateway_fw": self.gateway_fw, "node_id":    self.node_id, "node_fw":    self.node_fw, "rssi": rssi, "sensors":    self.sensors}

        result = self.client.publish(self.topic, json.dumps(payload, separators=(",", ":")))

        print(payload)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[SUDASPHERE] Published {len(self.sensors)} sensor(s)  →  {self.topic}")

        else:
            print(f"[SUDASPHERE] Publish failed  rc={result.rc}")

        self.clear()