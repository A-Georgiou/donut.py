# donut.py 🍩

A Python implementation of the famous "donut.c" ASCII art animation, with explicit and optimized versions for learning purposes.

## Overview

This project provides three implementations of the rotating ASCII donut animation, originally created by Andy Sloane:

1. `donut.py` - The base implementation
2. `donut_explicit.py` - A detailed, step-by-step version with clear mathematical operations
3. `donut_optimized.py` - A performance-optimized version using NumPy

## How It Works

The program creates a 3D ASCII animation of a rotating torus (donut) in your terminal. It achieves this by:

- Generating a torus through parametric equations
- Applying 3D rotations using rotation matrices
- Calculating surface luminance for shading
- Projecting 3D points onto the 2D terminal screen.
- Rendering ASCII characters based on luminance values

## Usage

```bash
# Run the base version
python donut.py

# Run the explicit version
python donut_explicit.py

# Run the optimized version
python donut_optimized.py
```

## Parameters

You can modify these variables to experiment with the visualization:

```python
SCREEN_HEIGHT = 50         # Terminal display height
SCREEN_WIDTH = 50          # Terminal display width
theta_spacing = 0.04       # Angle step for torus generation
phi_spacing = 0.02         # Rotation step around y-axis
circle_radius = 1          # Inner radius of the torus
edge_distance = 2          # Outer radius of the torus
```

## Acknowledgments

Based on Andy Sloane's original [donut.c](https://www.a1k0n.net/2011/07/20/donut-math.html) code, which was submitted to The International Obfuscated C Code Contest (IOCCC).
