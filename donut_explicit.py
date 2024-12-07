import numpy as np
import time
import math
import os

SCREEN_HEIGHT = 50
SCREEN_WIDTH = 50

theta_spacing = 0.04    # This is the distance between steps for the sweeping angle
phi_spacing  = 0.02     # This is the angle that sweeps around the y-axis
circle_radius = 1       # This is the radius of the circle that forms the torus
edge_distance = 2       # This is the distance from the origin to the edge of the torus
z_distance = 5          # This is the distance from the screen to the center of the torus

# This is the scaling factor that determines how close the torus is to the screen
scale = SCREEN_WIDTH * z_distance * 2 / (8 * (circle_radius + edge_distance))

# This does a rotation around the y-axis for a 3d coordinate.
# applies the rotation matrix to the point and returns the new point
def rotate_on_y_axis(point, theta):
    rotation_matrix = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])
    return np.dot(rotation_matrix, point)

# This does a rotation around the x-axis for a 3d coordinate.
# applies the rotation matrix to the point and returns the new point
def rotate_on_x_axis(point, A):
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(A), np.sin(A)],
        [0, -np.sin(A), np.cos(A)]
    ])
    return np.dot(rotation_matrix, point)

# This does a rotation around the z-axis for a 3d coordinate.
# applies the rotation matrix to the point and returns the new point
def rotate_on_z_axis(point, B):
    rotation_matrix = np.array([
        [np.cos(B), np.sin(B), 0],
        [-np.sin(B), np.cos(B), 0],
        [0, 0, 1]
    ])
    return np.dot(rotation_matrix, point)

# Explicitly rotates the torus by the x-axis and z-axis
# Since we generate the torus by rotating around the y-axis already we skip that in this step.
def rotate_torus(torus_point, A, B):
    return rotate_on_z_axis(rotate_on_x_axis(torus_point, A), B)

# Generates a single point on the torus given the current theta and phi angles (which are the angles that sweep around the torus)
def compute_torus(theta, phi):
    distance_from_center = np.array([edge_distance, 0, 0])
    circle_point = np.array([circle_radius * np.cos(theta), circle_radius * np.sin(theta), 0])
    offset_circle_point = distance_from_center + circle_point
    rotated_point = rotate_on_y_axis(offset_circle_point, phi)
    return rotated_point

# Computes the luminance of a point on the torus given the current theta and phi angles.
# Luminance is calculated as the dot product of the surface normal and the light direction.
def compute_luminance(theta, phi, A, B):
    luminance_origin = np.array([np.cos(theta), np.sin(theta), 0])
    rotated_luminance_point = rotate_on_z_axis(rotate_on_x_axis(rotate_on_y_axis(luminance_origin, phi), A), B)
    return np.dot(rotated_luminance_point, np.array([0, 1, -1]))

# Creates a single ascii frame of the torus given the current A and B angles
def render_frame(A, B):
    output = [[" " for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
    zbuffer = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
    theta = 0.0
    while theta < math.pi * 2:
        phi = 0.0
        while phi < math.pi * 2:
            torus_point = compute_torus(theta, phi)
            x, y, z = rotate_torus(torus_point, A, B)
            z = z + z_distance
            ooz = 1 / z

            xp = int(SCREEN_WIDTH / 2 + scale * ooz * x)
            yp = int(SCREEN_HEIGHT / 2 - scale * ooz * y)

            luminance = compute_luminance(theta, phi, A, B)
            if 0 <= xp < SCREEN_WIDTH and 0 <= yp < SCREEN_HEIGHT:
                if ooz > zbuffer[yp][xp]:
                    zbuffer[yp][xp] = ooz
                    luminance_index = max(0, min(11, int(8 * luminance)))
                    output[yp][xp] = ".,-~:;=!*#$@"[luminance_index]
            phi += phi_spacing
        theta += theta_spacing
    return output

if __name__ == "__main__":
    A, B = 0, 0
    while True:
        print("\x1b[H", end="")
        out = render_frame(A, B)
        for row in out:
            print("\033[92m"," ".join(row),"\033[0m")
        A += 0.08
        B += 0.04
        time.sleep(0.025)