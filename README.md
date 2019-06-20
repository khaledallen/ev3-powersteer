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
## Explanation for Students

The file `main.py` contains both the class definition and a simple example of how to use the class. For now, the simplest way to implement it is to simply copy and paste the class definition into your own `main.py` (make sure to include `import math`, since microPython doesn't import it by default).

The first line `class PowerSteer(DriveBase)` tells the program to define a new class called `PowerSteer` inheriting everything from the `DirveBase` class that comes from the `pybricks.robotics` module. If we stopped at that line, any new `PowerSteer` object would be exactly the same as a `DriveBase` object.

Any functions we define in the `class PowerSteer` block will be added on top of functions that come from `DriveBase`, and if they have the same name as `DriveBase` functions, they will overwrite them. For example, `DriveBase` already has an `__init__` function, so when we define `__init__` in this file, it replaces the one in `DriveBase`.

The first function `__init__` tells the program what to do when a new `PowerSteer` object is initialized. In this case, all it does is assign some attributes to the object, so that the robot knows its wheel diameter, axle length, drivebase length, and which motors do what. We need a new one here because the `DriveBase.__init__` doesn't do anything with `drivebase` and doesn't have space for `steering_motor`.

The real magic happens in the `drive` function. Note that this function is meant to perform exactly the same  as the default `drive` function that comes with the `DriveBase` class, but since we are moving the steering functions away from the drive motors, we need to change how the robot calculates its turn and power. 

```
def drive(self, speed, steering):
    circumferance = self.wheel_diameter * math.pi
    degrees_per_second = (speed / circumferance) * 360

    if steering != 0:
        turn_radius = self.wheel_base / math.sin(math.radians(math.fabs(steering)))
        outer_drive_factor = turn_radius + self.axle_track
        inner_drive_factor = turn_radius - self.axle_track
        outer_motor_multiplier = outer_drive_factor / inner_drive_factor
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
```

First, note that the way you call the function is exactly the same as how you would call `DriveBase.drive()`. You give it a speed in mm/s and a steering angle in deg/sec (the `self` paramter is hidden when the function is used outside the class definition).

The circumference is calculted from the wheel diameter and used to figure out how fast the wheel will need to turn to match the desired speed.

Next, the function checks if you wanted to turn at all (`if steering != 0`). If we don't need to turn, we don't want to waste time on all the calculations it would take to figure out the steering, so we skip ahead to the `else` statement and just turn on the drive motors at the right deg/sec.

If we do want steering, we need to figure out the turn radius and then figure out how much farther the outer wheel has to travel compared to the inner wheel (`outer_motor_multiplier`). Then, depending on whether we are turning left (positive steering angle) or right (negative steering angle), we apply that adjustment to the appropriate motor and set the other motor to the base deg/sec speed.

In all cases, we should apply the desired steering angle to the steering motor, on the last line, even if it is 0, since otherwise the robot would not straighten out when instructed too.
