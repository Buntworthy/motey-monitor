# Motey Monitor
### A house data logging system

<!-- MarkdownTOC depth=3 -->

- [Overview](#overview)
    - [Aim](#aim)
    - [Things to use:](#things-to-use)
    - [List of sensors:](#list-of-sensors)
- [Temperature sensors](#temperature-sensors)
- [Hub](#hub)
- [Database](#database)
    - [Structure](#structure)

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

## Hub

Raspberry Pi connected to Moteino. Moteino receives RF temperature readings, communicates to Pi over serial port. Pi updates MySQL database via calls to a PHP script. Pi code written in Python to monitor serial port and report to database. Plugged into power supply.

## Database

### Structure

Temperature database fields:

- Datetime
- ID (-> relate to friendly name in a config file etc)
- Temperature
- Humidity