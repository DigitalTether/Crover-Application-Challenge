import math 



class LocalTracker():
	# gnss position w/ rolling average
	gnss_positions = []
	position = (0, 0)
	estimated_vel = (0, 0)
	last_timestamp = 0
	rolling_count = 10


	# takes the velocities in both map and odom frames and estimates the car's orientation
	def OrientationFromVelocities(velocity_map, velocity_odom):
		
		theta_map = math.atan2(velocity_map[1], velocity_map[0])
		theta_odom = math.atan2(velocity_odom[1], velocity_odom[0])
		theta = theta_map + theta_odom
		
		return (0, 0, math.sin(theta), math.cos(theta))

	def InputGNSS(self, timestamp, xPos, yPos):

		if len(gnss_positions) >= rolling_count:
			gnss_positions.pop()
		
		l = len(gnss_positions)
		
		gnss_positions.append((xPos, yPos))
		x = 0
		y = 0
		c = 0
		
		while c < l:
			x = x + gnss_positions[c][0]
			y = y + gnss_positions[c][1]
			
		new_position = (x/l, y/l)
		deltaTime = timestamp - last_timestamp
		estimated_vel = ( (new_position[0] - position[0]) / deltaTime, (new_position[1] - position[1]) / deltaTime )
			
		position = new_position
		last_timestamp = timestamp

	def InputODOM(self, timestamp, xVel, yVel, theta, xVel_cov, yVel_cov, theta_cov):
		q = OrientationFromVelocities(estimated_vel, (xVel, yVel))
		return q


# TODO read packaged data from both GNSS and ODOM, and run a simulation using given data
def RunSim(local_tracker, data):
	
	continue


if __name__ == "__main__":
	
	# TODO read data from input files, and call RunSim to test formulas
	
	continue