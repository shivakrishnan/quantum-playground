import streamlit as st
import pandas as pd
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Qiskit Quantum Playground", layout="wide")

# --- Initialize Router & Memory ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'gates' not in st.session_state:
    st.session_state.gates = [] 
if 'init_states' not in st.session_state:
    st.session_state.init_states = [0, 0, 0] 

def clear_circuit():
    st.session_state.gates = []
    st.session_state.init_states = [0, 0, 0]

def navigate_to(page_name):
    st.session_state.page = page_name

# --- Persistent Header (Visible on all pages) ---
st.title("⚛️ Qiskit Quantum Playground")
st.markdown("""
👨‍💻 **Developed by: Shiva Krishna Nallabothu** *Assistant Professor | M.Tech (Ph.D) in Computer Science | **KLH (Deemed to be University)***
""")
st.write("") 

# ==========================================
# PAGE VIEW: HOME (The 4-Level Grid)
# ==========================================
def render_home():
    st.header("Embark on Your Quantum Journey")
    st.write("Select a level below to begin exploring the mechanics of quantum computing.")
    st.write("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### Level 1")
            st.markdown("## 🌟 Quantum Basics")
            st.write("Foundations of qubits, superposition, entanglement, and core gates.")
            st.write("")
            if st.button("Start Level 1", use_container_width=True, type="primary"):
                navigate_to('level1')
                st.rerun()
                
        with st.container(border=True):
            st.markdown("### Level 3")
            st.markdown("## 🌐 Real Hardware & Noise")
            st.write("Transitioning from perfect math to the messy real world with noise models and measurement toggles.")
            st.write("")
            if st.button("Start Level 3", use_container_width=True, type="primary"):
                navigate_to('level3')
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### Level 2")
            st.markdown("## 🚀 Famous Algorithms")
            st.write("Interactive walkthroughs of Quantum Teleportation, Superdense Coding, and Grover's Search.")
            st.write("")
            if st.button("Start Level 2", use_container_width=True, type="primary"):
                navigate_to('level2')
                st.rerun()
                
        with st.container(border=True):
            st.markdown("### Level 4")
            st.markdown("## 🧬 Quantum Applications")
            st.write("High-level visualizations of real-world use cases like Quantum Cryptography (QKD) and VQE.")
            st.write("")
            if st.button("Start Level 4", use_container_width=True, type="primary"):
                navigate_to('level4')
                st.rerun()

# ==========================================
# PAGE VIEW: LEVEL 1 (The Original Playground)
# ==========================================
def render_level_1():
    if st.button("⬅️ Back to Home"):
        navigate_to('home')
        st.rerun()
        
    st.divider()

    with st.expander("📚 Beginner's Guide to Quantum Computing (Click to expand)"):
        st.markdown("""
        ### 1. What is a Qubit?
        While classical computers use **bits** (which are strictly `0` or `1`), quantum computers use **qubits** (quantum bits). A qubit can exist as `|0⟩`, `|1⟩`, or a complex combination of both.
        ### 2. What is Superposition?
        Superposition is a quantum phenomenon where a qubit exists in a linear combination of both `|0⟩` and `|1⟩` simultaneously. 
        ### 3. What is the Bloch Sphere?
        The **Bloch Sphere** is a 3D geometric representation of a single qubit's state. The North Pole is `|0⟩`, the South Pole is `|1⟩`, and the Equator represents perfect Superposition.
        ### 4. Essential Quantum Gates
        * **X (NOT):** Flips a qubit from `|0⟩` to `|1⟩`. 
        * **H (Hadamard):** Puts a `|0⟩` or `|1⟩` qubit into a state of perfect Superposition.
        * **CNOT:** Flips the `Target` qubit ONLY if the `Control` qubit is `|1⟩`. Used to create Entanglement.
        ### 5. Entanglement
        Entanglement links two or more qubits together so the state of one instantly provides information about the other.
        """)

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
        st.sidebar.subheader("A. Set Initial States")
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

        if st.session_state.gates:
            st.sidebar.markdown("**Current Gate Sequence:**")
            seq_str = " ➔ ".join([f"{g[0]}({g[1]})" if len(g)==2 else f"{g[0]}({g[1]},{g[2]})" for g in st.session_state.gates])
            st.sidebar.info(seq_str)

        if st.sidebar.button("🗑️ Clear Circuit"):
            clear_circuit()
            st.rerun()

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

    st.sidebar.divider()
    st.sidebar.header("2. Simulation Settings")
    num_shots = st.sidebar.slider("Number of Shots", min_value=10, max_value=5000, value=1024, step=10)

    state = Statevector.from_instruction(qc)
    qc_meas = qc.copy()
    qc_meas.measure_all()
    simulator = AerSimulator()
    result = simulator.run(qc_meas, shots=num_shots).result()
    counts = result.get_counts()

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
        fig_bloch = plot_bloch_multivector(state, reverse_bits=True)
        st.pyplot(fig_bloch)

        st.subheader("4. Statevector Math (Theoretical)")
        state_data = state.data
        labels = [format(i, f'0{num_qubits}b') for i in range(len(state_data))]
        df_state = pd.DataFrame({
            "State": [f"|{l}⟩" for l in labels],
            "Amplitude (Complex)": state_data,
            "Probability (%)": [round(abs(amp)**2 * 100, 2) for amp in state_data]
        })
        st.table(df_state)

# ==========================================
# PAGE VIEW: LEVEL 2 (Famous Algorithms)
# ==========================================
# ==========================================
# PAGE VIEW: LEVEL 2 (Famous Algorithms)
# ==========================================
def render_level_2():
    if st.button("⬅️ Back to Home"):
        navigate_to('home')
        st.rerun()
        
    st.divider()
    st.title("🚀 Level 2: Famous Algorithms")
    st.write("See how basic quantum gates are combined to achieve the impossible.")

    tab1, tab2 = st.tabs(["🌌 Quantum Teleportation", "🔒 Superdense Coding"])

    with tab1:
        st.markdown("### The Teleportation Protocol")
        st.write("Move the exact quantum state of **Qubit 0** (Alice's message) over to **Qubit 2** (Bob's receiver) without a direct physical connection!")

        st.subheader("1. Prepare the Message (Qubit 0)")
        msg_state = st.selectbox(
            "Select a state to prepare on Qubit 0 to teleport it to Qubit 2:", 
            ["|1⟩ (Flipped State)", "|+⟩ (Positive Superposition)", "|-⟩ (Negative Superposition)"]
        )

        qc = QuantumCircuit(3)

        if msg_state == "|1⟩ (Flipped State)":
            qc.x(0)
        elif msg_state == "|+⟩ (Positive Superposition)":
            qc.h(0)
        elif msg_state == "|-⟩ (Negative Superposition)":
            qc.x(0)
            qc.h(0)
        qc.barrier(label="Prepare")

        qc.h(1)
        qc.cx(1, 2)
        qc.barrier(label="Entangle")

        qc.cx(0, 1)
        qc.h(0)
        qc.barrier(label="Alice")

        qc.cx(1, 2)
        qc.cz(0, 2)
        qc.barrier(label="Bob")

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("2. The Teleportation Circuit")
            fig_circ = qc.draw(output='mpl')
            st.pyplot(fig_circ)

        with col2:
            st.subheader("3. Final Bloch Spheres")
            st.info("🎯 **Look at Q2!** It now perfectly matches the state you selected for Q0.")
            
            state = Statevector.from_instruction(qc)
            fig_bloch = plot_bloch_multivector(state, reverse_bits=True)
            st.pyplot(fig_bloch)

        with st.expander("📚 How does Teleportation actually work?"):
            st.markdown("""
            Quantum Teleportation requires three steps:
            1. **Entanglement Distribution:** Alice and Bob share an entangled pair of qubits (Q1 and Q2). Alice takes Q1, Bob takes Q2.
            2. **Alice's Measurement:** Alice wants to send Q0. She entangles Q0 with her Q1, and applies a Hadamard gate. This destroys the state of Q0, but transfers its information into the entangled link.
            3. **Bob's Correction:** Because Q1 and Q2 were entangled, Bob's Q2 reacts instantly. Based on how Alice manipulated her side, Bob simply applies an $X$ or $Z$ gate to lock the teleported state into his Qubit 2!
            """)

    with tab2:
        st.markdown("### The Superdense Coding Protocol")
        st.write("Send **two** classical bits of information by transmitting only **one** physical quantum bit!")
        
        

        st.subheader("1. Encode the Message (Alice)")
        message = st.selectbox(
            "Alice selects a 2-bit classical message to send to Bob:", 
            ["00", "01", "10", "11"]
        )

        # We need 2 qubits and 2 classical bits (for measurement)
        qc_sdc = QuantumCircuit(2, 2)

        # Step 1: Create Entanglement (Shared Bell Pair)
        qc_sdc.h(0)
        qc_sdc.cx(0, 1)
        qc_sdc.barrier(label="Share Pair")

        # Step 2: Alice Encodes her message using only HER qubit (Q0)
        if message == "01":
            qc_sdc.x(0)
        elif message == "10":
            qc_sdc.z(0)
        elif message == "11":
            qc_sdc.z(0)
            qc_sdc.x(0)
        qc_sdc.barrier(label="Alice Encodes")

        # Step 3: Bob Decodes using both qubits
        qc_sdc.cx(0, 1)
        qc_sdc.h(0)
        qc_sdc.barrier(label="Bob Decodes")

        # Step 4: Bob Measures
        qc_sdc.measure([0, 1], [0, 1])

        # Run Simulation
        simulator = AerSimulator()
        result_sdc = simulator.run(qc_sdc, shots=1024).result()
        counts_sdc = result_sdc.get_counts()

        # Display
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("2. The Superdense Circuit")
            fig_sdc = qc_sdc.draw(output='mpl')
            st.pyplot(fig_sdc)

        with col2:
            st.subheader("3. Bob's Measurement Result")
            st.success(f"🎯 Bob measured **{list(counts_sdc.keys())[0]}** with 100% certainty!")
            fig_hist_sdc = plot_histogram(counts_sdc)
            st.pyplot(fig_hist_sdc)

        with st.expander("📚 How does Superdense Coding work?"):
            st.markdown("""
            Superdense Coding works in reverse to Teleportation:
            1. **Entanglement:** Alice and Bob share an entangled pair. Alice holds Q0, Bob holds Q1.
            2. **Encoding:** Alice wants to send a 2-bit message. She applies specific gates to *only her qubit* (Q0):
               * `00` $\\rightarrow$ Do nothing (Identity)
               * `01` $\\rightarrow$ Apply $X$ gate
               * `10` $\\rightarrow$ Apply $Z$ gate
               * `11` $\\rightarrow$ Apply $Z$ then $X$
            3. **Transmission:** Alice physically sends her single qubit (Q0) to Bob.
            4. **Decoding:** Bob receives Q0. He applies a CNOT and a Hadamard gate to the pair, then measures them. Thanks to the magic of the initial entanglement, the result will always perfectly match Alice's 2-bit message!
            """)
# ==========================================
# PAGE VIEW: LEVEL 3 (Real Hardware & Noise)
# ==========================================
def render_level_3():
    # Import noise tools specifically for this level
    from qiskit_aer.noise import NoiseModel, depolarizing_error

    if st.button("⬅️ Back to Home"):
        navigate_to('home')
        st.rerun()
        
    st.divider()
    st.title("🌐 Level 3: Real Hardware & Noise")
    st.write("Real quantum computers aren't perfect. They suffer from 'noise' (errors) due to temperature fluctuations, radiation, and imperfect lasers. Let's see what happens when we run a perfect mathematical circuit on messy real-world hardware.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Measurement Toggles")
        st.write("First, let's create a Bell State. Choose which qubits you actually want to measure. In the real world, measuring just one part of an entangled pair collapses the other!")
        meas_q0 = st.checkbox("Measure Q0", value=True)
        meas_q1 = st.checkbox("Measure Q1", value=True)

    with col2:
        st.subheader("2. Inject Quantum Noise")
        st.write("Simulate real hardware by injecting random errors into our logic gates.")
        error_rate_percent = st.slider("Hardware Error Rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=1.0)
        error_rate = error_rate_percent / 100.0

    # Build the Bell State Circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    
    # Apply selected measurements
    if meas_q0:
        qc.measure(0, 0)
    if meas_q1:
        qc.measure(1, 1)

    # 1. Run Ideal Simulation (Perfect Math)
    simulator_ideal = AerSimulator()
    result_ideal = simulator_ideal.run(qc, shots=1024).result()
    counts_ideal = result_ideal.get_counts() if (meas_q0 or meas_q1) else {"None": 1024}

    # 2. Run Noisy Simulation (Real Hardware)
    noise_model = NoiseModel()
    # Add depolarizing error (random state flips) to our gates
    error_1q = depolarizing_error(error_rate, 1)
    error_2q = depolarizing_error(error_rate * 2, 2) # 2-qubit gates are usually noisier
    noise_model.add_all_qubit_quantum_error(error_1q, ['h'])
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

    simulator_noisy = AerSimulator(noise_model=noise_model)
    result_noisy = simulator_noisy.run(qc, shots=1024).result()
    counts_noisy = result_noisy.get_counts() if (meas_q0 or meas_q1) else {"None": 1024}

    # Visualizations
    st.divider()
    st.subheader("3. Simulation Results")
    col_hist1, col_hist2 = st.columns(2)
    
    with col_hist1:
        st.write("**Ideal Quantum Computer (0% Error)**")
        st.pyplot(plot_histogram(counts_ideal))
        
    with col_hist2:
        st.write(f"**Noisy Hardware ({error_rate_percent}% Error)**")
        st.pyplot(plot_histogram(counts_noisy))
        
    st.info("💡 **Learning Exercise:** A perfect Bell State should only ever output `00` or `11`. Look at the Noisy Hardware chart. Because of the injected noise, you will see 'impossible' results like `01` and `10` creeping in! This is why Quantum Error Correction is the biggest challenge in the industry right now.")


# ==========================================
# PAGE VIEW: LEVEL 4 (Quantum Applications)
# ==========================================
def render_level_4():
    if st.button("⬅️ Back to Home"):
        navigate_to('home')
        st.rerun()
        
    st.divider()
    st.title("🧬 Level 4: Quantum Applications")
    st.write("Why does all this matter? Let's explore a real-world use case: **Unhackable Cryptography**.")

    st.markdown("### The BB84 Protocol (Quantum Key Distribution)")
    st.write("Alice and Bob want to create a perfectly secure secret password (a key) over the internet. If a hacker (Eve) tries to intercept the qubits, the laws of quantum mechanics will force the qubit's state to collapse, instantly altering the data and alerting Alice and Bob to the intrusion!")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📡 Alice's Transmission")
        st.write("Alice encodes a binary bit into a qubit using a specific 'basis' (filter).")
        alice_bit = st.selectbox("1. Alice wants to send the bit:", ["0", "1"])
        alice_basis = st.radio("2. Alice encodes it using Basis:", ["Standard (+)", "Diagonal (x)"], horizontal=True)
    
    with col2:
        st.subheader("📥 Bob's Reception")
        st.write("Bob receives the qubit, but he doesn't know which filter Alice used! He has to guess.")
        bob_basis = st.radio("3. Bob randomly guesses a Basis to measure in:", ["Standard (+)", "Diagonal (x)"], horizontal=True)

    # Cryptography Logic
    match = alice_basis == bob_basis
    
    st.divider()
    st.subheader("🔐 The Result")
    if match:
        st.success(f"✅ **Bases Match!** Bob guessed the right filter. He correctly measured the bit **{alice_bit}**. This bit is kept and added to their secure secret key.")
    else:
        st.warning(f"❌ **Bases Mismatch!** Bob guessed the wrong filter. The quantum state collapsed incorrectly, and Bob measured random garbage. They discard this bit.")
        
    st.info("💡 **How it stops hackers:** By repeating this process thousands of times, Alice and Bob build a secure cryptographic key out of the matched bits. After they finish, they publicly compare a small sample of their matched bits. If a hacker intercepted the qubits mid-flight, the hacker would have guessed the wrong bases and corrupted the qubits. Alice and Bob would see a massive error rate in their sample and instantly know the line was tapped!")
# ==========================================
# ROUTING LOGIC (Determines what to show)
# ==========================================
if st.session_state.page == 'home':
    st.markdown(
        """
        <style>
            [data-testid="collapsedControl"] {display: none;}
            section[data-testid="stSidebar"] {display: none;}
        </style>
        """, unsafe_allow_html=True
    )
    render_home()
elif st.session_state.page == 'level1':
    render_level_1()
elif st.session_state.page == 'level2':
    render_level_2()
elif st.session_state.page == 'level3':
    render_level_3()
elif st.session_state.page == 'level4':
    render_level_4()
