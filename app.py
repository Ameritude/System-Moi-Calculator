# MOI & Power Calculator - Web Version with Streamlit

import streamlit as st
import math

def calculate_moi_and_power(mass_kg, radius_m, drop_height_m, fall_time_s,
                             rpm1, rpm2, coast_time_s):
    g = 9.81
    a = (2 * drop_height_m) / fall_time_s**2
    alpha = a / radius_m
    T = radius_m * mass_kg * (g - a)
    I = T / alpha

    omega1 = rpm1 * (2 * math.pi / 60)
    omega2 = rpm2 * (2 * math.pi / 60)
    alpha_f = (omega2 - omega1) / coast_time_s
    T_f = abs(I * alpha_f)
    T_total = I * alpha + T_f
    omega_operating = omega1
    P = T_total * omega_operating
    HP = P / 745.7
    power_loss_percent = (T_f / T_total) * 100

    return {
        "Linear acceleration (m/s^2)": a,
        "Angular acceleration (rad/s^2)": alpha,
        "Torque from falling mass (N*m)": T,
        "Moment of Inertia (kg*m^2)": I,
        "Coast-down deceleration (rad/s^2)": alpha_f,
        "Friction torque (N*m)": T_f,
        "Total torque (N*m)": T_total,
        "Power (W)": P,
        "Horsepower (HP)": HP,
        "Power Loss (%)": power_loss_percent
    }

st.title("MOI & Power Loss Calculator")

mass_kg = st.number_input("Mass (kg)", min_value=0.0)
radius_m = st.number_input("Radius (m)", min_value=0.0)
drop_height_m = st.number_input("Drop Height (m)", min_value=0.0)
fall_time_s = st.number_input("Fall Time (s)", min_value=0.01)
rpm1 = st.number_input("Start RPM", min_value=0.0)
rpm2 = st.number_input("End RPM", min_value=0.0)
coast_time_s = st.number_input("Coast-down Time (s)", min_value=0.01)

if st.button("Calculate"):
    try:
        results = calculate_moi_and_power(mass_kg, radius_m, drop_height_m, fall_time_s,
                                          rpm1, rpm2, coast_time_s)
        for key, value in results.items():
            st.write(f"{key}: {value:.3f}")
    except Exception as e:
        st.error(f"Error: {e}")
