import time
import sys
import serial
from statistics import mean

import bme680
import mh_z19

from db import SensorData

ser = serial.Serial("/dev/ttyUSB0", 9600)


# Im a comment for testing
db_url = "mysql+pymysql://admin:admin@localhost:3306/sensor_data"


sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)  # 0x77

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

interval = 10
interval = int(sys.argv[1])
num_of_data_points = 0
co2_vals = []
temp_vals = []
pressure_vals = []
humidity_vals = []
dust_vals = []


def traffic_light_check(co2, pressure, dust):
    pass


start_time = time.time()
try:
    while True:
        try:
            co2 = mh_z19.read()["co2"]
        except KeyError:
            co2 = 0
        if sensor.get_sensor_data():
            temperature = round(sensor.data.temperature)
            pressure = round(sensor.data.pressure)
            humidity = round(sensor.data.humidity)
            dust = float(ser.readline())
            print(co2, temperature, pressure, humidity, dust)

            co2_vals.append(co2)
            temp_vals.append(temperature)
            pressure_vals.append(pressure)
            humidity_vals.append(humidity)
            dust_vals.append(dust)

            num_of_data_points += 1
            # output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(
            #     sensor.data.temperature, sensor.data.pressure, sensor.data.humidity
            # )
            # print(
        end_time = time.time()

        if end_time - start_time > 600:
            co2_mean = mean(co2_vals)
            temperature_mean = mean(temp_vals)
            humidity_mean = mean(humidity_vals)
            pressure_mean = mean(pressure_vals)
            dust_mean = mean(dust_vals)

            co2_vals = []
            temp_vals = []
            humidity_vals = []
            pressure_vals = []
            dust_vals = []

            new_sensor_data = SensorData(
                co2=co2_mean,
                temperature=temperature_mean,
                humidity=humidity_mean,
                pressure=pressure_mean,
                dust=dust_mean,
            )

            new_sensor_data.save()

        time.sleep(interval)
except KeyboardInterrupt:
    print(f"Total number of iterations: {num_of_data_points}")
