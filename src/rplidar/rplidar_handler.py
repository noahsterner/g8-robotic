# TODO: FIX VOXEL SIZE ACCUMULATOR LIMIT(DON'T WASTE MEMORY)

import sys
import math
import numpy as np
import pygame # install pygame-ce if python > 3.10
import traceback
import time
import open3d as o3d
import argparse

from simplification.cutil import simplify_coords
from robot_hat import RPLidarC1, RPLidarC1Config

### --- Configuration --- ###

PORT_NAME = 'COM7'  # RPLidar connection port
BAUD_RATE = 460800  # RPLidar baud rate

### Screen settings

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
MAP_SCALE = 150 #0.15 # Pixels per meter(Adjust to zoom out)

### Current position of robot

robot_pos = {
    'x': 0.0,       # X position in terms of mm on map
    'y': 0.0,       # Y position in terms of mm on map
    'heading': 0.0  # Direction of robot in terms of radians(0 = straight forward)
}

### Current position of map

map_pos = {
    'x': 0.0,       # X position in terms of mm on map
    'y': 0.0,       # Y position in terms of mm on map
    'rotation': 0.0 # Rotation of map in terms of radians(0 = straight forward)
}

### Global positioning/accumulation of robot/sensor

global_pos = np.eye(4)
global_map_pcd = None

### Map drawing and ICP settings

VOXEL_SIZE = 0.02  # Gitter-size(In meters) - Put together points closer than this distance.
ICP_THRESHOLD = 0.3  # Max distance(In meters) to match specific point with accumulated map

### Voxel-accumulator for average grid

voxel_grid_accumulator = {}

### Array for closest points in any direction
### Array order: Front, back, left, right
### Returns -1 on uninitialized points
closest_map_points = {
  "front": -1.0,
  "back": -1.0,
  "left": -1.0,
  "right": -1.0
}

### --- FUNCTIONS/METHODS --- ###

### --- Parse command arguments when initializing program --- ###

def parse_args():
    default_port = PORT_NAME
    p = argparse.ArgumentParser(description="RPLidar Handler")
    p.add_argument("--port", default=default_port,
                    help=f"Serial port for the RPLidar (default: {default_port})")
    p.add_argument("--baudrate", type=int, default=460800,
                    help="Serial baud rate (default: 460800 for C1)")
    return p.parse_args()

### --- Return closest point by any direction --- ###

def get_closest_map_point(direction):
    
    global closest_map_points
    
    if direction not in closest_map_points:
        raise RuntimeError("Returned direction is invalid, returning front")
        return closest_map_points["front"]
    
    return closest_map_points[direction]
    #else
    #    raise RuntimeError("Returned direction is invalid, returning front")

### --- Handle collision event --- ###

def collision_event_broadcast(directions = ["none"], data=[-1]):
    
    #print("FOUND COLLISION IN THE FOLLOWING DIRECTIONS: ", directions)
    
    if data[0] != -1:
        print("VALID COLLISION HERE!")
        ### TODO: CALL CAMERA AND SCRIPT FOR SENDING CAMERA IMAGES AND CURRENT DATA TO BACKEND

### --- Init the program --- ###

def init_pygame():
    
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPLidar C1 - Fast Vector Map")
    clock = pygame.time.Clock()
    
    return screen, clock

### --- Convert polar position to proper point position --- ###

def polar_to_global_vector(angle_deg, distance_m, pose):
    
    if distance_m <= 0:
        return None  # Filter away unlikely/too closely distances points

    lidar_rad = math.radians(angle_deg)

    local_x = distance_m * math.cos(lidar_rad)
    local_y = distance_m * math.sin(lidar_rad)

    global_x = pose['x'] + (local_x * math.cos(pose['heading']) - local_y * math.sin(pose['heading']))
    global_y = pose['y'] + (local_x * math.sin(pose['heading']) + local_y * math.cos(pose['heading']))

    return [global_x, global_y]

### --- Rotate point around another point in radians --- ###

def rotate(origin, point, angle):

    o_x, o_y = origin
    p_x, p_y = point

    q_x = o_x + math.cos(angle) * (p_x - o_x) - math.sin(angle) * (p_y - o_y)
    q_y = o_y + math.sin(angle) * (p_x - o_x) + math.cos(angle) * (p_y - o_y)
    
    return q_x, q_y

### --- Generate finalized point cloud based of averaged value in every voxel --- ###

def generate_average_map():

    avg_points = []
    
    for voxel_data in voxel_grid_accumulator.values():
        mean_point = voxel_data["sum_coords"] / voxel_data["count"]
        avg_points.append(mean_point)
        
    pcd = o3d.geometry.PointCloud()
    if avg_points:
        pcd.points = o3d.utility.Vector3dVector(np.array(avg_points))
    return pcd

### --- Main program function --- ###

def main(args):
    
    global MAP_SCALE, PORT_NAME, BAUD_RATE
    global global_pos, global_map_pcd
    global voxel_grid_accumulator
    global closest_map_points
    
    screen, clock = init_pygame()
    print(f"Connecting to RPLidar C1 at port {PORT_NAME}...")
    
    PORT_NAME = args.port
    BAUD_RATE = args.baudrate
    
    lidar = RPLidarC1(RPLidarC1Config(port=PORT_NAME))
    
    with lidar:
        
        info = lidar.get_device_info()
        print("RPLidar Info: ", info)

        health = lidar.get_health()
        print("RPLidar Health Status: ", health)
        
        if not health.is_usable:
            raise RuntimeError(f"Lidar health error: {health.error_code}")
        
        lidar.start_scan()
        
        time.sleep(2.0) # Wait for RPLidar to start up properly
    
        print("RPLidar connected. Starting Pygame-window...")
    
        font = pygame.font.SysFont(None, 25)
        
        ### Current maximum RPLidar dot measurement thresholds ###

        rplidar_quality = 10
        rplidar_min_dist = 0
        rplidar_min_line_dist = 0.15
        rplidar_collision_dist = 0.05
        rplidar_simplify_epsilon = 0.001
        
        ### Run the program ###
    
        running = True
        while running:
            try:
                
                ### Handle PyGame keyboard input
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise KeyboardInterrupt
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        raise KeyboardInterrupt
                
                pressed_keys = pygame.key.get_pressed()
                if (pressed_keys):
                    if pressed_keys[pygame.K_e]: #Zoom in
                        MAP_SCALE = MAP_SCALE + 25
                    if pressed_keys[pygame.K_q]: #Zoom out
                        MAP_SCALE = MAP_SCALE - 25
                    if pressed_keys[pygame.K_w]: #Move map up
                        map_pos['y'] = map_pos['y'] + 25
                    if pressed_keys[pygame.K_s]: #Move map down
                        map_pos['y'] = map_pos['y'] - 25
                    if pressed_keys[pygame.K_a]: #Move map left
                        map_pos['x'] = map_pos['x'] + 25
                    if pressed_keys[pygame.K_d]: #Move map right
                        map_pos['x'] = map_pos['x'] - 25
                    if pressed_keys[pygame.K_z]: #Rotate map left
                        map_pos['rotation'] = map_pos['rotation'] - 0.1
                    if pressed_keys[pygame.K_x]: #Rotate map right
                        map_pos['rotation'] = map_pos['rotation'] + 0.1
                    if pressed_keys[pygame.K_c]: #Center map
                        map_pos['x'] = 0
                        map_pos['y'] = 0
                        map_pos['rotation'] = 0
                    if pressed_keys[pygame.K_r]: #Raise RPL quality
                        rplidar_quality = rplidar_quality + 1
                    if pressed_keys[pygame.K_f]: #Lower RPL quality
                        rplidar_quality = rplidar_quality - 1
                    if pressed_keys[pygame.K_t]: #Raise minimum RPL dot distance
                        rplidar_min_dist = rplidar_min_dist + 0.01
                    if pressed_keys[pygame.K_g]: #Lower minimum RPL dot distance
                        rplidar_min_dist = rplidar_min_dist - 0.01
                    if pressed_keys[pygame.K_y]: #Raise minimum RPL vector line distance
                        rplidar_min_line_dist = rplidar_min_line_dist + 0.01
                    if pressed_keys[pygame.K_h]: #Lower minimum RPL vector line distance
                        rplidar_min_line_dist = rplidar_min_line_dist - 0.01
                    if pressed_keys[pygame.K_u]: #Raise minimum collision detection distance
                        rplidar_collision_dist = rplidar_collision_dist + 0.01
                    if pressed_keys[pygame.K_j]: #Lower minimum collision detection distance
                        rplidar_collision_dist = rplidar_collision_dist - 0.01
                    if pressed_keys[pygame.K_i]: #Raise RPL dot simplification epsilon value
                        rplidar_simplify_epsilon = rplidar_simplify_epsilon + 0.001
                    if pressed_keys[pygame.K_k]: #Lower RPL dot simplification epsilon value
                        rplidar_simplify_epsilon = rplidar_simplify_epsilon - 0.001
                
                ### Clear the screen with a dark background

                screen.fill((20, 24, 30))
                
                ### Find central position of sensor/robot on local map
                
                center_x = SCREEN_WIDTH // 2
                center_y = SCREEN_HEIGHT // 2
                
                heading_x = center_x + int(30 * math.cos(robot_pos['heading']))
                heading_y = center_y + int(30 * math.sin(robot_pos['heading']))
                
                robot_center = (center_x + map_pos['x'], center_y + map_pos['y'])
                robot_heading = (heading_x + map_pos['x'], heading_y + map_pos['y'])
                
                robot_heading = rotate(robot_center,
                                    robot_heading,
                                    map_pos['rotation'])
                
                ### Draw the sensor position in the middle of the screen
                pygame.draw.circle(screen, (255, 50, 50), robot_center, 6)
                
                ### Draw heading of sensor/robot
                pygame.draw.line(screen, (0, 255, 0), robot_center, robot_heading, 2)
                
                ### Draw text of current RPLidar measurement qualities
                text = font.render(f'Current RPLidar quality: {rplidar_quality}', True, (255, 255, 255))
                screen.blit(text, (0, 0))
                text = font.render(f'Current RPLidar minimum distance: {rplidar_min_dist}', True, (255, 255, 255))
                screen.blit(text, (0, 25))
                text = font.render(f'Current RPLidar minimum line distance: {rplidar_min_line_dist}', True, (255, 255, 255))
                screen.blit(text, (0, 50))
                text = font.render(f'Current RPLidar minimum collision distance: {rplidar_collision_dist}', True, (255, 255, 255))
                screen.blit(text, (0, 75))
                text = font.render(f'Current RPLidar dot simplification epsilon: {rplidar_simplify_epsilon}', True, (255, 255, 255))
                screen.blit(text, (0, 100))
                
                ### --- Process sensor data --- ###
                
                ### Scan points ###

                current_vectors = [] #XY-coordinates
                #current_vectors_info = [] #angles and distances

                current_pcd = o3d.geometry.PointCloud()

                for scan in lidar.iter_scans(min_measurements=100, max_scans=1): 
                    #print(scan)
                    
                    points_3d = []
                    
                    for measurement in scan.measurements:
                        #print(measurement)
                        if measurement.quality > rplidar_quality and measurement.distance_m > rplidar_min_dist:
                            
                            """
                            vector = polar_to_global_vector(measurement.angle_deg,
                                                            measurement.distance_m,
                                                            robot_pos)
                            if vector:
                                current_vectors.append(vector)
                                current_vectors_info.append([measurement.angle_deg, measurement.distance_m])
                            """
                            
                            angle_rad = np.radians(measurement.angle_deg)
                            x = measurement.distance_m * np.cos(angle_rad)
                            y = measurement.distance_m * np.sin(angle_rad)
                            vector = [x, y, 0.0]
                            
                            if vector:
                                points_3d.append(vector)
                                #current_vectors_info.append([measurement.angle_deg, measurement.distance_m])
                                
                    if points_3d:
                        current_pcd.points = o3d.utility.Vector3dVector(np.array(points_3d))            
                
                current_pcd = current_pcd.voxel_down_sample(voxel_size=VOXEL_SIZE)
                
                # Make sure current scan has enough points before continuation
                if len(current_pcd.points) < 15:
                    continue
                
                # Make sure global map is properly initialized
                # with first proper scan before continuation
                #if len(global_map_pcd.points) == 0:
                if global_map_pcd is None:
                    global_map_pcd = current_pcd
                    
                    # Accumulate average points for current map
                    points = np.asarray(current_pcd.points)
                    
                    for pt in points:
                        # Find voxel index based on voxel size
                        grid_coord = tuple(np.floor(pt / VOXEL_SIZE).astype(int))
                        
                        # Update sum and counts for current voxel
                        if grid_coord not in voxel_grid_accumulator:
                            voxel_grid_accumulator[grid_coord] = {"sum_coords": np.array(pt), "count": 1}
                        else:
                            voxel_grid_accumulator[grid_coord]["sum_coords"] += pt
                            voxel_grid_accumulator[grid_coord]["count"] += 1
                    
                    print("GLOBAL MAP INITIATED!")
                    continue
                
                ### Perform ICP on currently accumulated global map
                ### Use previously known global positioning as initial guess
                icp_result = o3d.pipelines.registration.registration_icp(
                    current_pcd, global_map_pcd, ICP_THRESHOLD, np.eye(4),
                    o3d.pipelines.registration.TransformationEstimationPointToPoint(),
                    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=30)
                )
                
                # Update robot/sensor positioning based on current ICP matching
                global_pos = global_pos @ icp_result.transformation
                
                # Make deep copy of new map
                transformed_pcd = current_pcd.select_by_index(list(range(len(current_pcd.points))))
                transformed_pcd.transform(global_pos)
                
                # Generate map based on average value in each voxel
                points = np.asarray(transformed_pcd.points)
                
                for pt in points:
                    grid_coord = tuple(np.floor(pt / VOXEL_SIZE).astype(int))
                    
                    if grid_coord not in voxel_grid_accumulator:
                        voxel_grid_accumulator[grid_coord] = {"sum_coords": np.array(pt), "count": 1}
                    else:
                        voxel_grid_accumulator[grid_coord]["sum_coords"] += pt
                        voxel_grid_accumulator[grid_coord]["count"] += 1
                
                # Voxel-downsample current map to prevent memory leaks and remove duplications
                #global_map_pcd = global_map_pcd.voxel_down_sample(voxel_size=VOXEL_SIZE)
                
                # Save to global map
                global_map_pcd = current_pcd
                
                # Print test values for current map
                global_pos_x = global_pos[0, 3]
                global_pos_y = global_pos[1, 3]
                global_yaw_deg = np.degrees(np.arctan2(global_pos[1, 0], global_pos[0, 0]))
                
                #print("GLOBAL MAP, NUMBER OF POINTS: ", len(global_map_pcd.points))
                #print(f"GLOBAL MAP, POSITION: X={global_pos_x:.2f} m, Y={global_pos_y:.2f} m")
                #print(f"GLOBAL MAP, DIRECTION: {global_yaw_deg:.1f}°")
                #print(f"Accumulated voxels in memory: {len(voxel_grid_accumulator)}")
                
                current_vectors = np.asarray(current_pcd.points)[:, [0, 1]].tolist()
                #print(current_vectors)
                
                ### Simplify collected vector points ###
                
                current_vectors_info_remove = []
                simplified_vectors = simplify_coords(current_vectors, epsilon=rplidar_simplify_epsilon)        
                current_vectors = simplified_vectors
                
                ### Draw all available vectors and lines on the screen ###
                ### Also draw out vector color based on angle difference
                ### and handle collision if any point is too close
                
                curr_closest_map_points = {
                  "front": -1.0,
                  "back": -1.0,
                  "left": -1.0,
                  "right": -1.0
                }

                for i in range(0, len(current_vectors)):
                    
                    screen_x = robot_center[0] + int(current_vectors[i][0] * MAP_SCALE)
                    screen_y = robot_center[1] - int(current_vectors[i][1] * MAP_SCALE)
                    
                    screen_x, screen_y = rotate(robot_center,
                                                [screen_x, screen_y],
                                                map_pos['rotation'])
                    
                    detected_direction = "none"
                    drawn_color = (255, 255, 255) # Default color - White
                    
                    curr_vec_angle_rads = np.arctan2(current_vectors[i][1],
                                                     current_vectors[i][0])
                    curr_vec_angle_degs = np.degrees(curr_vec_angle_rads)
                    
                    if curr_vec_angle_degs < 0:
                        curr_vec_angle_degs = curr_vec_angle_degs + 360
                    
                    #print(curr_vec_angle_degs)
                    
                    if curr_vec_angle_degs > 315 or curr_vec_angle_degs <= 45:
                        drawn_color = (255, 0, 0) # In front of RPLidar - Red
                        detected_direction = "front"
                    elif curr_vec_angle_degs > 45 and curr_vec_angle_degs <= 135:
                        drawn_color = (0, 255, 0) # To the left of RPLidar - Green
                        detected_direction = "left"
                    elif curr_vec_angle_degs and curr_vec_angle_degs <= 225:
                        drawn_color = (0, 0, 255) # Behind the RPLidar - Blue
                        detected_direction = "back"
                    elif curr_vec_angle_degs > 225 and curr_vec_angle_degs <= 315:
                        drawn_color = (255, 255, 0) # To the right of RPLidar - Yellow
                        detected_direction = "right"
                    
                    curr_vec_dist = math.dist([0, 0], current_vectors[i])
                    
                    if curr_closest_map_points[detected_direction] <= float(-1.0)\
                    or curr_closest_map_points[detected_direction] > curr_vec_dist:
                        curr_closest_map_points[detected_direction] = curr_vec_dist
                    
                    if curr_vec_dist <= rplidar_collision_dist:
                        #print("COLLISION DETECTED AT DISTANCE ", current_vectors_info[i][1])
                        drawn_color = (255, 255, 255)
                        #collision_event_broadcast([detected_direction]) #Too close to a nearby point; Detect collision!
                    
                    if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
                        pygame.draw.circle(screen, drawn_color, (screen_x, screen_y), 2)
                        
                closest_map_points = curr_closest_map_points
                #print(curr_closest_map_points["front"])
                #print("CLOSEST DIRECTIONAL MAP POINTS:", closest_map_points)

                ### Draw lines between all available vectors ###
                        
                if len(current_vectors) > 1:
                    
                    current_segment = [current_vectors[0]]
                    
                    for i in range(1, len(current_vectors)):
                        
                        #print(i)
                        p1 = current_vectors[i - 1]
                        p2 = current_vectors[i]
                        
                        dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
                        #print(dist)
                        
                        if dist < rplidar_min_line_dist:
                            current_segment.append(p2)
                        else:
                            if len(current_segment) > 1:
                                
                                segment = current_segment
                                #segment = simplify_coords_2d(segment, epsilon=0.01) #Simplify vector map
                                for e in range(0, len(segment)):
                                    segment[e] = [robot_center[0] + int(segment[e][0] * MAP_SCALE),
                                                  robot_center[1] - int(segment[e][1] * MAP_SCALE)]
                                    segment[e] = rotate(robot_center, segment[e], map_pos['rotation'])
                                pygame.draw.lines(screen, (127,127,127), False, segment, 2)
                                
                            current_segment = [p2]
                    
                    # --> Draw last segment and close circle if allowed --> #
                    
                    last_segment = current_segment
                    if len(last_segment) > 1:
                        
                        for e in range(0, len(last_segment)):
                            last_segment[e] = [robot_center[0] + int(last_segment[e][0] * MAP_SCALE),
                                               robot_center[1] - int(last_segment[e][1] * MAP_SCALE)]
                            last_segment[e] = rotate(robot_center, last_segment[e], map_pos['rotation'])
                        pygame.draw.lines(screen, (127,127,127), False, last_segment, 2)
                        
                        ### Try to bind first and last point for a completely closured conture
                        end_start_dist = math.hypot(current_vectors[-1][0] - current_vectors[0][0], current_vectors[-1][1] - current_vectors[0][1])
                        if end_start_dist < rplidar_min_line_dist:
                            draw_segment_1 = [robot_center[0] + int(current_vectors[-1][0] * MAP_SCALE),
                                robot_center[1] - int(current_vectors[-1][1] * MAP_SCALE)]
                            draw_segment_2 = [robot_center[0] + int(current_vectors[0][0] * MAP_SCALE),
                                robot_center[1] - int(current_vectors[0][1] * MAP_SCALE)]
                            draw_segment_1 = rotate(robot_center, draw_segment_1, map_pos['rotation'])
                            draw_segment_2 = rotate(robot_center, draw_segment_2, map_pos['rotation'])
                            pygame.draw.line(screen, (127,127,127), draw_segment_1, draw_segment_2, 2)
                        
                ### Update the display (Hardware flip) ###
                pygame.display.flip()
                #print("UPDATE DISPLAY")

                ### Limit frame rate to 60 FPS ###
                clock.tick(60)
                    
            ### Handle closing session down ###

            except KeyboardInterrupt:
                print("\nClosing down due to user request...")
                running = False
            except Exception as e:
                print(f"Error raised: {e}", file=sys.stderr)
                traceback.print_exc()
                running = False
            #finally:
                
        pygame.quit()
        print("Closing RPLidar connection...")
        try:
            lidar.stop_scan()
        except NameError:
            pass
            
        # Generate and store averaged map if it exists
        if voxel_grid_accumulator:
            print("Saving global map to file...")
            final_map = generate_average_map()
            output_file = "averaged_global_map.pcd"
            o3d.io.write_point_cloud(output_file, final_map)
            print(f"Averaged map saved to '{output_file}'!")
            print(f"Amount of unique, stabilized points: {len(final_map.points)}")
            
        print("Done.")

if __name__ == "__main__":
    args = parse_args()
    main(args)
