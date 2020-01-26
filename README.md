---
title: 'Infotecs test task'

---

Infotecs Test Task
===

## Table of Contents
* [Infotecs Test Task](#Infotecs-Test-Task)
     * [Table of Contetns](#Table-of-Contetns)
     * [Test task description](#Test-task-description)
     * [Avaliable methods](#Avaliable-methods)
         * [Get by geonameid](#Get-by-geonameid)
         * [Get cities info list](#Get-cities-info-list)
         * [Compare cities by name](#Compare-cities-by-name)
     * [Additional tasks](#Additional-tasks)


##  Test task description

Implement an HTTP server to provide information on geographical objects.


> Take data from the GeoNames geographical database by clicking the link: http://download.geonames.org/export/dump/RU.zip.

> Description of the data format can be found at the link:
http://download.geonames.org/export/dump/readme.txt

## Getting started
Get yourself a copy and start the server by pasting the following lines into your terminal:

``` 
git clone https://github.com/kirpastuhov/infotecs_test_2.git Pastukhov_Python
cd Pastukhov_Python
python3 server.py
```

Make sure that RU.txt file is present in folder with the server

## Avaliable methods

#### Get by geonameid

The method accepts the geonameid identifier and returns information about the city.


![](https://i.imgur.com/m2MnrVh.png)

---

#### Get cities info list
The method accepts the page and the number of cities displayed on the page and returns the list of cities with their information. 


![](https://i.imgur.com/LyZXJso.png)

---

#### Compare cities by name
The method accepts the names of two cities (in Russian) and gets the information about the found cities, as well as additional information: which one is located to the north and whether they have the same time zone (when several cities have the same name, to resolve ambiguity by choosing a city with a large population; if the population is the same, take the first caught).


![](https://i.imgur.com/HR4z2sy.png)

## Additional tasks:
Additional tasks are not required, and will be taken into account if a very large number of candidates have completed the main task on excellent. You can perform any combination of the proposed tasks.
1. For the 3rd method to show the user not only the difference in time zones, but also how many hours they differ.
Implemented in [Compare cities by name](#Compare-cities-by-name) method
3. Implement a method where the user enters a part of the city name and returns a hint with possible extensions.
Shows suggestions if city name was not found in [Compare cities by name](#Compare-cities-by-name) method and [Get cities info list](#Get-cities-info-list)
![](https://i.imgur.com/yC7QPpp.png)

