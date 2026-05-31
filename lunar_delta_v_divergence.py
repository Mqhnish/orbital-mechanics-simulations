#!/usr/bin/env python
# coding: utf-8

# In[14]:


import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from poliastro.bodies import Moon
from poliastro.twobody import Orbit
from astropy import units as u


def make_orbit_with_tangential_burn(orbit_base, dv_ms):
    r0, v0 = orbit_base.rv()
    dv = (dv_ms * u.m / u.s).to(u.km / u.s)

    v0_kms = v0.to(u.km / u.s)
    v_mag = np.linalg.norm(v0_kms.value) * (u.km / u.s)
    v_hat = v0_kms / v_mag

    v_new = v0_kms + v_hat * dv
    return Orbit.from_vectors(Moon, r0, v_new)


def propagate_positions(orbit, ts):
    # FIXED: safe propagation for all Poliastro versions
    xyz = np.zeros((len(ts), 3))
    for i, dt in enumerate(ts):
        xyz[i] = orbit.propagate(dt).r.to(u.km).value
    return xyz


def main():
    try:
        dvA_ms = float(input("Delta-v for satellite A (default 0): ") or 0.0)
        dvB_ms = float(input("Delta-v for satellite B (default 5): ") or 5.0)
    except ValueError:
        print("Invalid input, using defaults.")
        dvA_ms, dvB_ms = 0.0, 5.0

    alt = 100.0 * u.km
    orb_base = Orbit.circular(Moon, alt=alt)

    orb_A = make_orbit_with_tangential_burn(orb_base, dvA_ms)
    orb_B = make_orbit_with_tangential_burn(orb_base, dvB_ms)

    n_periods = 20
    num_points = 1000
    total_time = n_periods * orb_base.period
    ts = np.linspace(0.0, total_time.to(u.s).value, num_points) * u.s

    pos_A = propagate_positions(orb_A, ts)
    pos_B = propagate_positions(orb_B, ts)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(*pos_A.T, linewidth=1.5, label=f"Sat A (dv = {dvA_ms:.2f} m/s)")
    ax.plot(*pos_B.T, linewidth=1.5, label=f"Sat B (dv = {dvB_ms:.2f} m/s)")

    r0 = orb_base.r.to(u.km).value
    ax.scatter(*r0, s=40, marker="o", label="Burn point")

    R_moon = Moon.R.to(u.km).value * 0.7
    u_s = np.linspace(0, 2 * np.pi, 20)
    v_s = np.linspace(0, np.pi, 10)
    x = R_moon * np.outer(np.cos(u_s), np.sin(v_s))
    y = R_moon * np.outer(np.sin(u_s), np.sin(v_s))
    z = R_moon * np.outer(np.ones_like(u_s), np.cos(v_s))
    ax.plot_surface(x, y, z, color="k", alpha=0.2, linewidth=0)

    ax.set(xlabel="x [km]", ylabel="y [km]", zlabel="z [km]",
           title="Tiny delta-v in lunar orbit – divergence over time")
    ax.legend(loc="upper left")

    # Aspect ratio fixed
    all_pts = np.vstack([pos_A, pos_B])
    max_range = (all_pts.max(axis=0) - all_pts.min(axis=0)).max() * 0.5
    mid = (all_pts.max(axis=0) + all_pts.min(axis=0)) * 0.5

    ax.set_xlim(mid[0] - max_range, mid[0] + max_range)
    ax.set_ylim(mid[1] - max_range, mid[1] + max_range)
    ax.set_zlim(mid[2] - max_range, mid[2] + max_range)

    plt.tight_layout()
    plt.show()

    _, vA = orb_A.rv()
    _, vB = orb_B.rv()
    print(f"\nSpeed A: {np.linalg.norm(vA.to(u.km/u.s).value):.5f} km/s")
    print(f"Speed B: {np.linalg.norm(vB.to(u.km/u.s).value):.5f} km/s")
    print(f"Δv difference: {dvB_ms - dvA_ms:.3f} m/s")


if __name__ == "__main__":
    main()


# In[ ]:




