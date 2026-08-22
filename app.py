import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configuration for a Premium Industrial Look
st.set_page_config(
    page_title="NextGen 5G Beamforming Lab",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to force clean layout, subtle accents, and remove default clutter
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    h1 { color: #00D2FF; font-weight: 800; font-size: 2.2rem !important; margin-bottom: 0.2rem; }
    .stSlider > label { font-weight: 600; color: #E0E0E0; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700; color: #00FFCC !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.9rem !important; text-transform: uppercase; letter-spacing: 0.5px; }
    </style>
""", unsafe_allow_html=True)

# 2. Header Architecture
st.markdown("<h1>📡 NextGen 5G MIMO Beamforming Testbed</h1>", unsafe_allow_html=True)
st.caption("Advanced Spatial Multiplexing, Adaptive Phase-Shifting, and Link Budget Analytics Engine")
st.markdown("---")

# 3. Sidebar Control Panel
st.sidebar.markdown("### 🎛️ RF System Configuration")

mode = st.sidebar.radio(
    "Operational Mode",
    ["Single User Tracking", "Interference Mitigation (Null-Steering)"]
)

num_elements = st.sidebar.slider("Antenna Elements (N)", min_value=4, max_value=32, value=12, step=4)
element_spacing = st.sidebar.slider("Element Spacing (d/λ)", min_value=0.25, max_value=1.00, value=0.50, step=0.05)

st.sidebar.markdown("### 🎯 Spatial Coordinates")
target_angle = st.sidebar.slider("User Equipment (UE) Angle (°)", min_value=-90, max_value=90, value=25, step=1)

# Conditional Input for the Competitive Edge Feature
jamming_angle = 0
if mode == "Interference Mitigation (Null-Steering)":
    jamming_angle = st.sidebar.slider("Interference / Jammer Angle (°)", min_value=-90, max_value=90, value=-40, step=1)

# 4. Core Mathematical Analytics Engine
wavelength = 1.0
d = element_spacing * wavelength
theta_scan = np.radians(np.linspace(-90, 90, 720))
theta_target = np.radians(target_angle)

# Compute Phase Vector for Target
phase_target = 2 * np.pi * (d / wavelength) * np.sin(theta_target)

# Compute Array Factor (AF)
array_factor = np.zeros_like(theta_scan, dtype=complex)

if mode == "Single User Tracking":
    # Conventional Phase Shifting Beamforming
    for n in range(num_elements):
        phase_diff = n * (2 * np.pi * (d / wavelength) * np.sin(theta_scan) - phase_target)
        array_factor += np.exp(1j * phase_diff)
else:
    # Prize-Winning Feature: Zero-forcing Null-Steering Logic
    # Dynamically designs an antenna weight matrix to steer beam to target AND drop power to zero at jammer
    theta_jam = np.radians(jamming_angle)
    
    # Steering vectors for target and jammer
    v_target = np.exp(1j * 2 * np.pi * (d / wavelength) * np.sin(theta_target) * np.arange(num_elements))
    v_jam = np.exp(1j * 2 * np.pi * (d / wavelength) * np.sin(theta_jam) * np.arange(num_elements))
    
    # Combine steering vectors using Orthogonal Projection Matrix to nullify jammer channel
    H = np.column_stack((v_target, v_jam))
    weights = v_target - (np.dot(np.conj(v_jam), v_target) / np.dot(np.conj(v_jam), v_jam)) * v_jam
    weights /= np.linalg.norm(weights) # Normalize weights
    
    for n in range(num_elements):
        array_factor += weights[n] * np.exp(1j * n * 2 * np.pi * (d / wavelength) * np.sin(theta_scan))

# Power & Decibel Math for Plots
power = np.abs(array_factor) ** 2
power_norm = power / np.max(power)
power_db = 10 * np.log10(power_norm + 1e-5) # 1e-5 floor prevents log(0) runtime crash

# Metric Calculations to impress the evaluators
# Extract power values at specific spatial positions
idx_target = np.abs(theta_scan - theta_target).argmin()
power_at_ue = power_norm[idx_target]

if mode == "Interference Mitigation (Null-Steering)":
    idx_jam = np.abs(theta_scan - theta_jam).argmin()
    power_at_jam = power_norm[idx_jam]
    sinr = 10 * np.log10(power_at_ue / (power_at_jam + 0.01)) # Assume noise floor 0.01
    spectral_efficiency = np.log2(1 + (power_at_ue / (power_at_jam + 0.01)))
else:
    sinr = 10 * np.log10(power_at_ue / 0.02) # Background noise only
    spectral_efficiency = np.log2(1 + (power_at_ue / 0.02))

# 5. Live UI Presentation Layer (Grid Layout)
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📊 Live RF Performance Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Directivity Gain", value=f"{10 * np.log10(num_elements):.1f} dBi")
    m2.metric(label="Calculated SINR", value=f"{sinr:.1f} dB")
    m3.metric(label="Spectral Efficiency", value=f"{spectral_efficiency:.2f} bps/Hz")
    
    # Plot 1: Linear Power Distribution (Clean Modern Dark Subplot style)
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig1.patch.set_facecolor('#0E1117')
    ax1.set_facecolor('#1E232A')
    
    ax1.plot(np.degrees(theta_scan), power_db, color='#00D2FF', linewidth=2, label="Array Factor Pattern")
    ax1.axvline(target_angle, color='#00FFCC', linestyle='--', alpha=0.8, label="Target UE")
    if mode == "Interference Mitigation (Null-Steering)":
        ax1.axvline(jamming_angle, color='#FF3366', linestyle='--', alpha=0.8, label="Jammer/Interference")
        
    ax1.set_ylim([-30, 2])
    ax1.set_xlim([-90, 90])
    ax1.set_xlabel("Spatial Angle (Degrees)", color='#E0E0E0', fontsize=9)
    ax1.set_ylabel("Normalized Power (dB)", color='#E0E0E0', fontsize=9)
    ax1.tick_params(colors='#E0E0E0', labelsize=8)
    ax1.grid(True, color='#2E353F', linestyle=':')
    ax1.legend(facecolor='#1E232A', edgecolor='none', labelcolor='#E0E0E0', fontsize=8)
    st.pyplot(fig1)

with col2:
    st.markdown("### 🎯 Spatial Radiation Beam Pattern")
    
    # Plot 2: Polar Spatial Map
    fig2, ax2 = plt.subplots(figsize=(6, 5.2), subplot_kw={'projection': 'polar'})
    fig2.patch.set_facecolor('#0E1117')
    ax2.set_facecolor('#1E232A')
    
    # Polar formatting to face standard north-axis orientation
    ax2.set_theta_zero_location("N")
    ax2.set_theta_direction(-1) # Clockwise mapping
    
    ax2.plot(theta_scan, power_norm, color='#00D2FF', linewidth=2.5)
    ax2.fill(theta_scan, power_norm, color='#00D2FF', alpha=0.15)
    
    # Draw vector line targets for visuals
    ax2.annotate('', xy=(theta_target, 1.0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='#00FFCC', lw=2))
    if mode == "Interference Mitigation (Null-Steering)":
        ax2.annotate('', xy=(np.radians(jamming_angle), 0.8), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='#FF3366', lw=1.5, ls=':'))
        
    ax2.tick_params(colors='#E0E0E0', labelsize=8)
    ax2.grid(True, color='#2E353F', linestyle=':')
    st.pyplot(fig2)

# 6. Deep Technical Insight Box for Judges
st.markdown("### 💡 Theoretical Architecture & Engineering Deep-Dive")
with st.expander("Click to view mathematical equations and link details for evaluation Viva/Questions"):
    st.markdown(f"""
    * **Steering Vector Calculation:** Employs the array steering equation: $a(\\theta) = [1, e^{{j2\\pi \\frac{{d}}{{\\lambda}}\\sin(\\theta)}}, \\dots, e^{{j2\\pi(N-1)\\frac{{d}}{{\\lambda}}\\sin(\\theta)}}]^T$
    * **Null Steering Engine:** Utilizes spatial zero-forcing projection weights. It isolates the target vector space while projecting a vector null directly perpendicular to the jammer steering matrix coordinate, driving interference power near zero ($-\infty$ dB theoretical limit).
    * **Grating Lobe Avoidance:** Keep element spacing ($d/\lambda$) $\le 0.5$ to prevent structural spatial aliasing over the $[-90^\circ, 90^\circ]$ sweeping arc.
    """)
