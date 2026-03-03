import streamlit as st
import pandas as pd
from io import BytesIO
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector, plot_histogram, plot_state_qsphere
from qiskit.quantum_info import Statevector, Operator
import matplotlib.pyplot as plt

# --- Page Config & Memory ---
st.set_page_config(page_title="Qiskit Quantum Playground", layout="wide")

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

# --- Persistent Header ---
st.title("⚛️ Qiskit Quantum Playground")
st.markdown("👨‍💻 **Developed by: Shiva Krishna Nallabothu** *Assistant Professor | M.Tech (Ph.D) in Computer Science | **KLH (Deemed to be University)***")
st.write("") 

# --- GENERAL ADDITION: Glossary Sidebar ---
def render_glossary():
    with st.sidebar.expander("📖 Quantum Glossary"):
        st.markdown("""
        * **Superposition:** A state where a qubit is a combination of |0⟩ and |1⟩.
        * **Entanglement:** A quantum link between qubits where the state of one dictates the state of another.
        * **Interference:** Amplitudes of quantum states amplifying or canceling each other out.
        * **Unitary Matrix:** The mathematical representation of a reversible quantum gate.
        * **Decoherence:** The loss of a quantum state due to environmental noise.
        """)

# ==========================================
# PAGE VIEW: HOME 
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
            st.write("Foundations of qubits, gates, Q-Spheres, and linear algebra.")
            if st.button("Start Level 1", use_container_width=True, type="primary"):
                navigate_to('level1')
                st.rerun()
        with st.container(border=True):
            st.markdown("### Level 3")
            st.markdown("## 🌐 Real Hardware & Noise")
            st.write("Error correction, T1/T2 relaxation times, and noise simulation.")
            if st.button("Start Level 3", use_container_width=True, type="primary"):
                navigate_to('level3')
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### Level 2")
            st.markdown("## 🚀 Famous Algorithms")
            st.write("Simon's, Grover's, Deutsch-Jozsa, and QFT.")
            if st.button("Start Level 2", use_container_width=True, type="primary"):
                navigate_to('level2')
                st.rerun()
        with st.container(border=True):
            st.markdown("### Level 4")
            st.markdown("## 🧬 Quantum Applications")
            st.write("BB84 with Eve, VQE Chemistry, and QAOA MaxCut.")
            if st.button("Start Level 4", use_container_width=True, type="primary"):
                navigate_to('level4')
                st.rerun()

# ==========================================
# PAGE VIEW: LEVEL 1 (Upgraded)
# ==========================================
def render_level_1():
    render_glossary()
    
    if st.button("⬅️ Back to Home"):
        navigate_to('home')
        st.rerun()
        
    st.divider()
    st.title("🌟 Level 1: Quantum Basics")

    st.sidebar.header("1. Circuit Builder")
    num_qubits = 3
    qc = QuantumCircuit(num_qubits)

    # Manual Circuit Builder
    st.sidebar.subheader("A. Set Initial States")
    col1, col2, col3 = st.sidebar.columns(3)
    with col1: st.session_state.init_states[0] = 1 if st.checkbox("Q0 = |1⟩", value=bool(st.session_state.init_states[0])) else 0
    with col2: st.session_state.init_states[1] = 1 if st.checkbox("Q1 = |1⟩", value=bool(st.session_state.init_states[1])) else 0
    with col3: st.session_state.init_states[2] = 1 if st.checkbox("Q2 = |1⟩", value=bool(st.session_state.init_states[2])) else 0

    st.sidebar.divider()
    st.sidebar.subheader("B. Add Gates")
    gate_choice = st.sidebar.selectbox("Select Gate", ["H (Hadamard)", "X (NOT)", "Y", "Z", "S (Phase)", "T (Pi/8)", "CNOT", "SWAP", "CCNOT (Toffoli)"])
    
    if gate_choice in ["CNOT", "SWAP"]:
        ctrl = st.sidebar.radio("Qubit 1 (Control/Swap A)", [0, 1, 2], horizontal=True)
        tgt = st.sidebar.radio("Qubit 2 (Target/Swap B)", [0, 1, 2], index=1, horizontal=True)
        if st.sidebar.button(f"➕ Add {gate_choice}"):
            if ctrl != tgt: st.session_state.gates.append((gate_choice.split()[0], ctrl, tgt))
            else: st.sidebar.error("Qubits must be different!")
            
    elif gate_choice == "CCNOT (Toffoli)":
        c1 = st.sidebar.selectbox("Control 1", [0, 1, 2], index=0)
        c2 = st.sidebar.selectbox("Control 2", [0, 1, 2], index=1)
        tgt = st.sidebar.selectbox("Target", [0, 1, 2], index=2)
        if st.sidebar.button("➕ Add CCNOT"):
            if len(set([c1, c2, tgt])) == 3: st.session_state.gates.append(("CCNOT", c1, c2, tgt))
            else: st.sidebar.error("All three qubits must be unique!")
            
    else:
        tgt = st.sidebar.radio("Target Qubit", [0, 1, 2], horizontal=True)
        if st.sidebar.button(f"➕ Add {gate_choice.split()[0]}"):
            st.session_state.gates.append((gate_choice.split()[0], tgt))

    if st.sidebar.button("🗑️ Clear Circuit"):
        clear_circuit()
        st.rerun()

    # Construct Circuit
    for i, state_val in enumerate(st.session_state.init_states):
        if state_val == 1: qc.x(i) 
    if any(s == 1 for s in st.session_state.init_states): qc.barrier()
            
    for gate in st.session_state.gates:
        g = gate[0]
        if g == "CNOT": qc.cx(gate[1], gate[2])
        elif g == "SWAP": qc.swap(gate[1], gate[2])
        elif g == "CCNOT": qc.ccx(gate[1], gate[2], gate[3])
        elif g == "H": qc.h(gate[1])
        elif g == "X": qc.x(gate[1])
        elif g == "Y": qc.y(gate[1])
        elif g == "Z": qc.z(gate[1])
        elif g == "S": qc.s(gate[1])
        elif g == "T": qc.t(gate[1])

    # Circuit Math & Simulation
    state = Statevector.from_instruction(qc)
    unitary_op = Operator(qc).data
    
    qc_meas = qc.copy()
    qc_meas.measure_all()
    simulator = AerSimulator()
    counts = simulator.run(qc_meas, shots=1024).result().get_counts()

   
   # Visualizations & Educational Content
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualizations", "📖 Quantum Basics", "🧮 Linear Algebra", "📝 Knowledge Check"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1. Circuit Diagram")
            fig_circ = qc.draw(output='mpl')
            st.pyplot(fig_circ)
            
            buf = BytesIO()
            fig_circ.savefig(buf, format="png")
            st.download_button("💾 Download Circuit (PNG)", buf.getvalue(), "circuit.png", "image/png")

            st.subheader("3. Probability Distribution")
            fig_hist = plot_histogram(counts)
            st.pyplot(fig_hist)

        with col2:
            st.subheader("2. Q-Sphere (Phase Visualization)")
            st.write("Color represents phase; size represents probability.")
            fig_qsphere = plot_state_qsphere(state)
            st.pyplot(fig_qsphere)

            st.subheader("4. Statevector")
            state_data = state.data
            df_state = pd.DataFrame({
                "State": [f"|{format(i, f'0{num_qubits}b')}⟩" for i in range(len(state_data))],
                "Amplitude": state_data,
                "Probability (%)": [round(abs(amp)**2 * 100, 2) for amp in state_data]
            })
            st.dataframe(df_state, use_container_width=True)
            
            csv = df_state.to_csv(index=False)
            st.download_button("💾 Download State Data (CSV)", csv, "statevector.csv", "text/csv")

    with tab2:
        st.subheader("📖 The Foundations of Quantum Mechanics")
        st.markdown(r"""
        Before manipulating circuits, you need to understand the mathematical language of qubits.

        ### 1. Dirac Notation: Bras and Kets
        In quantum mechanics, we use **Dirac Notation** (bra-ket notation) to represent states and operations. 

        * **The Ket ($|\psi\rangle$):** Represents a quantum state as a **column vector**.
          $$|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad |1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$
        
        * **The Bra ($\langle\psi|$):** The complex conjugate transpose (also called Hermitian conjugate) of a Ket. It represents a state as a **row vector**.
          $$\langle 0| = \begin{pmatrix} 1 & 0 \end{pmatrix}, \quad \langle 1| = \begin{pmatrix} 0 & 1 \end{pmatrix}$$

        ### 2. Quantum Operations: Bra-Ket vs. Ket-Bra
        When we combine Bras and Kets, we perform specific linear algebra operations:

        * **Bra-Ket ($\langle\phi|\psi\rangle$) - The Inner Product:** A row vector multiplied by a column vector. It results in a **scalar** (a single complex number). In physics, this represents the *probability amplitude* of state $|\psi\rangle$ collapsing into state $|\phi\rangle$.
          *Example: Are $|0\rangle$ and $|1\rangle$ mutually exclusive (orthogonal)?*
          $$\langle 0 | 1 \rangle = \begin{pmatrix} 1 & 0 \end{pmatrix} \begin{pmatrix} 0 \\ 1 \end{pmatrix} = (1 \times 0) + (0 \times 1) = 0$$
          Since the inner product is $0$, there is a 0% chance a qubit in state $|1\rangle$ will be measured as $|0\rangle$.

        * **Ket-Bra ($|\psi\rangle\langle\phi|$) - The Outer Product:**
          A column vector multiplied by a row vector. It results in a **matrix** (an operator). This is often used to create projection operators or define quantum gates.
          *Example: Creating a projection matrix for state $|0\rangle$.*
          $$|0\rangle\langle 0| = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \begin{pmatrix} 1 & 0 \end{pmatrix} = \begin{pmatrix} 1\times1 & 1\times0 \\ 0\times1 & 0\times0 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$$

        ### 3. Vector Representation of a Qubit
        A qubit in superposition is a weighted sum of the basis vectors, using complex numbers $\alpha$ and $\beta$ (called amplitudes):
        $$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$$
        *Rule:* The total probability must equal 100%, so the inner product with itself must be 1: $\langle\psi|\psi\rangle = |\alpha|^2 + |\beta|^2 = 1$.

        ### 4. Polar Representation (The Bloch Sphere)
        Because global phase doesn't affect measurements, we can map the mathematical vector of a single qubit onto a 3D sphere using two angles ($\theta$ for latitude, $\phi$ for longitude):
        $$|\psi\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + e^{i\phi}\sin\left(\frac{\theta}{2}\right)|1\rangle$$
        """)
        
        st.divider()
        st.markdown(r"""
        ### 🚪 Quantum Gates & Their Matrices
        Gates are Unitary matrices that manipulate the qubit's vector.

        * **Pauli-X (NOT Gate):** Flips $|0\rangle$ to $|1\rangle$ and vice versa.
        $$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$
        
        * **Pauli-Y Gate:** Flips the state and introduces a phase shift of $i$.
        $$Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$$

        * **Pauli-Z (Phase Flip):** Leaves $|0\rangle$ alone, but flips the sign of $|1\rangle$.
        $$Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$
        
        * **Hadamard (H Gate):** Creates a perfect 50/50 superposition.
        $$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$
        
        * **CNOT (Controlled-NOT):** A 2-qubit gate. Flips the target qubit *only* if the control qubit is $|1\rangle$.
        $$\text{CNOT} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$$
        """)

    with tab3:
        st.subheader("📚 Linear Algebra Crash Course")
        st.markdown(r"""
        Quantum mechanics is entirely powered by linear algebra. Here are the core concepts you need to know:

        * **Complex Numbers:** The "amplitudes" of quantum states are complex numbers, written as $z = a + bi$. The actual probability of measuring a state is the magnitude squared: $|z|^2 = a^2 + b^2$.
        * **Vectors (Statevectors):** As seen in the basics tab, a quantum state is a column vector.
        * **Vector Magnitude (Norm):** Because probabilities must add up to 1, the "length" (or norm) of a statevector must always equal 1. 
        * **Matrices & Square Matrices:** Quantum gates are linear operations represented by square matrices (same number of rows and columns). A 1-qubit gate is a $2 \times 2$ matrix, a 2-qubit gate is $4 \times 4$, etc.
        * **Unitary Matrices:** Quantum matrices must be *Unitary* ($U^{\dagger}U = I$). In plain English: **all quantum operations (except measurement) are perfectly reversible.**
        """)
        
        st.divider()
        st.subheader("🧮 How Matrix Multiplication Works")
        st.markdown(r"""
        When you apply a quantum gate to a qubit, you are multiplying the gate's matrix by the qubit's vector. 
        
        **Example:** Applying the Pauli-X (NOT) gate to a qubit in state $|0\rangle$.
        $$ \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} (0 \times 1) + (1 \times 0) \\ (1 \times 1) + (0 \times 0) \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \end{pmatrix} = |1\rangle $$
        As you can see, the math perfectly predicts that the qubit flips to $|1\rangle$!
        """)
        
        st.divider()
        st.subheader("⚙️ Behind the Scenes: Your Current Circuit's Matrix")
        st.write("Here is the final, combined unitary matrix for the exact circuit you have built in the sidebar right now. As you add more qubits, the matrix grows exponentially ($2^n \times 2^n$)!")
        
        df_unitary = pd.DataFrame(unitary_op)
        st.dataframe(df_unitary)

    with tab4:
        st.subheader("🧠 Quick Quiz")
        q1 = st.radio("What gate puts a qubit into a perfect 50/50 superposition?", ["X Gate", "Z Gate", "Hadamard Gate", "CNOT Gate"], index=None)
        if q1 == "Hadamard Gate": st.success("Correct! The Hadamard (H) gate creates superposition.")
        elif q1: st.error("Not quite. Try applying the H gate in the builder and check the probabilities!")
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
