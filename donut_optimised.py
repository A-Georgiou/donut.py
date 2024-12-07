import numpy as np
import time
import math
import os

screen_height = 50
screen_width = 50

theta_spacing = 0.04    # This is the distance between steps for the sweeping angle
phi_spacing  = 0.02     # This is the angle that sweeps around the y-axis
circle_radius = 1       # This is the radius of the circle that forms the torus
edge_distance = 2       # This is the distance from the origin to the edge of the torus
z_distance = 5          # This is the distance from the screen to the center of the torus

# This is the scaling factor that determines how close the torus is to the screen
scale = screen_width * z_distance * 2 / (8 * (circle_radius + edge_distance))

theta_range = np.arange(0, 2 * np.pi, theta_spacing)    # pre-define the theta range
phi_range = np.arange(0, 2 * np.pi, phi_spacing)        # pre-define the phi range
luminance_chars = np.array(list(".,-~:;=!*#$@"))

# Pre-compute 
def create_rotation_matrices(A, B, phi):
    sin_A, cos_A = np.sin(A), np.cos(A)
    sin_B, cos_B = np.sin(B), np.cos(B)
    sin_phi, cos_phi = np.sin(phi), np.cos(phi)
    
    # Pre-calculated 3d rotation matrix
    return np.array([
    [cos_phi*cos_B + sin_phi*sin_A*sin_B,     cos_phi*sin_B - sin_phi*sin_A*cos_B,     sin_phi*cos_A],
    [-cos_A*sin_B,                            cos_A*cos_B,                             sin_A],
    [-sin_phi*cos_B + cos_phi*sin_A*sin_B,    -sin_phi*sin_B - cos_phi*sin_A*cos_B,    cos_phi*cos_A]
    ])

def compute_torus_points():
    points = []
    luminance_vectors = []
    
    for theta in theta_range:
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        # Base circle point
        circle_point = np.array([
            circle_radius * cos_theta + edge_distance,
            circle_radius * sin_theta,
            0
        ])
        
        # Luminance vector
        luminance_vector = np.array([cos_theta, sin_theta, 0])
        
        points.append(circle_point)
        luminance_vectors.append(luminance_vector)
    
    return np.array(points), np.array(luminance_vectors)

def render_frame(A, B):
    output = np.full((screen_height, screen_width), " ", dtype=str)
    zbuffer = np.zeros((screen_height, screen_width))
    
    base_points, base_luminance = compute_torus_points()
    
    for phi in phi_range:
        rot_matrix = create_rotation_matrices(A, B, phi)
        
        # Apply all rotations at once
        points = np.dot(base_points, rot_matrix)
        luminance = np.dot(base_luminance, rot_matrix)

        # Add z distance and calculate projection
        z = points[:, 2] + z_distance
        ooz = 1 / z
        
        # Calculate screen coordinates
        xp = (screen_width / 2 + scale * ooz * points[:, 0]).astype(int)
        yp = (screen_height / 2 - scale * ooz * points[:, 1]).astype(int)
        
        # Calculate luminance
        L = np.dot(luminance, np.array([0, 1, -1]))
        luminance_indices = np.clip((8 * L).astype(int), 0, 11)
        
        # Filter valid coordinates
        mask = (0 <= xp) & (xp < screen_width) & (0 <= yp) & (yp < screen_height)
        
        for i in range(len(points)):
            if mask[i]:
                if ooz[i] > zbuffer[yp[i], xp[i]]:
                    zbuffer[yp[i], xp[i]] = ooz[i]
                    output[yp[i], xp[i]] = luminance_chars[luminance_indices[i]]
    return output

if __name__ == "__main__":
    A, B = 0, 0
    while True:
        print("\x1b[H", end="")
        out = render_frame(A, B)
        for row in out:
            print("\033[92m", " ".join(row), "\033[0m")
        A += 0.08
        B += 0.04
        time.sleep(0.05)