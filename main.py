#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import math

class PowerSteer(DriveBase):
    def __init__(self, left_motor, right_motor, steering_motor, wheel_diameter, axle_track, wheel_base):
        self.wheel_diameter = wheel_diameter
        self.axle_track = axle_track
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.wheel_base = wheel_base
        self.steering_motor = steering_motor

    def drive(self, speed, steering):
        circumferance = self.wheel_diameter * math.pi
        degrees_per_second = (speed / circumferance) * 360

        if steering != 0:
            turn_radius = self.wheel_base / math.sin(math.radians(math.fabs(steering)))
            outer_drive_factor = turn_radius + self.axle_track
            inner_drive_factor = turn_radius - self.axle_track
            outer_motor_multiplier = outer_drive_factor / inner_drive_factor
            print(outer_motor_multiplier)
            if steering > 0:
                self.right_motor.run(degrees_per_second * outer_motor_multiplier)
                self.left_motor.run(degrees_per_second)
            elif steering < 0:
                self.left_motor.run(degrees_per_second * outer_motor_multiplier)
                self.right_motor.run(degrees_per_second)
        else:
            self.left_motor.run(degrees_per_second)
            self.right_motor.run(degrees_per_second)

        self.steering_motor.run_target(70,steering)
            

# Write your program here
brick.sound.beep()

left = Motor(Port.C, Direction.COUNTERCLOCKWISE)
right = Motor(Port.B, Direction.COUNTERCLOCKWISE)
steering = Motor(Port.A)
robot = PowerSteer(left, right, steering, 40, 95, 150)

while True:
    robot.drive(100,30)
    wait(5000)
    robot.drive(100,0)
    wait(5000)
    robot.drive(100,-30)
    wait(5000)