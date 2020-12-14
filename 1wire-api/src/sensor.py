
class SensorValue:

    def __init__(self, valueType: str, units: str, value):
        self._valueType = valueType
        self._units = units
        self._value = value

    def __str__(self):
        if self._value is not None:
            return f"{self._valueType}: {self._value:.2f} {self._units}"
        return f"{self._valueType}: null"

    def __rerp__(self):
        return self.__str__()

    def offset(self, offset):
        if self._value is None:
            return
        self._value = self._value + offset

    @property
    def name(self):
        return self._valueType

    @property
    def value(self):
        return self._value

    @property
    def units(self):
        return self._units

    def json(self):
        out = {}
        if self._valueType is not None:
            out["type"] = self._valueType
        if self._units is not None:
            out["units"] = self._units
        if self._value is not None:
            out["value"] = self._value
        else:
            out["value"] = None
        return out

class TempValue(SensorValue):
    def __init__(self, value: float):
        SensorValue.__init__(self, "temp", "C", value)

class RowSensor:

    def __init__(self, sensorId: str):
        self._values = []
        self._sensorId = sensorId
        self._name = None

    @property
    def id(self):
        return self._sensorId
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def addTempValue(self, value):
        val = TempValue(value)
        self._values.append(val)

    def offsetValue(self, name, offset):
        for v in self._values:
            if v.name == name:
                v.offset(offset) 

    def valueUnits(self, name):
        for v in self._values:
            if v.name == name:
                return v.units
        return None

    def value(self, name):
        for v in self._values:
            if v.name == name:
                return v.value
        return None

    def json(self):
        out = {}
        out["sensorId"] = self._sensorId
        if self._name is not None:
            out["name"] = self._name
        if len(self._values) > 0:
            out["values"] = []
            for v in self._values:
                out['values'].append(v.json())
        return out


    def __str__(self):
        if len(self._values) == 1:
            v = self._values[0]
            return f"id: {self.name} {v}"
        values = ', '.join([ str(x) for x in self._values] )
        return f"id: {self._sensorId} [{values}]"

class TempSensor(RowSensor):
    def __init__(self, sensorId :str, value: float):
        RowSensor.__init__(self, sensorId)
        self.addTempValue(value)


if __name__ == "__main__":
    val = SensorValue("temp", "C", 1231.3232)
    print(val)
    val.offset(-1200)
    print(val)
    print(val.name)


    s = RowSensor("1111")
    s.name = "senser1"
    s.addTempValue(23.2)
    s.offsetValue("temp", 1000)
    print(s)
    print(s.json())
    
    t1 = TempSensor("2222", 23.1)
    print(t1)

    t1 = TempSensor("3333", 10.3)
    print(t1.name)
    print(t1.json())
    print(t1.valueUnits("temp"))