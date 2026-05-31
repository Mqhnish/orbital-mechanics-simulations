#!/usr/bin/env python
# coding: utf-8

# In[5]:


from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.maneuver import Maneuver


def propagate_orbit(orbit, n_points=600):
    ts = np.linspace(0, orbit.period.to(u.s).value, n_points) * u.s

    positions = np.zeros((n_points, 3))

    for i, t in enumerate(ts):
        positions[i] = orbit.propagate(t).r.to(u.km).value

    return positions


def main():
    # ==========================================================
    # Initial Orbit
    # ==========================================================

    initial_orbit = Orbit.circular(Earth, alt=700 * u.km)

    print("Initial orbit:")
    print(initial_orbit)

    # ==========================================================
    # Hohmann Transfer
    # ==========================================================

    transfer = Maneuver.hohmann(initial_orbit, 36000 * u.km)

    transfer_orbit, final_orbit = initial_orbit.apply_maneuver(
        transfer,
        intermediate=True
    )

    print("\nTransfer orbit:")
    print(transfer_orbit)

    print("\nFinal orbit:")
    print(final_orbit)

    # ==========================================================
    # Propagate trajectories
    # ==========================================================

    r_initial = propagate_orbit(initial_orbit)
    r_transfer = propagate_orbit(transfer_orbit)
    r_final = propagate_orbit(final_orbit)

    # ==========================================================
    # Plot
    # ==========================================================

    fig, ax = plt.subplots(figsize=(8, 8))

    # Earth

    R_earth = Earth.R.to(u.km).value

    earth = Circle(
        (0, 0),
        R_earth,
        facecolor="black",
        edgecolor="black",
        alpha=0.9
    )

    ax.add_patch(earth)

    # Orbits

    ax.plot(
        r_initial[:, 0],
        r_initial[:, 1],
        linewidth=2,
        label="Initial Orbit"
    )

    ax.plot(
        r_transfer[:, 0],
        r_transfer[:, 1],
        linewidth=2,
        linestyle="--",
        label="Transfer Orbit"
    )

    ax.plot(
        r_final[:, 0],
        r_final[:, 1],
        linewidth=2,
        label="Final Orbit"
    )

    # Burn point

    burn_point = initial_orbit.r.to(u.km).value

    ax.scatter(
        burn_point[0],
        burn_point[1],
        s=40,
        color="red",
        label="Burn Point"
    )

    # ==========================================================
    # Formatting
    # ==========================================================

    ax.set_title("Hohmann Transfer Between Circular Earth Orbits")
    ax.set_xlabel("x [km]")
    ax.set_ylabel("y [km]")

    ax.grid(True, linestyle=":")
    ax.set_aspect("equal", "box")

    ax.legend()

    # Nice limits

    all_x = np.concatenate([
        r_initial[:, 0],
        r_transfer[:, 0],
        r_final[:, 0]
    ])

    all_y = np.concatenate([
        r_initial[:, 1],
        r_transfer[:, 1],
        r_final[:, 1]
    ])

    max_range = max(
        all_x.max() - all_x.min(),
        all_y.max() - all_y.min()
    ) / 2

    x_mid = (all_x.max() + all_x.min()) / 2
    y_mid = (all_y.max() + all_y.min()) / 2

    ax.set_xlim(
        x_mid - max_range * 1.1,
        x_mid + max_range * 1.1
    )

    ax.set_ylim(
        y_mid - max_range * 1.1,
        y_mid + max_range * 1.1
    )

    plt.tight_layout()

    plt.savefig(
        "hohmann_transfer.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("\nPlot saved as:")
    print("hohmann_transfer.png")


if __name__ == "__main__":
    main()


# In[ ]:




