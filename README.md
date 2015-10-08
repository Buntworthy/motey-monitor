# Motey Monitor
### A house data logging system

<!-- MarkdownTOC depth=3 -->

- Overview
    - Aim
    - Things to use:
    - List of sensors:
- Temperature sensors
    - Web temperature
- Hub
- Database
    - Structure
    - PHP updates

<!-- /MarkdownTOC -->

## Overview

### Aim
Logging data in a house, storing in server database, visualisation on the web. 

### Things to use:

- Sensors nodes - Moteino
- Hub - Raspberry Pi + Moteino
- Database - MySQL hosted on Dreamhost (update via PHP)
- Web visualisation - D3.js + PHP

### List of sensors:

- Temperature sensors x5 (2x bedroom, bathroom, kitchen, living room)
- Web sensor (Outside temperature)
- Electricity sensor
- Hot water sensor

![Overview plan](/Images/monitor_plan.png)

## Temperature sensors

Moteino using RF for communication to the hub, DHT-22 for temperature and humidity measurments, AAA(?) batteries for power, 3D printed case.

### Web temperature

Using openweathermap.org API for grabbing current conditions in Cambridge.

## Hub

Raspberry Pi connected to Moteino. Moteino receives RF temperature readings, communicates to Pi over serial port. Pi updates MySQL database via calls to a PHP script. Pi code written in Python to monitor serial port and report to database. Plugged into power supply.

## Database

### Structure

Temperature database fields:

- datetime
- id (-> relate to friendly name in a config file etc)
- temp
- rh *Currently not implemented*

### PHP updates

http://cutsquash.com/get_week.php?key=KEY_GOES_HERE

*Returns past week of readings in json format*

http://cutsquash.com/add-reading.php?key=KEY_GOES_HERE&date=2015-10-2+15%3A35%3A15&ID=hall&temp=23.57&rh=65.87

*Adds a single reading to the temperature database. (Date needs to be formatted correctly)*
