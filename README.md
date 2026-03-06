# 🌌 Quantum Playground

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://quantum-playground-t8e9gacf4mqg6fwfc4yqpg.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-6929C4.svg)](https://qiskit.org/)

**Quantum Playground** is an interactive, educational web application designed to bridge the gap between abstract quantum mechanics and practical quantum computing. Built with **Streamlit** and IBM's **Qiskit**, this platform takes users on a journey from foundational quantum mathematics all the way to real-world hybrid quantum applications.

---

## 🚀 Live Demo
**Play with the live application here:** [Quantum Playground on Streamlit](https://quantum-playground-t8e9gacf4mqg6fwfc4yqpg.streamlit.app/)

---

## 🧠 Curriculum & Features

The platform is divided into four distinct educational levels, each featuring interactive simulators, visual state vectors, and comprehensive textbook-style explanations.

### Level 1: Quantum Mathematics & Mechanics
* **Single Qubit Gates:** Explore the Bloch sphere, Dirac notation, and Pauli matrices (X, Y, Z, Hadamard).
* **Multi-Qubit Gates:** Understand quantum entanglement using CNOT and Toffoli gates.

### Level 2: Famous Quantum Algorithms
* **Communication Protocols:** Quantum Teleportation and Superdense Coding.
* **Deterministic Speedups:** Deutsch-Jozsa and Simon's Algorithm.
* **Search & Mathematics:** Grover's Search Algorithm and the Quantum Fourier Transform (QFT).

### Level 3: Real Hardware & Noise
* **The Measurement Postulate:** Wave function collapse and Einstein's "Spooky Action".
* **Thermodynamics:** Simulate actual hardware decay using $T_1$ (Thermal Relaxation) and $T_2$ (Dephasing) sliders.
* **Hardware Flaws:** Inject depolarizing (gate) noise and readout errors.
* **Quantum Error Correction:** Build a functional 3-Qubit Bit-Flip code with an active Toffoli parity check.

### Level 4: Quantum Applications (The NISQ Era)
* **Quantum Cryptography:** Simulate Alice, Bob, and Eve in the BB84 protocol to create unhackable keys.
* **Quantum Chemistry (VQE):** Act as a classical optimizer in a hybrid loop to find the ground state energy of a simulated molecule.
* **Logistics (QAOA):** Use quantum interference to solve the NP-Hard MaxCut graph problem.
* **Quantum Machine Learning:** Use a Quantum Feature Map to encode classical data into a complex quantum Hilbert space.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Quantum Engine:** Qiskit, Qiskit-Aer (Simulator & Noise Models)
* **Data & Math:** NumPy, Pandas
* **Visualization:** Matplotlib, Seaborn

---

## 💻 Local Installation & Setup

If you want to run this application locally on your own machine, follow these steps to set up your environment and dependencies.

### 1. Clone the repository
bash
git clone [https://github.com/shivakrishnan/quantum-playground.git](https://github.com/shivakrishnan/quantum-playground.git)
cd quantum-playground



### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to avoid dependency conflicts.

**For Windows:**

bash
python -m venv venv
venv\Scripts\activate



**For macOS and Linux:**

bash
python3 -m venv venv
source venv/bin/activate



### 3. Install Dependencies

Make sure you have a `requirements.txt` file in your root directory containing the following:


qiskit
qiskit-aer
streamlit
pandas
matplotlib
numpy
seaborn



Then, install them using pip:

bash
pip install -r requirements.txt



### 4. Run the Application

Start the Streamlit server to view the app in your local web browser:

bash
streamlit run app.py



## 👨‍💻 Author

**Shiva Krishna Nallabothu**

* **GitHub:** [@shivakrishnan](https://www.google.com/search?q=https://github.com/shivakrishnan)
* **LinkedIn:** [Nallabothu Shiva Krishna](https://www.linkedin.com/in/nallabothu88/)

Feel free to open an issue or submit a pull request if you have suggestions for new quantum algorithms or features!






