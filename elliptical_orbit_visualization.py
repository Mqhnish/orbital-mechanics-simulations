#!/usr/bin/env python
# coding: utf-8

# In[2]:


from astropy import units as u
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from poliastro.bodies import Earth
from poliastro.twobody import Orbit


def main():
    # --- 1. Define a simple elliptical orbit (Earth-centered) ---
    epoch = Time("2025-01-01 00:00:00", scale="utc")

    a = 26560 * u.km         # semi-major axis (like a GNSS orbit)
    ecc = 0.72 * u.one       # fairly eccentric
    inc = 63.4 * u.deg       # critical inclination
    raan = 0.0 * u.deg
    argp = 270.0 * u.deg
    nu = 0.0 * u.deg

    orb = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu, epoch=epoch)
    print(orb)               # quick text summary

    # --- 2. Sample one full period of the orbit ---
    num_points = 500
    ts = np.linspace(0.0, orb.period.to(u.s).value, num_points) * u.s

    rs = np.zeros((num_points, 3))  # positions [km]
    for i, dt in enumerate(ts):
        r_vec = orb.propagate(dt).r.to(u.km).value
        rs[i, :] = r_vec

    # --- 3. 3D plot with a black Earth ---
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Orbit path
    ax.plot(rs[:, 0], rs[:, 1], rs[:, 2], linewidth=2.0, label="Orbit")

    # Draw Earth as a black sphere
    R_earth = Earth.R.to(u.km).value
    u_sphere = np.linspace(0, 2 * np.pi, 60)
    v_sphere = np.linspace(0, np.pi, 30)
    xs = R_earth * np.outer(np.cos(u_sphere), np.sin(v_sphere))
    ys = R_earth * np.outer(np.sin(u_sphere), np.sin(v_sphere))
    zs = R_earth * np.outer(np.ones_like(u_sphere), np.cos(v_sphere))
    ax.plot_surface(xs, ys, zs, color="k", alpha=0.7, linewidth=0)

    # Labels and cosmetics
    ax.set_xlabel("x [km]")
    ax.set_ylabel("y [km]")
    ax.set_zlabel("z [km]")
    ax.set_title("Simple Earth Orbit (poliastro quickstart-style)")
    ax.legend()

    # Equal aspect ratio
    max_range = np.array([
        rs[:, 0].max() - rs[:, 0].min(),
        rs[:, 1].max() - rs[:, 1].min(),
        rs[:, 2].max() - rs[:, 2].min()
    ]).max() / 2.0

    mid_x = (rs[:, 0].max() + rs[:, 0].min()) * 0.5
    mid_y = (rs[:, 1].max() + rs[:, 1].min()) * 0.5
    mid_z = (rs[:, 2].max() + rs[:, 2].min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()


# In[ ]:




