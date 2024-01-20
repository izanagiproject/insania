from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Sensor:
    objid: int
    device: str
    sensor: str
    status: str
    status_raw: int

    @staticmethod
    def from_dict(obj: Any) -> 'Sensor':
        _objid = int(obj.get("objid"))
        _device = str(obj.get("device"))
        _sensor = str(obj.get("sensor"))
        _status = str(obj.get("status"))
        _status_raw = int(obj.get("status_raw"))
        return Sensor(_objid, _device, _sensor, _status, _status_raw)

@dataclass
class Root:
    treesize: int
    sensors: List[Sensor]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _treesize = int(obj.get("treesize"))
        _sensors = [Sensor.from_dict(y) for y in obj.get("sensors")]
        return Root(_treesize, _sensors)

# Example Usage
# myjsonstring = '{"prtg-version":"17.4.36.3595","treesize":2,"sensors":[{"objid":9508,"device":"PT_Specimen (172.21.87.67) [Speciment Laboratory Room]","sensor":"SSL Certificate Sensor (Port 443)","status":"Down","status_raw":5},{"objid":9510,"device":"KPPSMP_CONVERTER_WATER_PLC (Device) [Cisco Device Cisco IOS]","sensor":"SSL Certificate Sensor (Port 443)","status":"Down","status_raw":5}]}'
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)

# for sensor in root.sensors:
#     print(sensor.device)
#     print(sensor.status)
