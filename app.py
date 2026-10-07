import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="5G MIMO Beamforming Simulator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# THEME / RESPONSIVE CSS
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 25% 5%, rgba(0,115,220,.09), transparent 32%),
            radial-gradient(circle at 85% 70%, rgba(0,85,180,.07), transparent 35%),
            #06111f;
        color:#e8f1ff;
    }

    .main .block-container {
        max-width:1450px;
        padding:1rem 1rem 2rem 1rem;
    }

    section[data-testid="stSidebar"] {
        background:linear-gradient(180deg,#081727 0%,#06121f 58%,#071322 100%);
        border-right:1px solid rgba(70,150,220,.16);
    }
    section[data-testid="stSidebar"] > div { padding-top:.8rem; }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color:#24a9ff; }
    section[data-testid="stSidebar"] label { color:#d8e8f8 !important; line-height:1.25 !important; white-space:normal !important; }
    section[data-testid="stSidebar"] [data-testid="stSlider"] { padding-top:.08rem; }

    .dashboard-title {
        font-size:2.05rem; font-weight:800; color:#f4f8ff;
        letter-spacing:-.5px; margin-bottom:.12rem;
    }
    .dashboard-subtitle { color:#9fb4c8; font-size:.93rem; margin-bottom:.7rem; }

    .metric-grid {
        display:grid; grid-template-columns:repeat(4,1fr); gap:12px;
        margin:.7rem 0 .8rem 0;
    }
    .metric-card {
        min-height:116px; padding:13px 15px 9px 15px;
        border:1px solid rgba(82,145,190,.22); border-radius:12px;
        background:linear-gradient(145deg,rgba(12,31,50,.96),rgba(7,22,37,.96));
        box-shadow:inset 0 1px 0 rgba(255,255,255,.025),0 10px 30px rgba(0,0,0,.12);
    }
    .metric-label { font-size:.82rem; color:#73d6a3; margin-bottom:3px; }
    .metric-value { font-size:1.65rem; line-height:1.1; font-weight:700; color:#f3f8ff; margin-bottom:4px; }
    .metric-help { color:#6f879c; font-size:.68rem; margin-top:-1px; }
    .metric-spark { width:100%; height:30px; display:block; }
    .metric-spark-grid { stroke:rgba(100,150,190,.12); stroke-width:1; }
    .metric-spark-line { fill:none; stroke-width:2.1; stroke-linecap:round; stroke-linejoin:round; }

    .section-heading { font-size:1.04rem; font-weight:700; color:#f0f6ff; margin-top:.25rem; margin-bottom:.18rem; }
    .section-subheading { color:#8da5bd; font-size:.8rem; margin-bottom:.3rem; }

    .info-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px; }
    .info-card {
        background:linear-gradient(145deg,rgba(10,27,44,.96),rgba(6,19,33,.96));
        border:1px solid rgba(70,140,190,.22); border-radius:11px;
        padding:16px 18px; min-height:170px;
    }
    .info-title { color:#31a9ff; font-size:.95rem; font-weight:700; margin-bottom:8px; }
    .info-text { color:#c7d5e4; line-height:1.55; font-size:.82rem; }

    .mini-note {
        border:1px solid rgba(45,169,255,.14); background:rgba(5,24,41,.65);
        border-radius:9px; padding:8px 10px; color:#9fb4c8; font-size:.76rem; margin:.35rem 0 .5rem;
    }
    .footer { text-align:center; color:#70869b; font-size:.76rem; padding:12px 0 10px; }

    div[data-testid="stDataFrame"] { border:1px solid rgba(80,145,190,.20); border-radius:10px; overflow:hidden; }

    @media (max-width:1000px) {
        .metric-grid { grid-template-columns:repeat(2,1fr); }
        .info-grid { grid-template-columns:1fr; }
        .dashboard-title { font-size:1.7rem; }
    }
    @media (max-width:600px) {
        .main .block-container { padding:.65rem .45rem 1.25rem .45rem; }
        .metric-grid { grid-template-columns:1fr 1fr; gap:7px; }
        .metric-card { min-height:102px; padding:10px 10px 7px; }
        .metric-value { font-size:1.18rem; }
        .metric-label { font-size:.72rem; }
        .metric-help { font-size:.59rem; }
        .dashboard-title { font-size:1.4rem; }
        .dashboard-subtitle { font-size:.72rem; line-height:1.35; }
        .section-heading { font-size:.93rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================
def clamp(value, low, high):
    return max(low, min(high, value))


def sparkline(values):
    values = np.asarray(values, dtype=float)
    if len(values) < 2:
        values = np.array([0.0, 1.0])
    vmin, vmax = np.min(values), np.max(values)
    normalized = np.ones_like(values) * 0.5 if abs(vmax - vmin) < 1e-12 else (values - vmin) / (vmax - vmin)
    return " ".join(
        f"{2 + (i/(len(normalized)-1))*96:.2f},{31-value*25:.2f}"
        for i, value in enumerate(normalized)
    )


def build_metric_card(label, value, values, line_color, help_text):
    points = sparkline(values)
    return f"""<div class="metric-card" title="{help_text}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <svg class="metric-spark" viewBox="0 0 100 36" preserveAspectRatio="none">
            <line class="metric-spark-grid" x1="0" y1="30" x2="100" y2="30" />
            <polyline class="metric-spark-line" points="{points}" stroke="{line_color}" />
        </svg>
        <div class="metric-help">Hover for meaning</div>
    </div>"""


def steering_vector(theta, num_elements, spacing):
    n = np.arange(num_elements)
    return np.exp(1j * 2 * np.pi * spacing * n * np.sin(theta))


def calculate_array_factor(angles_rad, weights, num_elements, spacing):
    n = np.arange(num_elements)
    return np.sum(
        weights[:, None]
        * np.exp(1j * 2 * np.pi * spacing * n[:, None] * np.sin(angles_rad)[None, :]),
        axis=0,
    )


def calculate_fspl(distance, frequency_hz):
    distance = max(float(distance), 1.0)
    c = 3e8
    return 20*np.log10(distance) + 20*np.log10(frequency_hz) - 20*np.log10(c)


def calculate_reflection_point(bs, ue, requested_path, index):
    """Create a reflection point whose two-segment 3D distance is close to the requested path."""
    bs = np.asarray(bs, dtype=float)
    ue = np.asarray(ue, dtype=float)
    direct = np.linalg.norm(ue-bs)
    target = max(float(requested_path), direct + 0.05)
    midpoint = (bs + ue) / 2.0
    direction = ue - bs
    dxy = np.array([direction[0], direction[1], 0.0])
    dxy_norm = np.linalg.norm(dxy)
    if dxy_norm < 1e-9:
        perp = np.array([1.0, 0.0, 0.0])
    else:
        unit = dxy / dxy_norm
        perp = np.array([-unit[1], unit[0], 0.0])

    # Solve for an offset along a perpendicular direction and a modest elevation.
    height = 4.0 + 3.0*(index % 3)
    base = midpoint + np.array([0.0, 0.0, height])
    base_total = np.linalg.norm(base-bs) + np.linalg.norm(ue-base)
    needed = max(0.0, target-base_total)

    # Offset increases total path length monotonically for the usual geometry.
    lo, hi = 0.0, max(10.0, target*1.5)
    sign = 1 if index % 2 == 0 else -1
    for _ in range(45):
        off = (lo+hi)/2
        point = base + sign*perp*off
        total = np.linalg.norm(point-bs) + np.linalg.norm(ue-point)
        if total < target:
            lo = off
        else:
            hi = off
    point = base + sign*perp*((lo+hi)/2)
    return tuple(point.tolist())


def add_base_station_tower(fig, x=0, y=0, height=15):
    tower_color = "#9aa9b8"
    antenna_color = "#2da9ff"
    base_width = height*0.16

    fig.add_trace(go.Scatter3d(x=[x-base_width,x+base_width], y=[y,y], z=[0,height], mode="lines",
        line=dict(color=tower_color,width=5), showlegend=False, hovertemplate="Tower structure<extra></extra>"))
    levels = np.linspace(2,height-1.5,6)
    for level in levels:
        width = base_width*(1-0.65*level/height)
        fig.add_trace(go.Scatter3d(x=[x-width,x+width],y=[y,y],z=[level,level],mode="lines",
            line=dict(color=tower_color,width=3),showlegend=False,hovertemplate="Tower cross member<extra></extra>"))
    for z1,z2 in zip(levels[:-1],levels[1:]):
        w1 = base_width*(1-0.65*z1/height); w2 = base_width*(1-0.65*z2/height)
        for xa,xb in [(-w1,+w2),(+w1,-w2)]:
            fig.add_trace(go.Scatter3d(x=[x+xa,x+xb],y=[y,y],z=[z1,z2],mode="lines",
                line=dict(color=tower_color,width=2),showlegend=False,hovertemplate="Tower support<extra></extra>"))
    fig.add_trace(go.Scatter3d(x=[x,x],y=[y,y],z=[height,height+2.5],mode="lines",
        line=dict(color=antenna_color,width=4),showlegend=False,hovertemplate="Antenna mast<extra></extra>"))
    for offset in [-0.5,0,0.5]:
        fig.add_trace(go.Scatter3d(x=[x+offset,x+offset],y=[y-.35,y+.35],z=[height+1,height+1],mode="lines",
            line=dict(color=antenna_color,width=5),showlegend=False,hovertemplate="5G antenna panel<extra></extra>"))
    fig.add_trace(go.Scatter3d(x=[x],y=[y],z=[height+4],mode="text",text=["5G BS"],
        textfont=dict(color="#21a7ff",size=16),showlegend=False,hoverinfo="skip"))


def unit_vector_from_angles(az_deg, el_deg=0):
    az, el = np.radians([az_deg, el_deg])
    return np.array([np.cos(el)*np.cos(az), np.cos(el)*np.sin(az), np.sin(el)])


def make_beam_surface(target_angle, num_elements, spacing, weights, tx_power_dbm, display_radius=16.0):
    """Create a bounded 3D beam whose visual size follows transmit power.

    The RF pattern is normalized independently of transmit power, while the
    displayed radius is scaled by transmit power so lowering TX power makes
    the beam visibly smaller. The display is deliberately bounded so changing
    the physical UE distance never pushes the UE/beam outside this graph.
    """
    az = np.linspace(-180, 180, 241)
    el = np.linspace(-70, 70, 101)
    AZ, EL = np.meshgrid(az, el)

    global_af = calculate_array_factor(
        np.radians(AZ).ravel(), weights, num_elements, spacing
    ).reshape(AZ.shape)
    horiz = np.abs(global_af) ** 2
    horiz /= max(np.max(horiz), 1e-12)

    # Use the actual global array factor. The steering weights already contain
    # the UE direction, so do not rotate the pattern a second time. A gentle
    # front preference removes the ULA front/back ambiguity without erasing
    # the real side lobes.
    rel_az = np.radians(((AZ - target_angle + 180) % 360) - 180)
    front_factor = 0.05 + 0.95 * ((1.0 + np.cos(rel_az)) / 2.0) ** 2.0
    horiz *= front_factor

    vert = np.cos(np.radians(EL)) ** 4
    vert = np.maximum(vert, 0.0)
    pattern = horiz * vert
    pattern /= max(np.max(pattern), 1e-12)

    # Keep real low-level side lobes visible. This floor is only a visual
    # readability aid; it does not alter the RF calculations used for SINR.
    # Visual-only floor: make genuine low-level side lobes visible without changing
    # the RF array-factor values used by the link-budget calculations.
    pattern = np.maximum(pattern, 0.045)

    # Medium-large visual response to TX power. This is intentionally a
    # display scale rather than a physical meter conversion so the beam stays
    # readable while still responding to transmit power.
    power_fraction = np.clip((float(tx_power_dbm) - 10.0) / 33.0, 0.0, 1.0)
    power_scale = 0.95 + 0.50 * power_fraction

    forward = np.clip(np.cos(rel_az), 0, 1) ** 1.15
    # Give the complete radiation surface enough radius to make both the main
    # lobe and the real side lobes clearly visible at normal power settings.
    # Medium display size at normal power, with a larger envelope so the main
    # lobe and side lobes are easy to inspect. This affects only visualization.
    radius = 1.10 + power_scale * (2.10 + 15.0 * pattern)

    AZr, ELr = np.radians(AZ), np.radians(EL)
    X = radius * np.cos(ELr) * np.cos(AZr)
    Y = radius * np.cos(ELr) * np.sin(AZr)
    Z = radius * np.sin(ELr)

    # Stretch toward the selected UE direction. The stretch is moderate so the
    # main beam remains medium-sized and the side lobes remain distinguishable.
    stretch = 1.0 + power_scale * (1.05 * forward + 0.70 * pattern * forward)
    target_rad = np.radians(target_angle)
    ux, uy = np.cos(target_rad), np.sin(target_rad)
    along = X * ux + Y * uy
    perp_x = X - along * ux
    perp_y = Y - along * uy
    X = perp_x + (along * stretch) * ux
    Y = perp_y + (along * stretch) * uy

    current_max = max(float(np.max(np.sqrt(X**2 + Y**2 + Z**2))), 1e-9)
    envelope = float(display_radius)
    if current_max > envelope:
        envelope_scale = envelope / current_max
        X *= envelope_scale
        Y *= envelope_scale
        Z *= envelope_scale

    return X, Y, Z, pattern, AZ, EL

# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <div class="dashboard-title">5G MIMO Beamforming Simulator</div>
    <div class="dashboard-subtitle">Beam Steering | Null Steering | Multipath Propagation | 2D Radiation Pattern | Polar Pattern | 3D Spatial Beam</div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR CONTROLS
# ============================================================
st.sidebar.markdown("## 5G RF Configuration")
mode = st.sidebar.selectbox("Operating Mode", ["Single User Beam Steering", "Interference Mitigation (Null Steering)"], index=0)
num_elements = st.sidebar.slider("Antenna Elements", 4, 32, 16, 4)
element_spacing = st.sidebar.slider(
    "Antenna Spacing (reference wavelength)", 0.25, 1.00, 0.50, 0.05,
    help="Physical spacing is set as a fraction of the 3.5 GHz reference wavelength. Changing carrier frequency therefore changes spacing in current wavelengths and beam width.",
)

st.sidebar.markdown("### User Equipment")
target_angle = st.sidebar.slider("UE Direction (degrees)", -80, 80, 25, 1)

jamming_angle = 0
if mode == "Interference Mitigation (Null Steering)":
    jamming_angle = st.sidebar.slider("Interference Direction (degrees)", -80, 80, -35, 1)

st.sidebar.markdown("### RF Parameters")
frequency_ghz = st.sidebar.slider("Carrier Frequency (GHz)", 1.0, 40.0, 3.5, 0.5,
    help="Practical sub-6 GHz to mmWave range used for this educational 5G model.")
tx_power_dbm = st.sidebar.slider("Transmit Power (dBm)", 10.0, 43.0, 30.0, 1.0,
    help="Practical base-station transmit-power range for the simplified link-budget model.")
noise_power_dbm = st.sidebar.slider("Noise Power (dBm)", -100.0, -70.0, -90.0, 1.0,
    help="Effective receiver noise range used to avoid unrealistically low noise floors.")

st.sidebar.markdown("### UE Distance")
default_distance = st.sidebar.slider("UE Distance (m)", 20.0, 1000.0, 100.0, 5.0,
    help="Practical cell-distance range for this educational 5G model.")

st.sidebar.markdown("### Multipath")
path_count = st.sidebar.slider("Number of Paths", 1, 5, 3, 1)
# A reflected path cannot physically be shorter than the direct BS-to-UE route.
# The BS is modeled at 15 m and the UE at 1.5 m, so use the actual 3D direct
# distance as the minimum allowed propagation distance.
minimum_path_distance = float(np.sqrt(default_distance**2 + (15.0 - 1.5)**2))
path_distances = []
for i in range(path_count):
    requested_default = max(minimum_path_distance + i*25.0, minimum_path_distance)
    distance = st.sidebar.number_input(
        f"Path {i+1} Distance (m)", min_value=minimum_path_distance, max_value=10000.0,
        value=float(requested_default), step=5.0, key=f"path_distance_{i}",
        help="A reflected route must be at least as long as the direct BS-to-UE distance. The minimum updates automatically when UE Distance changes.",
    )
    path_distances.append(max(float(distance), minimum_path_distance))

# ============================================================
# PHYSICAL / ARRAY CALCULATIONS
# ============================================================
c = 3e8
frequency_hz = frequency_ghz*1e9
wavelength = c/frequency_hz
# Keep the physical antenna spacing fixed. The sidebar value is referenced to
# the 3.5 GHz wavelength, so changing carrier frequency changes spacing in
# current wavelengths and therefore changes beam width.
reference_frequency_hz = 3.5e9
reference_wavelength = c/reference_frequency_hz
element_spacing_m = element_spacing*reference_wavelength
effective_spacing = element_spacing_m/wavelength

angles_deg = np.linspace(-90,90,1201)
angles_rad = np.radians(angles_deg)
theta_target = np.radians(target_angle)

# IMPORTANT: conjugate steering vector for transmit beamforming so the peak is at +target_angle.
v_target = steering_vector(theta_target, num_elements, effective_spacing)
if mode == "Single User Beam Steering":
    weights = np.conj(v_target)/np.sqrt(num_elements)
else:
    theta_jammer = np.radians(jamming_angle)
    v_jammer = steering_vector(theta_jammer, num_elements, effective_spacing)
    # Orthogonal projection removes the jammer direction from the transmit weight vector.
    projection = np.vdot(v_jammer, np.conj(v_target)) / (np.vdot(v_jammer,v_jammer)+1e-12)
    weights = np.conj(v_target) - projection*np.conj(v_jammer)
    weights /= max(np.linalg.norm(weights),1e-12)

array_factor = calculate_array_factor(angles_rad, weights, num_elements, effective_spacing)
power = np.abs(array_factor)**2
power_norm = power/max(np.max(power),1e-12)
power_db = 10*np.log10(np.maximum(power_norm,1e-8))
target_index = np.argmin(np.abs(angles_deg-target_angle))
power_at_ue = float(power_norm[target_index])

if mode == "Interference Mitigation (Null Steering)":
    jammer_index = np.argmin(np.abs(angles_deg-jamming_angle))
    power_at_jammer = float(power_norm[jammer_index])
else:
    power_at_jammer = 0.0

# Link budget and SINR model.
# Keep the array gain and the directional beam response separate so that
# antenna count, null steering, spacing and operating mode can affect the link.
array_gain_db = 10*np.log10(num_elements)
fspl_direct = calculate_fspl(default_distance, frequency_hz)
beam_gain_db = 10*np.log10(max(power_at_ue,1e-8))
received_signal_dbm = tx_power_dbm + array_gain_db + beam_gain_db - fspl_direct

# Realistic co-channel interference model. A residual receiver/inter-cell
# interference floor prevents an ideal free-space simulation from producing
# implausibly huge SINR values without imposing an artificial SINR maximum.
# The floor is part of the interference model, not a display clamp.
RESIDUAL_INTERFERENCE_POWER = 1e-3  # -30 dB normalized spatial leakage floor
if mode == "Interference Mitigation (Null Steering)":
    interferer_tx_power_dbm = tx_power_dbm - 3.0
    effective_interference_response = max(power_at_jammer, RESIDUAL_INTERFERENCE_POWER)
    interference_dbm = (
        interferer_tx_power_dbm
        + array_gain_db
        + 10*np.log10(effective_interference_response)
        - fspl_direct
    )
else:
    background_interference_angle = float(clamp(target_angle + 35.0, -80.0, 80.0))
    bg_index = np.argmin(np.abs(angles_deg-background_interference_angle))
    background_response = float(power_norm[bg_index])
    interferer_tx_power_dbm = tx_power_dbm - 6.0
    effective_interference_response = max(background_response, RESIDUAL_INTERFERENCE_POWER)
    interference_dbm = (
        interferer_tx_power_dbm
        + array_gain_db
        + 10*np.log10(effective_interference_response)
        - fspl_direct
    )

signal_mw = 10**(received_signal_dbm/10)
noise_mw = 10**(noise_power_dbm/10)
interference_mw = 10**(interference_dbm/10)
sinr_linear = signal_mw/max(noise_mw+interference_mw,1e-30)
sinr_db = float(10*np.log10(max(sinr_linear,1e-12)))
spectral_efficiency = np.log2(1+sinr_linear)

# ============================================================
# MULTIPATH CALCULATIONS
# ============================================================
multipath_results = []
for i,distance in enumerate(path_distances):
    # Never allow a reflected route to be shorter than the direct geometric route.
    effective_distance = max(float(distance), minimum_path_distance)
    loss = calculate_fspl(effective_distance, frequency_hz)
    relative_power = (minimum_path_distance/max(effective_distance,1e-9))**2
    multipath_results.append({"path":f"Path {i+1}","distance":effective_distance,"path_loss":loss,"relative_power":relative_power})

# ============================================================
# METRICS
# ============================================================
sample_x = np.linspace(0,2*np.pi,50)
gain_samples = array_gain_db + 0.35*np.sin(sample_x*1.8)
sinr_samples = sinr_db + 0.5*np.sin(sample_x*3.0)
spectral_samples = spectral_efficiency + 0.25*np.sin(sample_x*2.5)
distance_samples = default_distance + 4*np.sin(sample_x*2.3)

metric_cards = [
    build_metric_card("Antenna Gain", f"{array_gain_db:.1f} dB", gain_samples, "#27c968", "Array gain is approximately 10*log10(N) dB for N equal-power antenna elements."),
    build_metric_card("SINR", f"{sinr_db:.2f} dB", sinr_samples, "#168cff", "Signal-to-interference-plus-noise ratio at the UE. Higher SINR generally supports higher spectral efficiency."),
    build_metric_card("Spectral Efficiency", f"{spectral_efficiency:.2f} bps/Hz", spectral_samples, "#a34dff", "Estimated Shannon-style spectral efficiency: log2(1 + SINR)."),
    build_metric_card("UE Distance", f"{default_distance:.1f} m", distance_samples, "#f0b52b", "Distance between the 5G base station and the User Equipment used by the link-budget and multipath model."),
]
st.markdown(f"<div class=\"metric-grid\">{''.join(metric_cards)}</div>", unsafe_allow_html=True)

st.markdown(
    f'<div class="mini-note"><b>Live model:</b> {num_elements} antenna elements at {frequency_ghz:.1f} GHz, physical spacing {element_spacing_m*1000:.1f} mm ({effective_spacing:.2f} current wavelengths). The yellow UE marker shows the selected steering direction in every visualization.</div>',
    unsafe_allow_html=True,
)

# ============================================================
# 2D + POLAR
# ============================================================
col1, col2 = st.columns(2, gap="small")

with col1:
    st.markdown('<div class="section-heading">2D Beamforming Pattern</div>', unsafe_allow_html=True)
    fig_2d = go.Figure()
    fig_2d.add_trace(go.Scatter(x=angles_deg,y=power_db,mode="lines",line=dict(color="#008cff",width=3),
        fill="tozeroy",fillcolor="rgba(0,140,255,.10)",name="5G Beam",
        hovertemplate="Angle: %{x:.1f} deg<br>Normalized Power: %{y:.2f} dB<extra>Beam response</extra>"))
    fig_2d.add_trace(go.Scatter(x=[target_angle,target_angle],y=[-40,2],mode="lines",
        line=dict(color="#f4c21f",width=2,dash="dash"),name=f"UE = {target_angle} deg",
        hovertemplate=f"UE direction = {target_angle} deg<br>The array weights are phased to maximize power here.<extra></extra>"))
    ue_marker_y = float(min(power_db[target_index], 0.4))
    fig_2d.add_trace(go.Scatter(x=[target_angle],y=[ue_marker_y],mode="markers+text",
        marker=dict(size=8,color="#f4c21f"),text=[f"UE = {target_angle} deg"],textposition="bottom center",
        textfont=dict(color="#f4c21f",size=11),cliponaxis=False,showlegend=False,
        hovertemplate=f"<b>UE direction</b><br>{target_angle} deg<br>Normalized response: {power_at_ue:.3f}<extra></extra>"))
    if mode == "Interference Mitigation (Null Steering)":
        fig_2d.add_trace(go.Scatter(x=[jamming_angle,jamming_angle],y=[-40,2],mode="lines",
            line=dict(color="#ff4b5c",width=2,dash="dot"),name=f"Interference = {jamming_angle} deg",
            hovertemplate=f"Interference direction = {jamming_angle} deg<br>Null steering suppresses the array response here.<extra></extra>"))
    fig_2d.update_layout(height=370,margin=dict(l=50,r=15,t=10,b=45),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(4,17,29,.45)",
        xaxis=dict(title="Angle (degrees)",range=[-90,90],color="#d5e4f2",gridcolor="rgba(80,140,190,.14)"),
        yaxis=dict(title="Normalized Power (dB)",range=[-40,4],color="#d5e4f2",gridcolor="rgba(80,140,190,.14)"),
        legend=dict(orientation="h",yanchor="bottom",y=-.27,xanchor="left",x=0,font=dict(color="#c7d7e7",size=10)),
        font=dict(color="#d5e4f2"),hovermode="x unified")
    st.plotly_chart(fig_2d,width="stretch",config={"displayModeBar":False,"responsive":True})

with col2:
    st.markdown('<div class="section-heading">Polar Radiation Pattern</div>', unsafe_allow_html=True)
    polar_deg = np.linspace(0,360,1441)
    polar_rad = np.radians(polar_deg)
    # The transmit weights already steer the beam toward target_angle.
    # Evaluate the array at the actual global polar angle. Do not rotate the
    # response a second time, otherwise the beam and UE marker can be misaligned.
    polar_af = calculate_array_factor(polar_rad, weights, num_elements, effective_spacing)
    polar_power = np.abs(polar_af)**2
    polar_norm = polar_power/max(np.max(polar_power),1e-12)
    target_polar_index = np.argmin(np.abs(polar_deg-(target_angle%360)))
    ue_polar_radius = float(np.clip(polar_norm[target_polar_index], 0.08, 1.0))
    fig_polar = go.Figure()
    fig_polar.add_trace(go.Scatterpolar(theta=polar_deg,r=polar_norm,mode="lines",line=dict(color="#008cff",width=2.7),
        fill="toself",fillcolor="rgba(0,140,255,.08)",name="5G Beam",
        hovertemplate="Angle: %{theta:.1f} deg<br>Normalized Power: %{r:.3f}<extra>Radiation pattern</extra>"))
    fig_polar.add_trace(go.Scatterpolar(theta=[target_angle%360],r=[ue_polar_radius],mode="markers+text",
        marker=dict(size=9,color="#f4c21f"),text=["UE"],textposition="middle right",textfont=dict(color="#f4c21f",size=12),name="UE",
        hovertemplate=f"UE direction: {target_angle:.1f} deg<br>Response: {polar_norm[target_polar_index]:.3f}<extra></extra>"))
    if mode == "Interference Mitigation (Null Steering)":
        ji = np.argmin(np.abs(polar_deg-(jamming_angle%360)))
        fig_polar.add_trace(go.Scatterpolar(theta=[jamming_angle%360],r=[polar_norm[ji]],mode="markers+text",
            marker=dict(size=8,color="#ff4b5c"),text=["Interference"],textposition="middle left",textfont=dict(color="#ff6978",size=10),name="Interference",
            hovertemplate=f"Interference direction: {jamming_angle:.1f} deg<br>Residual response: {polar_norm[ji]:.5f}<extra></extra>"))
    fig_polar.update_layout(height=370,margin=dict(l=25,r=25,t=10,b=20),paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(bgcolor="rgba(4,17,29,.45)",radialaxis=dict(range=[0,1.05],color="#d5e4f2",gridcolor="rgba(80,140,190,.20)",tickvals=[.25,.5,.75,1]),
                   angularaxis=dict(direction="counterclockwise",rotation=0,color="#d5e4f2",gridcolor="rgba(80,140,190,.20)")),
        legend=dict(orientation="h",yanchor="bottom",y=-.10,xanchor="left",x=0,font=dict(color="#c7d7e7",size=10)),font=dict(color="#d5e4f2"))
    st.plotly_chart(fig_polar,width="stretch",config={"displayModeBar":False,"responsive":True})

# ============================================================
# 3D REALISTIC BEAM
# ============================================================
st.markdown('<div class="section-heading">3D Radiation Pattern (Realistic 5G Beam)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subheading">The beam is physically oriented from the base station toward the selected UE direction. Hover the surface to inspect azimuth, elevation and normalized beam strength.</div>', unsafe_allow_html=True)

X_3d,Y_3d,Z_3d,beam_3d,AZ_3d,EL_3d = make_beam_surface(target_angle,num_elements,effective_spacing,weights,tx_power_dbm,display_radius=16.0)
fig_3d = go.Figure()
fig_3d.add_trace(go.Surface(
    x=X_3d,y=Y_3d,z=Z_3d,surfacecolor=beam_3d,
    colorscale=[[0.00,"#071c36"],[.12,"#064b9b"],[.30,"#087ed0"],[.48,"#13b9d5"],[.63,"#36cf65"],[.77,"#b8df25"],[.89,"#ffd21f"],[1,"#ff3a1f"]],
    cmin=0,cmax=1,opacity=.94,showscale=True,
    colorbar=dict(title=dict(text="Beam Strength (Normalized)",font=dict(color="#e5eef8",size=11)),orientation="h",thickness=12,len=.43,x=.50,xanchor="center",y=-.07,tickfont=dict(color="#d5e4f2",size=9)),
    lighting=dict(ambient=.48,diffuse=.78,specular=.55,roughness=.30,fresnel=.20),lightposition=dict(x=100,y=100,z=150),
    name="5G Radiation Beam",
    hoverlabel=dict(bgcolor="#081a2d",font=dict(color="#ffffff",size=11)),
    customdata=np.stack([AZ_3d, EL_3d, beam_3d], axis=-1),
    hovertemplate=(
        "<b>5G Radiation Beam</b><br>"
        "Azimuth: %{customdata[0]:.1f} deg<br>"
        "Elevation: %{customdata[1]:.1f} deg<br>"
        "Beam Strength: %{customdata[2]:.3f}"
        "<extra></extra>"
    ),
))

# BS point and antenna elements at origin.
fig_3d.add_trace(go.Scatter3d(x=[0],y=[0],z=[0],mode="markers+text",marker=dict(size=6,color="#f2f6fb"),text=["5G BS"],textposition="middle left",
    textfont=dict(color="#fff",size=11),name="5G BS",hovertemplate="<b>5G Base Station</b><br>Transmit array origin<extra></extra>"))
antenna_z=np.linspace(-2.3,2.3,num_elements)
fig_3d.add_trace(go.Scatter3d(x=np.zeros(num_elements),y=np.zeros(num_elements),z=antenna_z,mode="markers",marker=dict(size=3,color="#fff"),name="Antenna Elements",
    hovertemplate="Antenna element %{pointNumber}<extra></extra>"))

ue_radius=17.0
ue_dir=unit_vector_from_angles(target_angle)
ue_x,ue_y,ue_z=(ue_dir*ue_radius).tolist()
fig_3d.add_trace(go.Scatter3d(x=[0,ue_x],y=[0,ue_y],z=[0,ue_z],mode="lines",line=dict(color="#ffd21f",width=3,dash="dash"),name="Beam Direction",
    hovertemplate=f"Beam steered to UE at {target_angle} deg<extra></extra>"))
fig_3d.add_trace(go.Scatter3d(x=[ue_x],y=[ue_y],z=[ue_z],mode="markers+text",marker=dict(size=9,color="#39d06e",line=dict(color="#d8ffe6",width=1.5)),
    text=[f"UE ({target_angle} deg)"],textposition="middle right",textfont=dict(color="#61ee91",size=12),name="UE",
    hovertemplate=f"<b>UE</b><br>Direction: {target_angle:.1f} deg<br>Configured distance: {default_distance:.1f} m<extra></extra>"))

if mode == "Interference Mitigation (Null Steering)":
    jammer_radius=32
    jammer_dir=unit_vector_from_angles(jamming_angle)
    jx,jy,jz=(jammer_dir*jammer_radius).tolist()
    fig_3d.add_trace(go.Scatter3d(x=[jx],y=[jy],z=[jz],mode="markers+text",marker=dict(size=8,color="#ff3d54",symbol="x"),text=["Interference"],textposition="top center",
        textfont=dict(color="#ff6172",size=10),name="Interference",hovertemplate=f"Interference direction: {jamming_angle} deg<extra></extra>"))
    fig_3d.add_trace(go.Scatter3d(x=[0,jx],y=[0,jy],z=[0,jz],mode="lines",line=dict(color="#ff3d54",width=2,dash="dot"),name="Null Direction",hovertemplate="Null-steering direction<extra></extra>"))

fig_3d.update_layout(height=585,margin=dict(l=0,r=0,t=0,b=55),paper_bgcolor="rgba(0,0,0,0)",showlegend=True,
    legend=dict(x=.77,y=.96,font=dict(color="#dbe8f5",size=10),bgcolor="rgba(4,15,27,.55)",bordercolor="rgba(90,150,190,.12)",borderwidth=1),
    scene=dict(bgcolor="rgba(3,13,24,.55)",xaxis=dict(title="X",range=[-20,20],color="#9fb4c8",gridcolor="rgba(80,130,170,.14)",showbackground=False),
               yaxis=dict(title="Y",range=[-20,20],color="#9fb4c8",gridcolor="rgba(80,130,170,.14)",showbackground=False),
               zaxis=dict(title="Z",range=[-20,20],color="#9fb4c8",gridcolor="rgba(80,130,170,.14)",showbackground=False),
               camera=dict(eye=dict(x=1.45,y=1.45,z=.95)),aspectmode="manual",aspectratio=dict(x=1.25,y=1.25,z=.85)))
st.plotly_chart(fig_3d,width="stretch",config={"displayModeBar":False,"responsive":True})

# ============================================================
# MULTIPATH 3D
# ============================================================
st.markdown('<div class="section-heading">Multipath Propagation (3D)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subheading">Direct line-of-sight plus configurable reflected paths. Hover a path or reflection point to see the configured distance, FSPL and relative power.</div>', unsafe_allow_html=True)

bs_phys=np.array([0.0,0.0,15.0])
ue_phys=np.array([default_distance*np.cos(np.radians(target_angle)),default_distance*np.sin(np.radians(target_angle)),1.5])
direct_distance=float(np.linalg.norm(ue_phys-bs_phys))

fig_paths=go.Figure()
add_base_station_tower(fig_paths,x=0,y=0,height=15)
fig_paths.add_trace(go.Scatter3d(x=[0],y=[0],z=[15],mode="markers",marker=dict(size=5,color="#23a7ff"),name="5G BS",
    hovertemplate="<b>5G Base Station</b><br>Height: 15 m<extra></extra>"))
fig_paths.add_trace(go.Scatter3d(x=[ue_phys[0]],y=[ue_phys[1]],z=[ue_phys[2]],mode="markers+text",marker=dict(size=11,color="#32d36b",line=dict(color="#d9ffe5",width=1.5)),
    text=["UE"],textposition="middle right",textfont=dict(color="#56ee8a",size=14),name="UE",
    hovertemplate=f"<b>User Equipment</b><br>Direction: {target_angle:.1f} deg<br>Horizontal distance: {default_distance:.1f} m<extra></extra>"))
fig_paths.add_trace(go.Scatter3d(x=[bs_phys[0],ue_phys[0]],y=[bs_phys[1],ue_phys[1]],z=[bs_phys[2],ue_phys[2]],mode="lines",
    line=dict(color="#1ed760",width=5),name="Direct LOS Path",hovertemplate=f"<b>Direct LOS Path</b><br>Geometric distance: {direct_distance:.2f} m<extra></extra>"))

reflection_colors=["#ff9f1c","#ff4b42","#a36bff","#00c8ff","#ffd21f"]
reflection_points=[]
for i,path in enumerate(multipath_results):
    point=np.array(calculate_reflection_point(bs_phys,ue_phys,path["distance"],i))
    reflection_points.append(point)
    color=reflection_colors[i%len(reflection_colors)]
    fig_paths.add_trace(go.Scatter3d(x=[bs_phys[0],point[0]],y=[bs_phys[1],point[1]],z=[bs_phys[2],point[2]],mode="lines",
        line=dict(color=color,width=4),showlegend=False,hoverinfo="skip"))
    fig_paths.add_trace(go.Scatter3d(x=[point[0],ue_phys[0]],y=[point[1],ue_phys[1]],z=[point[2],ue_phys[2]],mode="lines",
        line=dict(color=color,width=4,dash="dash"),name=path["path"],
        hovertemplate=f"<b>{path['path']}</b><br>Configured path distance: {path['distance']:.2f} m<br>Path loss: {path['path_loss']:.2f} dB<br>Relative power: {path['relative_power']:.6f}<extra></extra>"))
    fig_paths.add_trace(go.Scatter3d(x=[point[0]],y=[point[1]],z=[point[2]],mode="markers",marker=dict(size=8,color=color),showlegend=False,
        hovertemplate=f"<b>Reflection Point {i+1}</b><br>Approx. route length: {path['distance']:.2f} m<extra></extra>"))

range_limit=max(default_distance*1.20,max(path_distances)*1.10,130)
ground_x=np.linspace(-range_limit*.15,range_limit,18); ground_y=np.linspace(-range_limit*.55,range_limit*.55,18); GX,GY=np.meshgrid(ground_x,ground_y); GZ=np.zeros_like(GX)
fig_paths.add_trace(go.Surface(x=GX,y=GY,z=GZ,showscale=False,opacity=.10,colorscale=[[0,"#102d45"],[1,"#102d45"]],hoverinfo="skip"))

zmax=max(24,max([15]+[float(p[2]) for p in reflection_points]+[ue_phys[2]])+5)
fig_paths.update_layout(height=585,margin=dict(l=0,r=0,b=0,t=0),paper_bgcolor="rgba(0,0,0,0)",showlegend=True,
    legend=dict(x=.76,y=.97,font=dict(color="#dce9f5",size=10),bgcolor="rgba(4,15,27,.55)",bordercolor="rgba(90,150,190,.12)",borderwidth=1),
    scene=dict(bgcolor="rgba(3,13,24,.55)",xaxis=dict(title="X (m)",range=[-range_limit*.12,range_limit],color="#9fb4c8",gridcolor="rgba(80,130,170,.16)",showbackground=False),
               yaxis=dict(title="Y (m)",range=[-range_limit*.55,range_limit*.55],color="#9fb4c8",gridcolor="rgba(80,130,170,.16)",showbackground=False),
               zaxis=dict(title="Z (m)",range=[0,zmax],color="#9fb4c8",gridcolor="rgba(80,130,170,.16)",showbackground=False),
               camera=dict(eye=dict(x=1.55,y=1.55,z=1.10)),aspectmode="manual",aspectratio=dict(x=1.65,y=1.15,z=.72)))
st.plotly_chart(fig_paths,width="stretch",config={"displayModeBar":False,"responsive":True})

# ============================================================
# TABLE
# ============================================================
st.markdown('<div class="section-heading">Multipath Measurements</div>', unsafe_allow_html=True)
table_data=[{"Path":p["path"],"Distance (m)":round(p["distance"],2),"Path Loss (dB)":round(p["path_loss"],2),"Relative Power":f"{p['relative_power']:.6f}"} for p in multipath_results]
st.dataframe(table_data,width="stretch",hide_index=True)

# ============================================================
# VIVA / EXPLANATION
# ============================================================
info_card_1="""<div class="info-card"><div class="info-title">How does this simulation work?</div><div class="info-text">
This project models a simplified 5G MIMO beamforming transmitter. Each antenna element sends the same information with a controlled phase shift. The steering vector calculates those phase shifts so the waves add constructively in the selected UE direction.<br><br>
The 2D plot shows normalized array power versus angle. The polar plot shows the same angular response around 360 deg. The 3D plot turns the angular response into a spatial beam so you can visually see the main lobe and side lobes pointing toward the UE.<br><br>
The multipath model adds a direct line-of-sight path and user-configurable reflected paths. Each path uses free-space path loss, so increasing path distance reduces its relative received power. In Null-Steering mode the weight vector is additionally projected away from the interference direction.
</div></div>"""
info_card_2="""<div class="info-card"><div class="info-title">What should I explain in my college viva?</div><div class="info-text">
My project demonstrates software-based 5G MIMO beamforming. A multiple-antenna array is used to steer RF energy toward a desired User Equipment by controlling the phase of each antenna element.<br><br>
The steering vector determines the phase relationship. When the phases are aligned at the UE, the signals combine constructively and produce a high-gain main beam. Null steering modifies the weights to suppress an interference direction.<br><br>
The project also demonstrates free-space path loss, a link-budget-based SINR estimate, Shannon-style spectral efficiency, 2D and polar radiation patterns, a 3D spatial beam, and configurable multipath propagation.
</div></div>"""
st.markdown(f'<div class="info-grid">{info_card_1}{info_card_2}</div>',unsafe_allow_html=True)
st.markdown('<div class="footer">5G MIMO Beamforming Simulator | Educational College Mini Project</div>',unsafe_allow_html=True)
