# MOI & Power Calculator - Web Version with Streamlit (Unit Toggle)

import streamlit as st
import math

def calculate_moi_and_power(mass, radius, drop_height, fall_time_s,
                             rpm1, rpm2, coast_time_s, use_metric):
    # Convert inputs to SI units if necessary
    if use_metric:
        mass_kg = mass
        radius_m = radius
        drop_height_m = drop_height
    else:
        mass_kg = mass * 0.453592
        radius_m = radius * 0.0254
        drop_height_m = drop_height * 0.3048

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

    if use_metric:
        return {
            "Linear acceleration (m/s^2)": a,
            "Angular acceleration (rad/s^2)": alpha,
            "Torque from falling mass (N·m)": T,
            "Moment of Inertia (kg·m^2)": I,
            "Coast-down deceleration (rad/s^2)": alpha_f,
            "Friction torque (N·m)": T_f,
            "Total torque (N·m)": T_total,
            "Power (W)": P,
            "Horsepower (HP)": HP,
            "Power Loss (%)": power_loss_percent
        }
    else:
        return {
            "Linear acceleration (ft/s^2)": a / 0.3048,
            "Angular acceleration (rad/s^2)": alpha,
            "Torque from falling mass (ft·lbf)": T / 1.35582,
            "Moment of Inertia (slug·ft^2)": I / 1.35582 * 0.737562149,
            "Coast-down deceleration (rad/s^2)": alpha_f,
            "Friction torque (ft·lbf)": T_f / 1.35582,
            "Total torque (ft·lbf)": T_total / 1.35582,
            "Power (HP)": HP,
            "Power Loss (%)": power_loss_percent
        }

st.title("MOI & Power Loss Calculator")

unit_system = st.radio("Select Unit System", ["Imperial (Standard)", "Metric (SI)"])
use_metric = unit_system == "Metric (SI)"

if use_metric:
    mass = st.number_input("Mass (kg)", min_value=0.0)
    radius = st.number_input("Radius (m)", min_value=0.0)
    drop_height = st.number_input("Drop Height (m)", min_value=0.0)
else:
    mass = st.number_input("Mass (lb)", min_value=0.0)
    radius = st.number_input("Radius (in)", min_value=0.0)
    drop_height = st.number_input("Drop Height (ft)", min_value=0.0)

fall_time_s = st.number_input("Fall Time (s)", min_value=0.01)
rpm1 = st.number_input("Start RPM", min_value=0.0)
rpm2 = st.number_input("End RPM", min_value=0.0)
coast_time_s = st.number_input("Coast-down Time (s)", min_value=0.01)

if st.button("Calculate"):
    try:
        results = calculate_moi_and_power(mass, radius, drop_height, fall_time_s,
                                          rpm1, rpm2, coast_time_s, use_metric)
        for key, value in results.items():
            st.write(f"{key}: {value:.3f}")
    except Exception as e:
        st.error(f"Error: {e}")
