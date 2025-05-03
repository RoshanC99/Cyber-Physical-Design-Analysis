# Simulator Skeleton File - Project 1
# CS-7639-O01/ECE-8823-OCY Spring 2025 
# This file provides the bare - bones requirements for interacting with the Robotarium.
# Note that this code won't actually run.  You'll have to insert your own algorithm!
# If you want to see some working code, check out the 'examples' folder.

import numpy as np
from scipy.io import savemat

import rps.robotarium as robotarium
from rps.utilities.barrier_certificates import create_unicycle_barrier_certificate_with_boundary

# Get Robotarium object used to communicate with the robots / simulator
N = 1
r = robotarium.Robotarium(number_of_robots=N, show_figure=True)
data = []

# Select the number of iterations for the experiment.
iterations = 3000 # Do not change

# Create a boundary barrier
uni_barrier_certificate = create_unicycle_barrier_certificate_with_boundary()

# Other important variables
target1 = np.array([[.5],[0],[np.pi]])
target2 = np.array([[-0.5],[0],[np.pi]])

k = 1 # angular gain for feedback/closed_loop control 

# ######################### Place Static Variables Here ##################
# ############### Do not modify anything outside this area ###############
# var = 0;
velocity = 0.08 # m/s <- 8 cm/s
time_step = 0.033 # 30 hz control freq

target2_init_iteration = None    #for target2 open-loop 
target2_required_iterations = None   #for target2 open-loop    
# ############### Do not modify anything outside this area ###############
# ########################################################################


# ######################## Place Helper Functions Here ##################
# ############## Do not modify anything outside this area ###############
# def foo(b)
def num_of_iterations_target2(distance, speed):            #find total number of iterations needed to reach a given distance
    return int(np.ceil(distance / (speed * time_step)))

def feedback_control(p, target_pose):
    x_diff = target_pose[0,0] - p[0,0]
    y_diff = target_pose[1,0] - p[1,0]
    theta_desired = np.arctan2(y_diff, x_diff)
    theta_current = p[2,0]
    angle_error = theta_desired - theta_current

    angle_error2 = (angle_error + np.pi) % (2*np.pi) - np.pi    # angle error [-pi, pi]

    omega = k * angle_error2
    v = velocity if abs(angle_error2) < 0.1 else 0     #conditional expression - only move forward if robot is oriented correctly

    return np.array([[v], [omega]])

# check if its within tolerance of target pose
def is_within_tolerance(p, target_pose, position_tolerance=0.01, angle_tolerance=0.1):  
    position_error = np.linalg.norm(p[:2,0] - target_pose[:2,0])
    angle_error = abs((p[2,0] - target_pose[2,0] + np.pi) % (2*np.pi) - np.pi)
    return position_error < position_tolerance and angle_error < angle_tolerance
# ############## Do not modify anything outside this area ###############
# #######################################################################

# Iterate for the previously specified number of iterations
state = 1 #start at state 1 to go to target1

for t in range(iterations):
    # Retrieve the most recent poses from the Robotarium.  The time delay is
    # approximately 0.033 seconds
    p = r.get_poses()

    # ######################## Place Algorithm Here #########################
    # ############## Do not modify anything outside this area ###############
    # u = ???;
    # You  can try with u = np.array([[0.1], [0]]) and np.array([[0], [1]]) first.
    # Observe what happens to get a sense of how it works.

    # You should think about implementing a finite-state machine. How many
    # states are there? What are the transitions? What signals the transition
    # from one state to another?

    if state == 1:
        print(f"state {state}: moving to target1 with feedback/closed-loop control")
        u = feedback_control(p, target1)
        if is_within_tolerance(p, target1):
            print("\n")
            print("reached target1" "\n"
                  "switching to state 2 \n")
            state = 2
          
          
            target2_init_iteration = t
            distance_to_target2 = np.linalg.norm(target2[:2,0] - target1[:2,0])
            target2_required_iterations = num_of_iterations_target2(distance_to_target2, velocity)

    elif state == 2:
        print(f"state {state}: moving to target2 with OPEN-LOOP control")
        if target2_init_iteration is not None and t - target2_init_iteration < target2_required_iterations:
            u = np.array([[velocity], [0]])
        else:
            print("\n")
            print("reached target2" "\n" 
                  "switching to state 3 \n")
            u = np.array([[0.1], [0]])
            state = 3
    
    elif state == 3:
        print(f"state {state}: returning back to target1 with feedback/closed-loop control")
        u = feedback_control(p, target1)
        if is_within_tolerance(p, target1):
            print("\n")
            print("reached target1" "\n"
                  "switching to state 4 \n")
            state = 4

    elif state == 4:
        print(f"state {state}: moving to target2 with Feedback/Closed-Loop control")
        u = feedback_control(p, target2)
        if is_within_tolerance(p, target2):
            print("\n")
            print("reached target2" "\n"
                  "switching to state 5 \n")
            state = 5

    elif state == 5: 
        print(f"state {state}: returning back to target1 with feedback/closed-loop control")
        u = feedback_control(p, target1)
        if is_within_tolerance(p, target1):
            print("\n")
            print("reached target1" "\n"
                  "done")
            break

    # ############## Do not modify anything outside this area ###############
    # #######################################################################

    # Send velocities to agents

    # Apply the barrier to the velocities
    u = uni_barrier_certificate(u, p)

    # Set velocities of agents 1,...,N
    r.set_velocities(np.arange(N), u) # u is the input, a 2x1 vector for 1 robot

    data.append(np.vstack((p, u)))
    # Send the previously set velocities to the agents.  This function must be called!
    r.step()

savemat('data.mat', {'data':np.hstack(tuple(data))})
# Call at end of script to print debug information and for your script to run on the Robotarium server properly
r.call_at_scripts_end()
