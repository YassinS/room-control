import time
import sys
import serial
from statistics import mean
import RPi.GPIO as GPIO

import bme680
import mh_z19

from db import SensorData

ser = serial.Serial("/dev/ttyUSB0", 9600)


# Im a comment for testing
db_url = "mysql+pymysql://admin:admin@localhost:3306/sensor_data"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
traffic_light_pins = [16, 20, 21]  # 16 red, 20 yellow, 21 green
for pin in traffic_light_pins:
    GPIO.setup(pin, GPIO.OUT)

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
if len(sys.argv) > 1:
    interval = int(sys.argv[1])
num_of_data_points = 0
co2_vals = []
temp_vals = []
pressure_vals = []
humidity_vals = []
dust_vals = []


def turn_traffic_lights_off():
    traffic_light_pins = [16, 20, 21]
    for pin in traffic_light_pins:
        GPIO.output(pin, GPIO.LOW)


def traffic_light_check(co2, dust):
    if (co2 > 800 or dust > 60) and (co2 < 1500 or dust < 91):
        turn_traffic_lights_off()
        GPIO.output(20, GPIO.HIGH)
    elif co2 > 1500 or dust > 91:
        turn_traffic_lights_off()
        GPIO.output(16, GPIO.HIGH)
    else:
        turn_traffic_lights_off()
        GPIO.output(21, GPIO.HIGH)


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
            try:
                dust = float(ser.readline())
            except ValueError:
                dust = 0
                print("Invalid Value!")
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

        if end_time - start_time > 60:
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

            traffic_light_check(co2_mean, dust_mean)
            new_sensor_data.save()
        time.sleep(interval)
except KeyboardInterrupt:
    print(f"Total number of iterations: {num_of_data_points}")
