# Simulator Skeleton File - Project 2
# CS-7639-O01/ECE-8823-OCY Spring 2025
# This file provides the bare - bones requirements for interacting with the Robotarium.
# Note that this code won't actually run.  You'll have to insert your own algorithm!
# If you want to see some working code, check out the 'examples' folder.

import numpy as np
from scipy.io import savemat

import rps.robotarium as robotarium
from rps.utilities.misc import *
from matplotlib.patches import Rectangle

# Get Robotarium object used to communicate with the robots / simulator
N = 3
initial = np.array([[.5, 0, .1],
                    [.1, .3, -.3],
                    [np.pi / 2, np.pi - .2, np.pi - 0.1]])

r = robotarium.Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial)

#################################################
# Select the number of iterations for the experiment.
iterations = 1750  # Do not change

# Other important variables
target = np.array([[.3, .2, .1], [0, 0, 0]])
targetalt = np.array([[.3, .1, .2], [0, 0, 0]])
data = []
final_data = []
# ######################### Place Static Variables Here ##################
# ############### Do not modify anything outside this area ###############
# var = 0;




x_airspace_boundary = np.array([[0.4, 0.7], [-0.3, 0.2]])  # boundary of red zone to avoid
#f_airspace_boundary = np.array([[-0.3, 0.7], [-0.4, 0.4]])
s_airspace_boundary = np.array([[0, 0.45], [-0.1, 0.1]])
taxiway_boundary = np.array([[0, 0.5], [-0.05, 0.05]]) # boundary of taxiway in 


# speed and angular velocity for Class Fast airspace
f_v_min = 0.05
f_v_max = 0.08
f_w_max = np.pi/4 

# speed and angular for Class Slow airspace 
s_v_min = 0.03
s_v_max = 0.04 
s_w_max = np.pi/6 

# speed and angular for taxiway
t_v_min = 0
t_v_max = 0.02
t_w_max = np.pi/2 


min_separation = 0.25 # separation between aircrafts

waypoints = [    # paths for each aircraft, it follows these coordinates
    # A1 - goes around to the left 
    [np.array([0.5, 0.1]), 
     np.array([0.5, 0.2]), 
     np.array([0.4, 0.25]),
     np.array([0.2, 0.25]),
     np.array([0.0, 0.25]),
     np.array([-0.2, 0.25]),
     np.array([-0.3, 0.2]),
     np.array([-0.35, 0.2]),
     np.array([-0.35, 0.15]),
     np.array([-0.3, 0.1]),
     np.array([-0.3, 0.0]),
     np.array([-0.2, 0.0]),
     np.array([-0.1, 0.0]),
     np.array([0.0, 0.0]),
     np.array([0.1, 0.0]),
     np.array([0.2, 0.0]),
     np.array([0.3, 0.0])],   # P3
     
    # A2 - moves down and around and heads to where A3 location was and from there makes its way
    #       to runway+taxiway
    [np.array([0, 0.3]),
     np.array([-0.1, 0.3]),
     np.array([-0.2, 0.25]),
     np.array([-0.35, 0.2]),
     np.array([-0.35, 0.15]),
     np.array([-0.35, 0.1]),
     np.array([-0.35, 0.05]),
     np.array([-0.35, 0.0]),
     np.array([-0.35, -0.05]),
     np.array([-0.35, -0.1]),
     np.array([-0.3, -0.15]),
     np.array([-0.25, -0.15]),
     np.array([-0.2, -0.15]),
     np.array([-0.1, -0.15]),
     np.array([-0.05, -0.15]),
     np.array([0.0, -0.15]),
     np.array([0.1, -0.2]),
     np.array([0.05, -0.25]),
     np.array([0.0, -0.3]),
     np.array([-0.1, -0.3]),
     np.array([-0.25, -0.3]),
     np.array([-0.3, -0.3]),
     np.array([-0.35, -0.3]),
     np.array([-0.4, -0.25]),
     np.array([-0.45, -0.2]),
     np.array([-0.5, -0.15]),
     np.array([-0.3, 0.0]),
     np.array([-0.2, 0.0]),
     np.array([-0.1, 0.0]),
     np.array([0.0, 0.0]),
     np.array([0.1, 0.0]),],  # P1
     
    # A3 - goes up and and circles around to P2, heads to runway+taxiway before A1
    [np.array([0.1, -0.3]),
     np.array([0.0, -0.3]),
     np.array([-0.1, -0.3]),
     np.array([-0.2, -0.3]),
     np.array([-0.3, -0.3]),
     np.array([-0.4, -0.3]),
     np.array([-0.45, -0.3]),
     np.array([-0.45, -0.25]),
     np.array([-0.5, -0.2]),
     np.array([-0.5, -0.15]),
     np.array([-0.5, -0.1]),
     np.array([-0.5, -0.05]),
     np.array([-0.5, 0.0]),
     np.array([-0.55, 0.05]),
     np.array([-0.55, 0.1]),
     np.array([-0.5, 0.15]),
     np.array([-0.5, 0.2]),
     np.array([-0.45, 0.25]),
     np.array([-0.4, 0.3]),
     np.array([-0.35, 0.25]),
     np.array([-0.3, 0.2]),
     np.array([-0.35, 0.1]),
     np.array([-0.3, 0.0]),
     np.array([-0.2, 0.0]),
     np.array([-0.1, 0.0]),
     np.array([0.1, 0.0]),
     np.array([0.2, 0.0]),],    # P2 
]

current_waypoint = [0, 0, 0]  # tracks current index for each aircraft 
waypoint_threshold = 0.07 # threshold distance when a waypoing is reached

a1_landed = False # state to track if A1 landed 
a1_at_parking = False # track if A1 parked

stuck_counter = [0, 0, 0]  # when aircraft moves, checks if it gets to stuck too long at certain waypoints
stuck_threshold = 50 

prev_positions = [None, None, None] # checks previous positions to see if aircraft is stuck









# ############### Do not modify anything outside this area ###############
# ########################################################################


# ######################## Place Helper Functions Here ##################
# ############## Do not modify anything outside this area ###############
# def foo(b)






def calc_dist(pos1, pos2): #calculates euclidean distance between the two 2d positions 
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def is_in_zone(pos, zone_bounds): # if position is within bounds of a specified zone. zone bounds are in 2x2 array with min/max x and y coordinates
    return (zone_bounds[0][0] <= pos[0] <= zone_bounds[0][1] and 
            zone_bounds[1][0] <= pos[1] <= zone_bounds[1][1])
def is_in_slow_zone(pos): # if it's in Slow zone
    return is_in_zone(pos, s_airspace_boundary)
def is_in_x_zone(pos): # if it's in X zone
    return is_in_zone(pos, x_airspace_boundary)
def is_in_taxiway_zone(pos): # if it's in taxiway zone
    return is_in_zone(pos, taxiway_boundary)

def get_speed_constaints(pos): #based on current postioin, returns min/max velocities and max angular; depends on which zone the aircraft is in
    if is_in_taxiway_zone(pos):
        return t_v_min, t_v_max, t_w_max
    elif is_in_slow_zone(pos):
        return s_v_min, s_v_max, s_w_max
    else:
        return f_v_min, f_v_max, f_w_max

def min_separation_dist(positions, i, j):  # checks min separation between 2 aircrafts
    if is_in_taxiway_zone(positions[i]) or is_in_taxiway_zone(positions[j]):
        return True 
    
    dist = calc_dist(positions[i], positions[j])
    return dist >= min_separation

def normalize_angle_orientation(angle): # -pi, pi ; have consistent angle calculations for orientation
    while angle > np.pi:
        angle -= 2*np.pi 
    while angle < -np.pi:
        angle += 2*np.pi
    return angle 

def angle_to_target_point(current_pos, current_angle, target_pos): # angle difference between current heading and direction to target position, this is used for steering toward waypoints
    dx = target_pos[0] - current_pos[0]
    dy = target_pos[1] - current_pos[1]
    target_angle = np.arctan2(dy, dx)

    angle_diff = normalize_angle_orientation(target_angle - current_angle)
    return angle_diff


#calculates inputs of velocity and angular to move aircraft toward target position
def input_controller(pos, angle, target_pos, v_min, v_max, w_max, smooth=1.0): 
    dist = calc_dist(pos, target_pos)
    angle_diff = angle_to_target_point(pos, angle, target_pos)
    
#impelments proprotional control  for angular and adjusts linear based on turn angle and distance to target
    w_gain = 3.5
    w = np.clip(w_gain * angle_diff, -w_max, w_max)
# slow speed for sharp turns that are greatser than 45 deg
    if abs(angle_diff) > np.pi/4:
        v = v_min
        return v, w 
    # else it adjust speed based on turn angle and distance 
    turn_factor = max(0.5, 1.0 - abs(angle_diff)/np.pi)
    dist_factor = min(1.0, dist / 0.15)

    v_desired = smooth * v_max * min(turn_factor, dist_factor)
    v = np.clip(v_desired, v_min, v_max)

    return v, w 

def is_waypoint_reached(pos, waypoint): # if aircraft reached a waypoint within threshold 
    return calc_dist(pos, waypoint) < waypoint_threshold

def is_stuck(pos, prev_pos):  # if aircraft is stuck - checks current position to previous positions
    if prev_pos is None:
        return False
    return calc_dist(pos, prev_pos) < 0.005






# ############## Do not modify anything outside this area ###############
# #######################################################################

# Iterate for the previously specified number of iterations
for t in range(iterations):
    # Retrieve the most recent poses from the Robotarium.  The time delay is
    # approximately 0.033 seconds
    p = r.get_poses()

    # Plot path traces every 20 iterations
    if np.mod(t, 20) == 0:
        plt.plot(p[0][0], p[1][0], 'k.',  # Black dot
                 p[0][1], p[1][1], 'm.',  # Magenta dot
                 p[0][2], p[1][2], 'b.')  # Blue dot

    # Success check with position tolerance embedded
    p_rounded = np.round(p[:2, :], decimals=2)
    if np.array_equal(p_rounded, target) or np.array_equal(p_rounded, targetalt):
        print(f'Success! The final iteration number is {t}.\n')
        break

    # ######################## Place Algorithm Here #########################
    # ############## Do not modify anything outside this area ###############





    
    positions = p[:2, :].T   # current positions of all the aircrafts
    angles = p[2, :]  # current angles of all the aircraft

    # if any of the 3 aircraft is stuck, checks with their previous positions
    for i in range(N):
        if prev_positions[i] is not None:
            if is_stuck(positions[i], prev_positions[i]):
                stuck_counter[i] += 1  # increments if it hasn't moved much
            else:
                stuck_counter[i] = 0 # resets the counter if aircraft is moving
        prev_positions[i] = positions[i].copy()
    
    # if any of the 3 aircraft reached its current waypoint
    for i in range(N):
        if current_waypoint[i] < len(waypoints[i]) and is_waypoint_reached(positions[i], waypoints[i][current_waypoint[i]]):
            current_waypoint[i] += 1 # increments to next waypoint if current waypoint is reached
    
    #if A1 completed its path to P3
    if current_waypoint[0] >= len(waypoints[0]):
        a1_landed = True
        a1_at_parking = True
    #if A2 completed its path to its parking spot P1                                           # Initially I went with strategy to check A1 path and then A2 path, but couldn't get A3 to hold out so I tweaked waypoints so that its A3 to P2 and A2 to P1 last
    a2_at_parking = current_waypoint[1] >= len(waypoints[1])

    # intilizes control inputs inputs for all aircraft
    v_inputs = np.zeros(N)
    w_inputs = np.zeros(N)

    # clacualtes control inputs for each aircraft
    for i in range(N):
        if current_waypoint[i] < len(waypoints[i]):
            target = waypoints[i][current_waypoint[i]]   # current target waypoint 
            v_min, v_max, w_max = get_speed_constaints(positions[i]) # get the velocity constraints based on current pos

            if i == 1: # A1 is prioritized so if A1 hasn't rached a certain point, A2 is held down
                if current_waypoint[i] == 3 and current_waypoint[0] < 10:
                    hold_radius = 0.05
                    hold_angle = t * 0.05
                    hold_x = target[0] + hold_radius * np.cos(hold_angle)
                    hold_y = target[1] + hold_radius * np.sin(hold_angle)
                    target = np.array([hold_x, hold_y])

            elif i == 2:  # A3 is held based on A1 and A2 flight path progress
                if current_waypoint[i] <= 4 and not a1_at_parking:
                    hold_radius = 0.05  # hold A3 in circular pattern until A1 to P3 is done
                    hold_angle = t * 0.05
                    hold_x = target[0] + hold_radius * np.cos(hold_angle)
                    hold_y = target[1] + hold_radius * np.sin(hold_angle)
                    target = np.array([hold_x, hold_y])

                elif current_waypoint[i] <= 12 and not a2_at_parking:  # A3 is held into another circular pattern until A2    # that's not the case in the simulation...
                    hold_radius = 0.05
                    hold_angle = t * 0.05
                    hold_x = target[0] + hold_radius * np.cos(hold_angle)
                    hold_y = target[1] + hold_radius * np.sin(hold_angle)
                    target = np.array([hold_x, hold_y])

            velocity_smoother_control = 1.0 # smooth aircraft velocity control 
            if stuck_counter[i] > stuck_threshold: # if aircraft is stuck for too long, increase velocity smooth control
                velocity_smoother_control = 1.5
                if stuck_counter[i] > stuck_threshold * 2:
                    current_waypoint[i] = min(current_waypoint[i] + 1, len(waypoints[i]) - 1)
                    stuck_counter[i] = 0
                    print(f"aircraft: {i} stuck; skipping to waypoint: {current_waypoint[i]}")

            # calcualte velocity and angular for current aircraft 
            v_inputs[i], w_inputs[i] = input_controller(positions[i], angles[i], target, v_min, v_max, w_max, velocity_smoother_control)

            if is_in_x_zone(positions[i]):  # if aircraft enters x airspace, change path to a safer point
                if i == 0:
                    emergency_target = np.array([0.0, 0.25])
                elif i == 1: 
                    emergency_target = np.array([-0.2, 0.3])
                else:
                    emergency_target = np.array([-0.5, -0.3])

                v_inputs[i], w_inputs[i] = input_controller(positions[i], angles[i], emergency_target, v_min, v_max, w_max)
        else:  # if aircraft reached all waypoints, put a stop
            v_inputs[i] = 0
            w_inputs[i] = 0
    
    for i in range(N):  # checks min separation
        for j in range(i+1, N):
            if not min_separation_dist(positions, i, j):
                v_inputs[1] *= 0.7 # reduce speeds of both aircraft it too close
                v_inputs[j] *= 0.7

                if i == 0:  # A1's movement is prioritzed; slows others more 
                    v_inputs[j] *= 0.5
                elif j == 0:
                    v_inputs[i] *= 0.5
                elif i == 1:    # then A2's movement          but simulation shows differet... 
                    v_inputs[j] *= 0.5
                elif j == 1:
                    v_inputs[i] *= 0.5

    for i in range(N):  # constaints to all control inputs 
        v_min, v_max, w_max = get_speed_constaints(positions[i])
        v_inputs[i] = np.clip(v_inputs[i], v_min, v_max)
        w_inputs[i] = np.clip(w_inputs[i], -w_max, w_max)
    
    u = np.array([v_inputs, w_inputs])   # merges linear and angular into control input matrix 

  







    #u = np.array([[.1, .2, .3], [.1, .2, .3]])
    # In u the first array covers velocity and the second array
    # covers angular velocity the affinity is as follows
    # np.array([[1, 2, 3], [1, 2, 3]])
    # Observe what happens to get a sense of how it works.

    # You should think about implementing a finite-state machine. How many
    # states are there? What are the transitions? What signals the transition
    # from one state to another?

    # ############## Do not modify anything outside this area ###############
    # #######################################################################

    # Send velocities to agents

    # Set velocities of agents 1,...,N
    r.set_velocities(np.arange(N), u)  # u is the input, a 2x1 vector for 1 robot

    data.append(np.vstack((p, u)))
    # Send the previously set velocities to the agents.  This function must be called!
    r.step()

final_data = np.hstack(data)
final_data_reshaped = final_data.reshape(15, len(data), order='F')
savemat('data.mat', {'data': final_data_reshaped})
plt.savefig('plot.png', dpi=300, bbox_inches='tight')

