# 📡 NextGen 5G MIMO Beamforming Testbed

A simple and interactive **5G MIMO Beamforming Simulation** developed using Python and Streamlit.

This mini project demonstrates how multiple antennas can focus a wireless signal toward a selected user and reduce interference from another direction.

Click this link for view the project : https://fiveg-mimo-beam-forming.onrender.com/

## 🎯 Project Objective

The main objective of this project is to understand and demonstrate the basic working of **5G MIMO Beamforming** through a graphical simulation.

The project demonstrates:

* 5G beamforming
* MIMO antenna arrays
* Beam steering
* Antenna phase shifting
* Interference reduction
* Null steering
* SINR calculation
* Spectral efficiency
* Beam pattern visualization

## ✨ Main Features

### 📡 Single User Beamforming

The user can select the direction of the target device.

The antenna array automatically changes its beam direction toward the selected user.

Target angle can be selected between:

```text
-90 degrees to +90 degrees
```

### 🎯 Interference Mitigation

The project also provides an **Interference Mitigation** mode.

In this mode:

* A target user can be selected.
* An interference direction can be selected.
* The main beam focuses on the target.
* The signal response toward the interference direction is reduced.

This demonstrates the basic concept of **null steering**.

## 🎛️ User Controls

The Streamlit sidebar provides controls for:

* Operational mode
* Number of antenna elements
* Antenna spacing
* Target user angle
* Interference angle

### Antenna Elements

The number of antennas can be changed from:

```text
4 to 32
```

### Antenna Spacing

The antenna spacing can be changed from:

```text
0.25 to 1.00
```

### Target Angle

The target user direction can be selected from:

```text
-90 degrees to +90 degrees
```

## 📊 Performance Results

The application displays important beamforming performance values.

### Directivity Gain

Shows the approximate gain obtained by using multiple antenna elements.

### SINR

Shows the signal quality compared with interference and noise.

A higher SINR generally means better signal quality.

### Spectral Efficiency

Shows the estimated communication efficiency of the simulated wireless link.

The result is displayed in:

```text
bits per second per Hz
```

## 📈 Graphical Output

The application provides two main graphs.

### 1. Beam Pattern

The beam pattern graph shows:

* Main beam
* Side lobes
* Target user direction
* Interference direction

The graph makes it easy to see how the antenna beam changes when the user changes the angle.

### 2. Polar Beam Pattern

The polar graph provides a visual representation of the antenna radiation pattern.

It shows the direction in which the antenna array is transmitting the strongest signal.

## 🔄 How the Simulation Works

The basic operation is:

```text
Select Operating Mode
          ↓
Select Number of Antennas
          ↓
Select Target Angle
          ↓
Calculate Antenna Phase
          ↓
Generate Beam Pattern
          ↓
Calculate Signal Power
          ↓
Calculate SINR
          ↓
Calculate Spectral Efficiency
          ↓
Display Results
```

For interference mitigation:

```text
Target User
     ↓
Generate Main Beam
     ↓
Interference Direction
     ↓
Reduce Signal Response
     ↓
Display Beam Pattern
```

## 🛠️ Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Main programming language |
| Streamlit  | Web-based user interface  |
| NumPy      | Numerical calculations    |
| Matplotlib | Graph visualization       |

## 📁 Project Structure

```text
5g-mimo-beamforming/
│
├── app.py
├── requirements.txt
├── README.md
└── screenshots/
    ├── dashboard.png
    ├── beam-pattern.png
    └── null-steering.png
```

## ⚙️ Installation

### Step 1: Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd 5g-mimo-beamforming
```

### Step 2: Create Virtual Environment

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
streamlit
numpy
matplotlib
```

## ▶️ Run the Project

Run:

```bash
streamlit run app.py
```

After starting the application, Streamlit will provide a local web address.

Example:

```text
http://localhost:8501
```

Open the address in your browser.

## 🎮 How to Use

### Single User Mode

1. Open the application.
2. Select **Single User Tracking**.
3. Select the number of antennas.
4. Select antenna spacing.
5. Select the target user angle.
6. Observe the beam pattern.
7. Check the gain, SINR and spectral efficiency.

### Interference Mitigation Mode

1. Select **Interference Mitigation**.
2. Select the target user angle.
3. Select the interference angle.
4. Observe the main beam.
5. Observe the reduced response toward the interference direction.
6. Check the updated SINR and spectral efficiency.

## 📚 Concepts Demonstrated

This project demonstrates concepts from:

### Wireless Communication

* 5G
* MIMO
* Beamforming
* Spatial processing
* Interference reduction

### Antenna Systems

* Antenna arrays
* Beam steering
* Radiation patterns
* Main beam
* Side lobes
* Grating lobes

### Signal Processing

* Phase shifting
* Steering vectors
* Beam weights
* Spatial filtering
* Null steering

## 🎓 Mini Project Viva

### What is beamforming?

Beamforming is a technique that uses multiple antennas to focus a wireless signal in a particular direction.

### Why are multiple antennas used?

Multiple antennas can improve signal strength, coverage and interference control.

### What is MIMO?

MIMO means Multiple Input Multiple Output. It uses multiple antennas at the transmitter and receiver to improve wireless communication performance.

### What is null steering?

Null steering reduces the antenna response in the direction of an unwanted interference signal.

### What is SINR?

SINR represents the quality of the desired signal compared with interference and noise.

### Why is antenna spacing important?

The distance between antenna elements affects the beam pattern and can create unwanted additional beams when the spacing becomes too large.

## ⚠️ Project Limitations

This project is an **educational simulation**.

It does not represent a complete commercial 5G system.

It does not currently simulate:

* Complete 5G NR protocol
* Real 5G hardware
* Real RF transmitters
* Real antenna hardware
* OFDM communication
* Channel coding
* Real-world multipath propagation
* Hardware imperfections

The main purpose is to demonstrate the basic concepts of **5G MIMO beamforming and interference mitigation**.

## 🚀 Future Improvements

Future versions can include:

* Real-time 3D beamforming
* Multiple users
* Moving users
* Real GPS integration
* 5G NR waveform simulation
* OFDM support
* Different channel models
* Doppler simulation
* Massive MIMO
* Adaptive beam tracking
* Machine learning based beam selection
* Software Defined Radio integration
* Real antenna hardware integration
* Cloud deployment

## 📌 Project Summary

```text
                 5G MIMO BEAMFORMING
                         |
          +--------------+--------------+
          |                             |
     Single User                Interference Mode
          |                             |
     Beam Steering                Null Steering
          |                             |
          +--------------+--------------+
                         |
                  Performance
                         |
             +-----------+-----------+
             |           |           |
            Gain        SINR    Spectral Efficiency
             |           |           |
             +-----------+-----------+
                         |
                  Visualization
                         |
              +----------+----------+
              |                     |
          Beam Pattern          Polar Pattern
```

## 👨‍💻 Author

**Akash**

### Project Title

**NextGen 5G MIMO Beamforming Testbed**

### Project Type

**College Mini Project**

### Domain

**5G / MIMO / Wireless Communication / Antenna Array / Signal Processing**

## 📄 License

This project is created for educational and academic purposes.

You are free to modify and improve the project for learning and research.
