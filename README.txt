# Orbital Mechanics Simulations

A collection of orbital mechanics simulations built using Python, Poliastro, Astropy, NumPy, and Matplotlib.

This project explores how spacecraft trajectories evolve under different orbital conditions and maneuvers, including delta-v burns, orbital transfers, and highly elliptical Earth-centered orbits.

---

## Simulations Included

### 1. Lunar Delta-V Divergence

**File:** `lunar_delta_v_divergence.py`

Demonstrates how extremely small velocity changes can cause significant divergence in lunar orbits over time.

Features:
- Lunar orbit propagation
- User-defined delta-v maneuvers
- 3D trajectory visualization
- Long-term orbital divergence analysis

Key Idea:

> Small changes in velocity accumulate over multiple orbits and can produce dramatically different trajectories.

---

### 2. Earth Delta-V Comparison

**File:** `earth_delta_v_comparison.py`

Simulates two satellites beginning in the same Low Earth Orbit (LEO) and receiving slightly different tangential burns.

Features:
- Circular Earth orbit
- Two-satellite comparison
- Delta-v sensitivity demonstration
- Orbital separation visualization

Key Idea:

> Even tiny differences in applied delta-v lead to increasing separation over time.


---

### 3. Elliptical Orbit Visualization

**File:** `elliptical_orbit_visualization.py`

Visualizes a highly eccentric Earth-centered orbit in three dimensions.

Orbital Parameters:
- Semi-major axis: 26,560 km
- Eccentricity: 0.72
- Inclination: 63.4°

Features:
- 3D orbit rendering
- Earth-centered propagation
- High-eccentricity trajectory visualization

---

### 4. Hohmann Transfer Visualization

**File:** `hohmann_transfer_visualization.py`

Demonstrates a Hohmann transfer between two circular Earth orbits.

Features:
- Initial orbit
- Transfer orbit
- Final orbit
- Transfer maneuver visualization

Key Idea:

> Hohmann transfers provide one of the most fuel-efficient methods for transferring between coplanar circular orbits.

---

## Technologies Used

- Python
- Poliastro
- Astropy
- NumPy
- Matplotlib

---

## Concepts Demonstrated

- Orbital propagation
- Delta-v maneuvers
- Hohmann transfers
- Keplerian motion
- Orbital sensitivity
- Spacecraft trajectory analysis
- 2D and 3D visualization

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Requirements

```text
numpy
matplotlib
astropy
poliastro
```

---

## Educational Purpose

These simulations were developed to explore fundamental aerospace engineering and astrodynamics concepts through computational modeling and visualization.

The project focuses on understanding how small velocity changes affect orbital trajectories and how spacecraft can efficiently transfer between different orbital regimes.
