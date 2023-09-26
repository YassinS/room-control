import time
import sys
import serial

import bme680
import mh_z19

from db import SensorData

ser = serial.Serial("/dev/ttyUSB0", 9600)

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

interval = int(sys.argv[1])
num_of_data_points = 0

try:
    while True:
        co2 = mh_z19.read()["co2"]
        print(co2)
        if sensor.get_sensor_data():
            temperature = round(sensor.data.temperature)
            pressure = round(sensor.data.pressure)
            humidity = round(sensor.data.humidity)
            print(temperature, pressure, humidity)
            dust_mg_per_m3 = float(ser.readline())
            new_sensor_data = SensorData(
                co2=co2, temperature=temperature, humidity=humidity, pressure=pressure
            )

            new_sensor_data.save()
            num_of_data_points += 1
            # output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(
            #     sensor.data.temperature, sensor.data.pressure, sensor.data.humidity
            # )
            # print(output)

        time.sleep(interval)
except KeyboardInterrupt:
    print(f"Total number of iterations: {num_of_data_points}")
