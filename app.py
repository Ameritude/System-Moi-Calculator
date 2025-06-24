# MOI & Friction Loss Calculator with Improved UI and Test Instructions

import streamlit as st
import math

def calculate_moi(mass, radius, drop_height, fall_time_s, use_metric):
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

    return I, a, alpha, T

def calculate_friction(I, rpm1, rpm2, coast_time_s):
    omega1 = rpm1 * (2 * math.pi / 60)
    omega2 = rpm2 * (2 * math.pi / 60)
    alpha_f = (omega2 - omega1) / coast_time_s
    T_f = abs(I * alpha_f)
    return alpha_f, T_f

def convert_units(I, T, T_f, a, use_metric):
    if use_metric:
        return {
            "MOI": I,
            "Torque": T,
            "Friction Torque": T_f,
            "Linear Acceleration": a,
            "MOI Unit": "kg·m²",
            "Torque Unit": "N·m"
        }
    else:
        return {
            "MOI": I / 1.35582 * 0.737562149,
            "Torque": T / 1.35582,
            "Friction Torque": T_f / 1.35582,
            "Linear Acceleration": a / 0.3048,
            "MOI Unit": "slug·ft²",
            "Torque Unit": "ft·lbf"
        }

def calculate_correction_factor(T_f, I, alpha):
    if alpha == 0:
        return 1.0
    return 1 + (T_f / (I * alpha))

def minutes_to_seconds(minutes):
    return minutes * 60

st.set_page_config(page_title="MOI & Friction Loss Tool", layout="centered")
st.title("🔧 MOI & Friction Loss Calculator")
st.caption("Use this tool to determine your system's moment of inertia and frictional power loss multiplier.")

unit_system = st.radio("⚙️ Select Unit System", ["Imperial (Standard)", "Metric (SI)"])
use_metric = unit_system == "Metric (SI)"

st.header("① Drop Test: Measure Moment of Inertia")
st.markdown("""
**Instructions:**
1. Attach a known mass to your rotating system with a string wound around a pulley (or drum).
2. Measure the radius from the center of rotation to the point where the string pulls.
3. Measure how far the weight drops (vertical distance).
4. Time how long it takes for the mass to fall this distance after release.
""")
col1, col2 = st.columns(2)
with col1:
    mass = st.number_input("Mass attached to string ({}):".format("kg" if use_metric else "lb"), min_value=0.0)
    radius = st.number_input("Effective radius of pulley ({}):".format("m" if use_metric else "in"), min_value=0.0)
with col2:
    drop_height = st.number_input("Vertical drop height ({}):".format("m" if use_metric else "ft"), min_value=0.0)
    drop_time_unit = st.radio("Drop Time Unit", ["Seconds", "Minutes"], horizontal=True, key="drop_time_unit")
    if drop_time_unit == "Minutes":
        fall_minutes = st.number_input("Drop time (min):", min_value=0.0, step=0.1)
        fall_time_s = minutes_to_seconds(fall_minutes)
    else:
        fall_time_s = st.number_input("Drop time (sec):", min_value=0.01)

st.header("② Coast-Down Test: Measure Frictional Loss")
st.markdown("""
**Instructions:**
1. Spin the system up to a known RPM.
2. Measure the RPM at the start and the point where it comes to rest or a lower RPM.
3. Record the time between these two RPM points.
""")
col3, col4 = st.columns(2)
with col3:
    rpm1 = st.number_input("Start RPM (before coast-down):", min_value=0.0)
with col4:
    rpm2 = st.number_input("End RPM (after coast-down):", min_value=0.0)
coast_time_unit = st.radio("Coast-Down Time Unit", ["Seconds", "Minutes"], horizontal=True, key="coast_time_unit")
if coast_time_unit == "Minutes":
    coast_minutes = st.number_input("Coast-down time (min):", min_value=0.0, step=0.1)
    coast_time_s = minutes_to_seconds(coast_minutes)
else:
    coast_time_s = st.number_input("Coast-down time (sec):", min_value=0.01)

if st.button("✅ Calculate"):
    try:
        I, a, alpha, T = calculate_moi(mass, radius, drop_height, fall_time_s, use_metric)
        alpha_f, T_f = calculate_friction(I, rpm1, rpm2, coast_time_s)
        converted = convert_units(I, T, T_f, a, use_metric)
        correction_factor = calculate_correction_factor(T_f, I, alpha)

        st.markdown("---")
        st.subheader("📊 Drop Test Results")
        st.write(f"• Moment of Inertia: `{converted['MOI']:.4f} {converted['MOI Unit']}`")
        st.write(f"• Torque from Falling Mass: `{converted['Torque']:.3f} {converted['Torque Unit']}`")
        st.write(f"• Linear Acceleration: `{converted['Linear Acceleration']:.3f} {'m/s²' if use_metric else 'ft/s²'}`")

        st.subheader("📉 Coast-Down Results")
        st.write(f"• Angular Deceleration: `{alpha_f:.4f} rad/s²`")
        st.write(f"• Friction Torque: `{converted['Friction Torque']:.3f} {converted['Torque Unit']}`")

        st.markdown("---")
        st.subheader("✅ Final Summary")
        st.success(f"System Moment of Inertia: {converted['MOI']:.4f} {converted['MOI Unit']}")
        st.success(f"Horsepower Correction Multiplier: {correction_factor:.4f}x")
        st.caption("Multiply any dyno-measured horsepower value by this factor to correct for system losses.")

    except Exception as e:
        st.error(f"Error during calculation: {e}")
    except Exception as e:
        st.error(f"Error during calculation: {e}")



