# ⚛️ Qiskit Quantum Playground

Welcome to the **Qiskit Quantum Playground**! This is an interactive educational web application designed to demystify the "spooky" world of quantum mechanics. It allows learners to build quantum circuits, visualize the math, and see the results instantly without needing to write any complex code.

## 🚀 Features

* **Interactive Circuit Builder:** Manually apply quantum gates (H, X, Y, Z, CNOT) to a 3-qubit system.
* **Quick Entanglement:** Instantly generate famous quantum states like the 2-qubit **Bell State** and 3-qubit **GHZ State**.
* **Real-Time Visualizations:** * **Quantum Circuit Diagram:** See the flow of your quantum logic.
  * **Probability Histogram:** Simulate real-world quantum measurements with an adjustable "shots" slider.
  * **Bloch Spheres:** Visualize the exact 3D state and phase of each individual qubit.
* **Statevector Math:** A dynamic table showing the underlying complex amplitudes and theoretical probabilities.
* **Built-in Crash Course:** An expanding reference guide to help novices understand Qubits, Superposition, Entanglement, and Gates.

## 🛠️ Built With

* [Python](https://www.python.org/) - The core programming language.
* [Qiskit](https://qiskit.org/) - IBM's open-source SDK for working with quantum computers.
* [Streamlit](https://streamlit.io/) - The framework used to turn the Python script into an interactive web app.
* [Pandas](https://pandas.pydata.org/) & [Matplotlib](https://matplotlib.org/) - For data formatting and visual rendering.

## 💻 How to Run Locally

If you want to run this playground on your own machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shivakrishnan/quantum-playground.git]
   cd quantum-playground

2. **Create a virtual environment (Python 3.10+ recommended):**
python3 -m venv quantum_env
source quantum_env/bin/activate  # On Windows use: quantum_env\Scripts\activate

3. **Install the dependencies:**
pip install -r requirements.txt

4. **Run the Streamlit app:**
streamlit run app.py
