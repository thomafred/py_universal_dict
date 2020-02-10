# -*- coding: utf-8 -*-
"""UniversalDict example

License:
    MIT License

    Copyright (c) 2020 Thomas Li Fredriksen

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

from universal_encoder import UniversalDict, universal_dict
import json


@universal_dict('SensorSample', ['timestamp', 'value'])
class SensorSample(object):
    """Simple sensor-value with associated timestamp
    """

    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

    def __str__(self):
        return '{:3f}s: {:3f}'.format(self.timestamp, self.value)

    def __repr__(self):
        return 'SensorSample[{:3f}s;{:3f}'.format(self.timestamp, self.value)


@universal_dict('SensorHistory', ['sensor_name', 'samples'])
class SensorHistory(object):
    """Sensor series
    """

    def __init__(self, sensor_name, samples=[]):
        self.sensor_name = sensor_name
        self.samples = samples

    def add_sample(self, timestamp, value):
        self.samples.append(SensorSample(timestamp, value))


# Create simple sensor sample

ss = SensorSample(123, 3.14)

# Encode sample as json using stock json-library
encoded_json = json.dumps(ss.encode(), indent=2)

print("Encoded sample as JSON:")
print(encoded_json)

# Decode sample

ss_decoded = UniversalDict.decode(json.loads(encoded_json))

assert(ss.timestamp == ss_decoded.timestamp)
assert(ss.value == ss_decoded.value)

print(repr(ss_decoded))

# Create series of sensor samples

hist = SensorHistory('MockSensor')
hist.add_sample(1, 101)
hist.add_sample(2, 102)
hist.add_sample(3, 103)
hist.add_sample(4, 104)

# Encode history as json using stock json-library
encoded_json = json.dumps(hist.encode(), indent=2)

print("Encoded history as JSON:")
print(encoded_json)

hist_decoded = UniversalDict.decode(json.loads(encoded_json))

for ref, decoded in zip(hist.samples, hist_decoded.samples):
    assert(ref.timestamp == decoded.timestamp)
    assert(ref.value == decoded.value)

print("Everything went as expected")
