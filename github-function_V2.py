def reward_function(params):
     
    center_variance = params["distance_from_center"] / params["track_width"]
     
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    closest_waypoints = params["closest_waypoints"]
    waypoints = params['waypoints']
    heading = params['heading']
    speed = params['speed']
    abs_steering = abs(params['steering_angle'])
    MAX_SPEED = 3
 
    marker_1 = 0.12 * track_width
    marker_2 = 0.24 * track_width
    marker_3 = 0.36 * track_width
    marker_4 = 0.48 * track_width
     
    left_lane = [25,26,27,28,29,30,31,57,58,59,60,61,62,63,72,73,74,75,76,77,78,79,80,81,82,83,84,
                 101,102,103,104,105,106,127,128,129,130,131,159,160,161,162,163,164]
    right_lane = [38,39,40,41,42,43,44,45,46,85,86,87,88,89,90,91,91,93,94,95]
    center_lane = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
                    32,33,34,35,36,37,46,47,48,49,50,51,52,53,54,55,56,64,65,66,67,68,69,70,71,
                    96,97,98,99,100,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,
                    132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158]
    straight_lane = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,113,114,115,116,117,118,119,120,121,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155]
    left_end_lane = [31,32,33,63,64,65,110,111,112,133,134,135,136,137,138]
    right_end_lane = [45,46,47,48]
     
#     after_closest_waypoints = params["closest_waypoints"][1]
     
    # Calculate 3 markers that are at varying distances away from the center line
    reward = 2.1
     
    if all_wheels_on_track:
        reward += 1
    else:
        reward -= 1
     
    # Give higher reward if the car is closer to center line and vice versa
     
    if closest_waypoints[1] in left_lane and params['is_left_of_center']:
        reward += 1
    elif closest_waypoints[1] in right_lane and not params['is_left_of_center']:
        reward += 1
    elif closest_waypoints[1] in center_lane and center_variance <0.4:
        reward += 1
    else:
        reward -= 1
     
#     speed_rate = speed / MAX_SPEED
#     reward_speed = speed_rate **2
     
    if closest_waypoints[1] in straight_lane and abs_steering < 5:
        speed = MAX_SPEED
         
    ##### distance_from_center check############
     
    reward_distance=1
     
    if distance_from_center <= marker_1:
        reward_distance = 1.0
    elif distance_from_center <= marker_2:
        reward_distance = 0.7
    elif distance_from_center <= marker_3:
        reward_distance = 0.4
    elif distance_from_center <= marker_4:
        reward_distance = 0.1
    else:
        reward_distance = 1e-3  # likely crashed/ close to off track
     
     
    reward_all  = reward + reward_distance
     
    ABS_STEERING_THRESHOLD = 15
     
    # Penalize reward if the car is steering too much
    if closest_waypoints[1] in straight_lane and abs_steering > 5:
        reward_all *=0.8
    elif closest_waypoints[1] in left_end_lane and abs_steering >10 and params['is_left_of_center']:
        reward_all *= 0.8
    elif closest_waypoints[1] in right_end_lane and abs_steering >10 and not params['is_left_of_center']:
        reward_all *= 0.8
    elif closest_waypoints[1] in center_lane and abs_steering > ABS_STEERING_THRESHOLD:
        reward_all *= 0.8
    else:
        reward_all = reward_all
 
    return float(reward_all)