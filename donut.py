import time
import math
import os

"""

This code is an attempt at replicating the original donut.c code in Python.
The original was written by Andy Sloane as part of The International Obfuscated C Code Contest (IOCCC).
It produces a 3D spinning ascii donut in the terminal. This code is a Python version of the same code.
Check out the explicit and explicit optimised versions of this code to gain a better understanding of what is happening under the hood.
This version factors out the rotation calculations to significantly improve performance of the matrix multiplications.

"""


screen_height = 50
screen_width = 50

theta_space = 0.04
phi_space  = 0.02
R1, R2, K2 = 1, 2, 5
K1 = screen_width * K2 * 2 / (8 * (R1 + R2))

def render_frame(A, B):
    cos_a = math.cos(A)
    sin_a = math.sin(A)
    cos_b = math.cos(B)
    sin_b = math.sin(B)

    output = [[" " for _ in range(screen_width)] for _ in range(screen_height)]
    zbuffer = [[0 for _ in range(screen_width)] for _ in range(screen_height)]
    theta = 0.0
    while theta < math.pi * 2:
        cos_theta, sin_theta = math.cos(theta), math.sin(theta)
        phi = 0.0
        while phi < math.pi * 2:
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            circle_x = R2 + R1 * cos_theta
            circle_y = R1 * sin_theta

            x = circle_x * (cos_b*cos_phi + sin_a*sin_b*sin_phi) - circle_y*cos_a*sin_b
            y = circle_x*(sin_b*cos_phi - sin_a*cos_b*sin_phi) + circle_y*cos_a*cos_b
            z = K2 + cos_a*circle_x*sin_phi + circle_y*sin_a
            ooz = 1/z

            xp = int(screen_width/2 + K1 * ooz * x)
            yp = int(screen_height/2 - K1 * ooz * y)

            # luminance calculation
            L = cos_phi * cos_theta * sin_b - cos_a * cos_theta * sin_phi - sin_a * sin_theta + cos_b * (cos_a * sin_theta - cos_theta * sin_a * sin_phi)
            if 0 <= xp < screen_width and 0 <= yp < screen_height:
                if ooz > zbuffer[yp][xp]:
                    zbuffer[yp][xp] = ooz
                    luminance_index = max(0, min(11, int(8 * L)))
                    output[yp][xp] = ".,-~:;=!*#$@"[luminance_index]
            phi += phi_space
        theta += theta_space
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
        time.sleep(0.03)
