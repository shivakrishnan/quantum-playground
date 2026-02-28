import streamlit as st
import pandas as pd
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Qiskit Quantum Playground", layout="wide")
st.title("⚛️ Qiskit Quantum Playground")

# --- NEW: Educational Reference Section ---
with st.expander("📚 Beginner's Guide to Quantum Computing (Click to expand)"):
    st.markdown("""
    ### 1. What is a Qubit?
    While classical computers use **bits** (which are strictly `0` or `1`), quantum computers use **qubits** (quantum bits). A qubit can exist as `|0⟩`, `|1⟩`, or a complex combination of both. In quantum mechanics, we use the "Dirac notation" (the `| ⟩` brackets) to represent these states.

    ### 2. What is Superposition?
    Superposition is a quantum phenomenon where a qubit exists in a linear combination of both `|0⟩` and `|1⟩` simultaneously. It isn't definitively one or the other until we **measure** it. Once measured, the superposition "collapses" into a standard `0` or `1`.

    ### 3. What is the Bloch Sphere & Why is it required?
    The **Bloch Sphere** is a 3D geometric representation of a single qubit's state. 
    * The **North Pole** is `|0⟩`.
    * The **South Pole** is `|1⟩`.
    * The **Equator** represents a state of perfect Superposition.
    * **Why it's required:** Quantum states involve complex numbers (phases). The Bloch sphere allows us to easily visualize these complex mathematical states as simple 3D coordinates.

    ### 4. Essential Quantum Gates
    Gates are operations we apply to qubits to change their state.
    * **X (NOT):** Flips a qubit from `|0⟩` to `|1⟩`, and vice versa. (Like a classical NOT gate).
    * **H (Hadamard):** The magic gate! It puts a definitive `|0⟩` or `|1⟩` qubit into a state of perfect Superposition.
    * **Z and Y:** These are "Phase Gates". They rotate the qubit's state around the Z or Y axes of the Bloch Sphere without changing its measurement probability.
    * **CNOT (Controlled-NOT):** A multi-qubit gate. It flips the `Target` qubit ONLY if the `Control` qubit is `|1⟩`. This is the primary gate used to create Entanglement.

    ### 5. Entanglement (The Spooky Stuff)
    Entanglement links two or more qubits together. Once entangled, the state of one qubit instantly provides information about the state of the other, regardless of how far apart they are. The **Bell State** and **GHZ State** are famous examples of entanglement.
    """)

# --- Initialize Session State (Memory) ---
if 'gates' not in st.session_state:
    st.session_state.gates = [] 
if 'init_states' not in st.session_state:
    st.session_state.init_states = [0, 0, 0] 

def clear_circuit():
    st.session_state.gates = []
    st.session_state.init_states = [0, 0, 0]

# --- Sidebar: Circuit Construction ---
st.sidebar.header("1. Circuit Builder")
num_qubits = 3
qc = QuantumCircuit(num_qubits)

mode = st.sidebar.radio("Choose Circuit Mode:", 
                        ["🛠️ Manual Build", "✨ Quick: Bell State", "🌌 Quick: GHZ State"])

if mode == "✨ Quick: Bell State":
    st.sidebar.success("2-Qubit Entanglement on Q0 & Q1")
    qc.h(0)
    qc.cx(0, 1)

elif mode == "🌌 Quick: GHZ State":
    st.sidebar.success("3-Qubit Entanglement!")
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)

else:
    # --- MANUAL MODE ---
    st.sidebar.subheader("A. Set Initial States")
    st.sidebar.write("By default, qubits start at |0⟩. Check boxes to start at |1⟩.")
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.session_state.init_states[0] = 1 if st.checkbox("Q0 = |1⟩", value=bool(st.session_state.init_states[0])) else 0
    with col2:
        st.session_state.init_states[1] = 1 if st.checkbox("Q1 = |1⟩", value=bool(st.session_state.init_states[1])) else 0
    with col3:
        st.session_state.init_states[2] = 1 if st.checkbox("Q2 = |1⟩", value=bool(st.session_state.init_states[2])) else 0

    st.sidebar.divider()
    
    st.sidebar.subheader("B. Add Gates")
    gate_choice = st.sidebar.selectbox("Select Gate", ["H (Hadamard)", "X (NOT)", "Y", "Z", "CNOT"])
    
    if gate_choice == "CNOT":
        ctrl = st.sidebar.radio("Control Qubit", [0, 1, 2], horizontal=True)
        tgt = st.sidebar.radio("Target Qubit", [0, 1, 2], index=1, horizontal=True)
        if st.sidebar.button("➕ Add CNOT"):
            if ctrl != tgt:
                st.session_state.gates.append(("CNOT", ctrl, tgt))
            else:
                st.sidebar.error("Control and Target must be different!")
    else:
        tgt = st.sidebar.radio("Target Qubit", [0, 1, 2], horizontal=True)
        if st.sidebar.button(f"➕ Add {gate_choice.split()[0]}"):
            st.session_state.gates.append((gate_choice.split()[0], tgt))

    # --- NEW: Gate History Visualizer ---
    if st.session_state.gates:
        st.sidebar.markdown("**Current Gate Sequence:**")
        # Format the list of gates into a readable sequence string
        seq_str = " ➔ ".join([f"{g[0]}({g[1]})" if len(g)==2 else f"{g[0]}({g[1]},{g[2]})" for g in st.session_state.gates])
        st.sidebar.info(seq_str)

    if st.sidebar.button("🗑️ Clear Circuit"):
        clear_circuit()
        st.rerun()

    # Construct the Manual Circuit from Memory
    for i, state_val in enumerate(st.session_state.init_states):
        if state_val == 1:
            qc.x(i) 
            
    if any(s == 1 for s in st.session_state.init_states):
        qc.barrier()
            
    for gate in st.session_state.gates:
        g_type = gate[0]
        if g_type == "CNOT":
            qc.cx(gate[1], gate[2])
        elif g_type == "H":
            qc.h(gate[1])
        elif g_type == "X":
            qc.x(gate[1])
        elif g_type == "Y":
            qc.y(gate[1])
        elif g_type == "Z":
            qc.z(gate[1])

# --- Sidebar: Simulation Settings ---
st.sidebar.divider()
st.sidebar.header("2. Simulation Settings")
num_shots = st.sidebar.slider("Number of Shots", min_value=10, max_value=5000, value=1024, step=10)

# --- Logic: Simulation ---
state = Statevector.from_instruction(qc)

qc_meas = qc.copy()
qc_meas.measure_all()
simulator = AerSimulator()
result = simulator.run(qc_meas, shots=num_shots).result()
counts = result.get_counts()

# --- Display: Visualizations ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Quantum Circuit")
    fig_circ = qc.draw(output='mpl')
    st.pyplot(fig_circ)

    st.subheader(f"3. Probability Distribution ({num_shots} Shots)")
    fig_hist = plot_histogram(counts)
    st.pyplot(fig_hist)

with col2:
    st.subheader("2. Bloch Sphere")
    st.write("Spheres are ordered **Q2, Q1, Q0** to match binary strings.")
    fig_bloch = plot_bloch_multivector(state, reverse_bits=True)
    st.pyplot(fig_bloch)

    # --- Mathematical Statevector View ---
    st.subheader("4. Statevector Math (Theoretical)")
    st.write("The underlying 'amplitudes' of the quantum state:")
    
    state_data = state.data
    labels = [format(i, f'0{num_qubits}b') for i in range(len(state_data))]
    df_state = pd.DataFrame({
        "State": [f"|{l}⟩" for l in labels],
        "Amplitude (Complex)": state_data,
        "Probability (%)": [round(abs(amp)**2 * 100, 2) for amp in state_data]
    })
    st.table(df_state)
