## TODO

- [ ] Confirm the turn radius measurements
- [ ] Confirm the differential drive calculations are correct
- [ ] Extend to handle front- and rear-wheel drive

# ev3 Powersteering

An extension of the LEGO microPython Drivebase class that adds support for a dedicated steering motor.

## Requirements

This class requires the LEGO microPython framework installed on your ev3 brick, since it is based on the robotics.DriveBase class. 

* [Instructions for installed microPython on LEGO Education Website](https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3)
* [Direct Link to the EV3 microSD card image](https://le-www-live-s.legocdn.com/sc/media/files/ev3-micropython/ev3micropythonv100sdcardimage-4b8c8333736fafa1977ee7accbd3338f.zip)
* [Direct Link to the EV3 microPython documentation](https://le-www-live-s.legocdn.com/sc/media/files/ev3-micropython/ev3micropythonv100-71d3f28c59a1e766e92a59ff8500818e.pdf)

## Usage

The function template is
`class PowerSteer(left_motor, right_motor, steering_motor, wheel_diameter, axle_width, drivebase)`

- `left_motor` - A LEGO ev3 motor class (`Motor(Port.[A-D])`, associated with the physical motor powering the left drive wheel.
- `right_motor` - A LEGO ev3 motor class (`Motor(Port.[A-D])`, associated with the physical motor powering the right drive wheel.
- `steering_motor` - A LEGO ev3 motor class (`Motor(Port.[A-D])`, associated with the physical motor powering the steering column.
- `wheel_diameter` - wheel diameter of the drive wheels in millimeters
- `axle_width` - distance between the steering wheels in millimeters
- `drivebase` - distance from the drive wheels to the steering wheels in millimeters

To instantiate a powersteering robot, create a new `PowerSteer` class with the appropriate measurements for the various dimensions of the robot.

You may need to adjust the direction of the steering motor depending on its arrangement.

### example

For a robot with wheel diameter 40mm, axle legnth 95mm, and drivebase 150mm, and the drive motors facing "backwards": 

```
left = Motor(Port.C, Direction.COUNTERCLOCKWISE)
right = Motor(Port.B, Direction.COUNTERCLOCKWISE)
steering = Motor(Port.A)
robot = PowerSteer(left, right, steering, 40, 95, 150)
```

The class handles steering by extending the `DriveBase.drive()` function and offloading the steering from the drive wheels to the steering wheels. It still powers the drive wheels differently based on the turn radius and speed.

### example

To drive the robot at 100mm/s while performing a 30 degree turn

```
robot.drive(100,30)
```

