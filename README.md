# microbit-ml
IoT Machine Learning: Vibrational Anomaly Detection using Tri-Axial Accelerometer Data

## Introduction
From bridges to cranes to servers to trains, the modern world is filled with essential equipment and infrastructure. Breakages endanger safety, halt operations, and incur high financial costs. Intelligent vibration analysis enables preventative maintenance, detecting degradation or faults before disaster strikes. Combining this algorithm with Internet of Things (IoT) technology allows for sensitive analytics on easily deployable, inexpensive, small form-factor devices. 

This project introduces a statistics-based, time-series Vibrational Anomaly Detection algorithm that relies on extreme memory efficiency to fit onto highly constrained devices. Many other machine learning algorithms are too resource intensive to fit inference on severely resource-constrained devices. However, this project fits both the training and inference phases on a true edge device while running analytics in real time. The development and testing was run on the BBC Micro:bit. This device runs at only 16MHz with only 16kb of RAM, classifying the device as a Class I IoT device. 

## Algorithm Overview

An accelerometer captures tri-axial accelerometer data accounting for the x, y, and z dimensions in a series of time windows. These data points within each window are manipulated into a collection of features used to detect anomalies. Features include averages, mins, maxes, and frequencies for x, y, and z data as well as magnitude, which takes each dimension into consideration.

To fit within the tight memory constraints, training is broken into two phases. Phase I collects data for a configurable number of training windows and computes the averages. Phase II uses these averages and, using incoming data, computes the standard deviations for each feature. Again, the number of training windows is configurable. Finally, an infinite inference loop analyzes new time windows, computes averages, and determines how many standard deviations the new value is from the trained average. If this z-score value is greater than a threshold, that feature is marked as suspicious. If the number of suspicious features exceeds a threshold, an anomaly is reported.  
In this project, an anomalous event triggers a radio transmission. This message is received by another Micro:bit, which flashes its LED grid to notify a human. 


## Hardware Requirements

This code was designed for a BBC Micro:bit. This repo involves a system of two microbits working together; one runs anomally detection and the other listens for radio transmissions containing alerts. The second device lights up its LED screen (in this case with a skull image) to alert a human. 

Using only one Micro:bit -- Comment out the radio transmission functions in vib_detecion_mini_d1.py 
Using different hardware -- Comment out the radio transmission functions, as these are micro:bit specific. Commend out all LED display functions. (Note that this project requires micropython on-device to run)
