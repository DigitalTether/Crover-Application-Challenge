=== Software Execution ===
The program was intended to run using Python3 and Linux Ubuntu 16.04 for the ROS simulation.


=== Technical Description and Issues ===

### Summary

The final result of this effort is the Python scripts for both the local tracking algorithm itself, and the framework for a new ROS node that could be used to both simulate a car’s operation (using the given dataset) and be included in a larger ROS framework on the actual car localisation system.

Overall I believe this project did not go as well as I could have made it. I ran into several issues that, while in the course of correcting them, I spent too much time on and it affected my ability to deliver a final working piece of software.

### Issues

I had some time-consuming issues during the assessment that overall affected the quality of the final software. I’ve included details on those issues and how I dealt with them, and how I would have continued with the project if I had more time.

### ROS Simulation

I have an old laptop that I’ve used for ROS simulations in the past which I intended to use for this project. The laptop’s battery died and refused to run even when plugged in, and I couldn’t use to run the desired tests. I attempted to run Ubuntu on a second partition on my desktop but ran into some problems getting it to recognise my SSD. It was taking too long to set up so I decided to leave it there and just focus on getting what I can done.

### Quaternion Calculations

After breaking the work up I began working on finding the needed equations to find the car’s estimated orientation. I wasn’t familiar with Quaternions so I spent some time trying to understand them enough to find the car’s orientation based on the car’s velocity in both the odom and map frames. I tested my formula by copying the ground truth dataset and applying the formulas in excel, and comparing my results to the true orientation. What took up most of my time was trying to find out why most of the results seemed fairly accurate but in some cases the orientation was seeming pointing in the exact opposite direction. I eventually discovered the issue, but had already spent so much time on this part of the problem - because I saw this as an integral part to producing reliable results - that I didn’t have sufficient time to conduct testing on the program.

### Future Work

I would continue with the roadmap I outlined, and adapt as needed during testing and evaluation.

I expect there may be issues that come up during the orientation calculations. Because the positional information provided by the GNSS has a standard deviation of 0.7m, this can result in very significant different orientation results. My initial attempt to reduce this was to take a rolling average of the position from this sensor. Other work could include using the angular velocity of the car to better inform the orientation values e.g. if the angular rotation is minimal (like if it is not rotating) then the apparent orientations can’t be rotating to any significant degree despite what the GNSS says. However this is speculation at the moment without any test results, and would be something I would look into if I had the opportunity to.


=== Work Description ===

### Roadmap

- Identify key objectives and tasks
- Theory
    - Identify necessary equations
    - Test equations on ground truth dataset
- Local_Tracker Class
    - Create local_tracker class with functions
    - Test results against ground truth dataset
- Create ROS node framework
    - Create high-level descripion
    - Create and import local_tracker
- Simulation
    - Run ROS simulation and output dataset values
    - Test full simulation
    - Display results and analyse


### Start

I started by breaking down the assessment into its most important pieces: what the task is, what work is needed to be done, what is given, what is to be delivered, etc. This information is then stored in a document which can be referred back on and updated as needed.

## Task

Develop an algorithm in order to localise a car equipped with wheel encoders and a GNSS receiver, which provide linear and angular speed, and position respectively.

**Input:** Data from Sensors:

- Wheel Encoders (linear and angular wheel velocity - /odom)
- GNSS Receiver (position - /map)

**Output:** Estimated position and orientation of the car in the map frame

# Approach

For project management, I’ll be using Notion to keep the project organised. I haven’t used this software before but have started using it recently and think this would be a good opportunity to use it.

Since the job posting references some programming languages you use on the job so I’ll stick with those for the assessment. **Programming Languages:** ROS, C++, Python, Linux Ubuntu, Git. Both Python and C++ can be used for ROS nodes, but I’ll stick with Python for the time being.

I’m currently on Windows 10 at the moment and prefer to stay on this for the time being unless absolutely necessary; I have an old laptop with Linux Ubuntu and ROS installed but it has been having issues and want to avoid it where possible. But if this algorithm is meant to be installed in an existing ROS framework, I’ll need to in order to test it properly. The assessment doesn’t explicitly say this but does hint that ROS is used to generate the input data.

I’m not familiar with ROSBAG or .bag files so I may stick with the CSV files while working on Windows (since I’ve used this format before in programming), but I’ll look at the ROS doc to see what it would take to use it and if it would be worthwhile.

## Observations on input data:

The orientation is not explicitly provided to us, so we must estimate this using the ODOM and GNSS sensors.

The position is given to us by the GNSS, but it’s standard deviation of 0.7m could be better. Ideally we would use the car’s relative velocity and orientation, but this creates a cyclical dependency between orientation and position. Since orientation is not given by any sensor, we will have to rely on GNSS’ given position value. Maybe odom velocity could be used to inform position to a degree but I can’t immediately see how exactly this would be achieved.

Ground truth can’t be relied upon for normal operation (mainly for testing my algorithm), but we could include an ability to set a given position and orientation.

### ODOM:

Linear and angular speed of wheels on odom frame (standard deviation changes per record)

### GNSS:

Position of car on map frame (standard deviation: 0.7m)

### Ground Truth:

Real position and speed values. Not to be used for algorithm input but should be compared to algorithm’s results to test accuracy.

### Orientation:

I want to note that while I’ve used Quaternions before in Unity3D in the past, I haven’t modified them in this level of detail before.

Orientation is defined as a Quaternion, but since the car can only rotate on one axis and in our ground truth dataset only two orientation values change, Z and W, these will be the only values we need to focus on. The dataset also tells us that when then Orientation value is at it’s default, Quaternion identity of (0, 0, 0, 1), the car is facing along the positive X axis. This tells us that the quaternion_posW value is in the same direction as map_posX, while the quaternion_posZ is in the same direction as map_posY. This helps simplify the necessary calculations.

### Calculation Notes

GNSS → Position

vel_map * deltaTime = deltaPosition

deltaPosition & vel_odem → Orientation

angular_z → deltaOrientation

### Input 1: Position

(timestamp, x, y)

### Input 2: Odom

(timestamp, x, y, theta, x_c, y_c, theta_c)

---

### Ground Truth Data

I noticed all the timestamps were exactly the same. I assumed this was a mistake and they were meant to be the same as both other CSV datasets. For the Ground Truth data I copied over the time stamps from one of the other sets for test calculations.

### Quaternions

I had some initial issues understanding Quaternions as I haven’t worked with them before in this detail. Some work initially went into understanding them and how to get the needed calculations. These calculations were tested on the Ground Truth dataset; the goal was to calculate the car’s orientation (a quaternion) from the change in position on the map frame, and velocity in the odom frame.

The calculated results closely matched the provided orientation values in most cases, but in others ended up being at opposite signs to the provided result i.e. the calculated result approached (0,0,0,1) when the provided results approached (0,0,0,-1). Both quaternion values are actually very similar to each other (which I did not recognise immediately) and I’m happy to keep these calculations moving forward.

### Covariance

I haven’t had much experience in accounting for covariance values in previous projects, so I’m not sure what to do with it in this case unfortunately.


## ROS Framework

Assuming this is going into an existing ROS framework, it would be acting as a new node. It would be listening to (an) existing topic(s) and output its results as a topic. While no information is provided as to what this framework looks like, I made some assumptions based on the input data. I used the same topic names as mentioned in the given rosbag file, and picked suitable message types for the data.

## Input:

### GNSS

/sensors/gnss/odom

geometry_msgs/PointStamped.msg

### ODOM

/sensors/odom

geometry_msgs/TwistWithCovarianceStamped.msg

## Output:

/estimate/pose

geometry_msgs/Pose.msg