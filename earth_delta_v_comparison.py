#!/usr/bin/env python
# coding: utf-8

# In[1]:


# ==========================================================
# Simple Poliastro demo: tiny delta-v, big orbital changes
# Two satellites, same start, slightly different burns
# ==========================================================

from astropy import units as u
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle

from poliastro.bodies import Earth
from poliastro.twobody import Orbit

def main():
    # -----------------------------
    # 1. Base circular orbit (LEO)
    # -----------------------------
    alt = 500 * u.km                       # altitude above Earth
    orb_base = Orbit.circular(Earth, alt=alt)

    # Position and velocity at t0
    r0, v0 = orb_base.rv()                # r0 [km], v0 [km/s]

    # ---------------------------------------
    # 2. Ask user for two burn magnitudes
    #    (pure tangential, along-track)
    # ---------------------------------------
    print("Two satellites start on the SAME circular orbit.")
    print("Now choose two tangential burns (delta-v) in m/s.")
    print("Example: 0 and 10, or 10 and 20 etc.\n")

    dv1_str = input("Delta-v for Satellite A (m/s): ").strip()
    dv2_str = input("Delta-v for Satellite B (m/s): ").strip()

    # Fallback defaults if user just presses Enter
    dv1 = float(dv1_str) if dv1_str else 0.0
    dv2 = float(dv2_str) if dv2_str else 10.0

    dv1_q = (dv1 * u.m / u.s).to(u.km / u.s)   # convert to km/s
    dv2_q = (dv2 * u.m / u.s).to(u.km / u.s)

    # Direction of current velocity (unit vector)
    v0_kms = v0.to(u.km / u.s)
    v0_mag = np.linalg.norm(v0_kms.value) * (u.km / u.s)
    v_hat = v0_kms / v0_mag                   # dimensionless

    # New velocities after burns
    vA = v0_kms + v_hat * dv1_q
    vB = v0_kms + v_hat * dv2_q

    # Construct new orbits for the two satellites
    orb_A = Orbit.from_vectors(Earth, r0, vA, epoch=orb_base.epoch)
    orb_B = Orbit.from_vectors(Earth, r0, vB, epoch=orb_base.epoch)

    # ------------------------------------
    # 3. Propagate a few orbital periods
    # ------------------------------------
    n_periods = 8
    total_time = n_periods * orb_base.period
    n_points = 600

    ts = np.linspace(0.0, total_time.to(u.s).value, n_points) * u.s

    rs_base = np.zeros((n_points, 3))
    rs_A    = np.zeros((n_points, 3))
    rs_B    = np.zeros((n_points, 3))

    for i, dt in enumerate(ts):
        rs_base[i, :] = orb_base.propagate(dt).r.to(u.km).value
        rs_A[i, :]    = orb_A.propagate(dt).r.to(u.km).value
        rs_B[i, :]    = orb_B.propagate(dt).r.to(u.km).value

    # We will plot in the orbital plane (x-y)
    x_base, y_base = rs_base[:, 0], rs_base[:, 1]
    x_A,    y_A    = rs_A[:, 0],    rs_A[:, 1]
    x_B,    y_B    = rs_B[:, 0],    rs_B[:, 1]

    # ------------------------------------
    # 4. Plotting
    # ------------------------------------
    fig, ax = plt.subplots(figsize=(7, 7))

    # Earth as a black disk
    R_earth = Earth.R.to(u.km).value
    earth = Circle((0, 0), R_earth, facecolor="black", edgecolor="black", alpha=0.9)
    ax.add_patch(earth)

    # Orbits
    ax.plot(x_base, y_base, linestyle="--", linewidth=1.2, label="Original orbit")
    ax.plot(x_A, y_A, linewidth=2.0, label=f"Satellite A (Δv = {dv1:.1f} m/s)")
    ax.plot(x_B, y_B, linewidth=2.0, label=f"Satellite B (Δv = {dv2:.1f} m/s)")

    # Starting point
    ax.scatter(r0.to(u.km).value[0], r0.to(u.km).value[1],
               s=40, color="red", zorder=5, label="Burn point")

    # Make it look nice
    ax.set_xlabel("x [km]")
    ax.set_ylabel("y [km]")
    ax.set_title("Tiny change in delta-v, big change in orbit (2D view)")
    ax.grid(True, linestyle=":", linewidth=0.7)
    ax.set_aspect("equal", "box")
    ax.legend(loc="upper right")

    # Tight limits around orbits
    all_x = np.concatenate([x_base, x_A, x_B])
    all_y = np.concatenate([y_base, y_A, y_B])
    max_range = 1.05 * max(all_x.max() - all_x.min(),
                           all_y.max() - all_y.min()) / 2.0
    x_mid = 0.5 * (all_x.max() + all_x.min())
    y_mid = 0.5 * (all_y.max() + all_y.min())
    ax.set_xlim(x_mid - max_range, x_mid + max_range)
    ax.set_ylim(y_mid - max_range, y_mid + max_range)

    # Print some numbers you can quote in an interview
    print("\n--- Numbers you can talk about ---")
    print(f"Base circular-orbit speed   : {v0_mag.to(u.km / u.s).value:.4f} km/s")
    print(f"Satellite A speed after burn: {(np.linalg.norm(vA.value)):.4f} km/s")
    print(f"Satellite B speed after burn: {(np.linalg.norm(vB.value)):.4f} km/s")
    print(f"Δv A: {dv1:.2f} m/s, Δv B: {dv2:.2f} m/s")
    print("Both start together, but after a few orbits the paths no longer line up.\n")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()


# In[ ]:




