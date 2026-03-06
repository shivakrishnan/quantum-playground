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
st.markdown("👨‍💻 Developed by: Shiva Krishna Nallabothu | M.Tech (Ph.D) in Computer Science | Assistant Professor, KLH (Deemed to be University)|")
st.write("") 
st.markdown(""" **GitHub Repository:** [Click here to view the source code](https://github.com/shivakrishnan/quantum-playground)    """)
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
    # -----------------------------------------
    # 1. THE TOP BANNER IMAGE
    # -----------------------------------------
    # Replace 'banner.png' with the actual name of your image file.
    # use_container_width=True ensures it perfectly fits the width of the app.
    st.image("banner.png", use_container_width=True)
    
    # -----------------------------------------
    # 2. YOUR DETAILS & GITHUB LINK
    # -----------------------------------------
    # Use Markdown to create a clickable link to your GitHub profile or repository.   
    # Adds a subtle horizontal line to separate your header from the main content
    st.divider() 

    # -----------------------------------------
    # 3. ACTUAL CONTENT OF THE HOMEPAGE
    # -----------------------------------------
    st.title("🌌 Welcome to the Quantum Playground")
    st.write("An interactive platform to explore the math, algorithms, hardware, and applications of Quantum Computing.")
    
    #st.header("Embark on Your Quantum Journey")
    #st.write("Select a level below to begin exploring the mechanics of quantum computing.")
   # st.write("")
    
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
        st.subheader("🧠 Level 1 Final Quiz")
        st.write("Test your knowledge on the foundations of quantum mechanics, Dirac notation, and logic gates!")
        st.divider()

        # Dictionary of Quiz Questions
        quiz_data = [
            {
                "q": "1. In Dirac notation, what mathematical object does a 'Ket' ($|\\psi\\rangle$) represent?",
                "options": ["A row vector", "A column vector", "A scalar number", "A 2x2 matrix"],
                "answer": "A column vector",
                "explanation": "A Ket always represents a quantum state as a column vector."
            },
            {
                "q": "2. What does a 'Bra' ($\\langle\\psi|$) represent in linear algebra?",
                "options": ["A column vector", "A 3D sphere", "A row vector (complex conjugate transpose)", "An identity matrix"],
                "answer": "A row vector (complex conjugate transpose)",
                "explanation": "A Bra is the Hermitian conjugate of a Ket, turning the column vector into a row vector."
            },
            {
                "q": "3. When you multiply a Bra by a Ket ($\\langle\\phi|\\psi\\rangle$), what is the mathematical result?",
                "options": ["A scalar (a single number)", "A 2x2 matrix", "A 4x4 matrix", "A column vector"],
                "answer": "A scalar (a single number)",
                "explanation": "This is the inner product. A row vector multiplied by a column vector results in a single scalar number, representing probability amplitude."
            },
            {
                "q": "4. What is the value of the inner product $\\langle 0 | 1 \\rangle$?",
                "options": ["1", "0.5", "i", "0"],
                "answer": "0",
                "explanation": "Because |0⟩ and |1⟩ are mutually exclusive (orthogonal), their inner product is exactly 0."
            },
            {
                "q": "5. What mathematical operation does a Ket-Bra ($|\\psi\\rangle\\langle\\phi|$) represent?",
                "options": ["The Inner Product (Scalar)", "The Outer Product (Matrix / Operator)", "Vector Addition", "Matrix Division"],
                "answer": "The Outer Product (Matrix / Operator)",
                "explanation": "A column vector multiplied by a row vector generates a matrix, often used as a projection operator."
            },
            {
                "q": "6. For a valid quantum state $\\alpha|0\\rangle + \\beta|1\\rangle$, what must be true about the amplitudes?",
                "options": ["$\\alpha + \\beta = 1$", "$\\alpha$ and $\\beta$ must be real numbers", "$|\\alpha|^2 + |\\beta|^2 = 1$", "$\\alpha = \\beta$"],
                "answer": "$|\\alpha|^2 + |\\beta|^2 = 1$",
                "explanation": "The sum of the absolute squares (the probabilities) must always equal 1 (100%)."
            },
            {
                "q": "7. The Bloch Sphere is used to visually represent the state of:",
                "options": ["A classical bit", "Exactly one qubit", "Two entangled qubits", "An entire quantum circuit"],
                "answer": "Exactly one qubit",
                "explanation": "The Bloch sphere maps the complex state of a single qubit to 3D geometry. It cannot represent entangled multi-qubit states."
            },
            {
                "q": "8. Which quantum gate creates a perfect 50/50 superposition from a basis state?",
                "options": ["Pauli-X", "Pauli-Z", "CNOT", "Hadamard (H)"],
                "answer": "Hadamard (H)",
                "explanation": "The Hadamard gate spreads the probability equally between the |0⟩ and |1⟩ states."
            },
            {
                "q": "9. Which gate acts as the quantum equivalent of a classical NOT gate?",
                "options": ["Pauli-X", "Pauli-Y", "Pauli-Z", "Hadamard (H)"],
                "answer": "Pauli-X",
                "explanation": "The Pauli-X gate flips |0⟩ to |1⟩ and |1⟩ to |0⟩."
            },
            {
                "q": "10. What effect does the Pauli-Z gate have on the state $|1\\rangle$?",
                "options": ["Flips it to $|0\\rangle$", "Leaves it unchanged", "Applies a negative phase (changes it to $-|1\\rangle$)", "Puts it into superposition"],
                "answer": "Applies a negative phase (changes it to $-|1\\rangle$)",
                "explanation": "The Pauli-Z gate is a phase flip gate. It leaves |0⟩ alone but flips the sign of |1⟩."
            },
            {
                "q": "11. The Pauli-Y gate matrix contains which special mathematical element?",
                "options": ["Only 1s and 0s", "Fractions", "The imaginary unit ($i$)", "Negative infinity"],
                "answer": "The imaginary unit ($i$)",
                "explanation": "The Y gate introduces complex numbers into the state via the imaginary unit i and -i."
            },
            {
                "q": "12. What property of Unitary matrices ensures that quantum circuits are reversible?",
                "options": ["They are always diagonal", "$U^{\\dagger}U = I$ (Multiplying by its conjugate transpose gives the Identity)", "They are always 2x2", "They only contain real numbers"],
                "answer": "$U^{\\dagger}U = I$ (Multiplying by its conjugate transpose gives the Identity)",
                "explanation": "Because UU† = I, you can always apply the inverse of a quantum gate to perfectly reverse its effect!"
            }
        ]

        # Quiz Logic
        for i, q in enumerate(quiz_data):
            st.markdown(f"**{q['q']}**")
            ans = st.radio("Select an answer:", q["options"], key=f"quiz_{i}", index=None, label_visibility="collapsed")
            
            if ans == q["answer"]:
                st.success(f"✅ **Correct!** {q['explanation']}")
            elif ans is not None:
                st.error("❌ **Incorrect.** Try again or review the Quantum Basics tab.")
            st.write("") 
# ==========================================
# PAGE VIEW: LEVEL 2 (Famous Algorithms)
# ==========================================


# ==========================================
# PAGE VIEW: LEVEL 2 (Famous Algorithms)
# ==========================================
def render_level_2():
    import numpy as np # Required for QFT Pi calculations
    
    if st.button("⬅️ Back to Home"):
        navigate_to('home')
        st.rerun()
        
    st.divider()
    st.title("🚀 Level 2: Famous Algorithms")
    st.write("Explore how quantum mechanics allows us to communicate securely and solve problems exponentially faster than classical computers.")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🌌 Teleportation", 
        "🔒 Superdense Coding", 
        "⚖️ Deutsch-Jozsa", 
        "🔍 Simon's Algorithm", 
        "🔎 Grover's Search", 
        "🌊 QFT", 
        "📝 Quiz"
    ])

   
    # --- TAB 1: TELEPORTATION ---
    with tab1:
        st.markdown("### 🌌 Quantum Teleportation")
        st.write("Move the exact quantum state of **Qubit 0** over to **Qubit 2** without a physical connection!")

        # 1. Interactive Simulation
        msg_state = st.selectbox("1. Select a state to prepare on Q0 (Alice's Message):", ["|1⟩", "|+⟩", "|-⟩"])
        qc = QuantumCircuit(3)

        if msg_state == "|1⟩": qc.x(0)
        elif msg_state == "|+⟩": qc.h(0)
        elif msg_state == "|-⟩": qc.x(0); qc.h(0)
        qc.barrier(label="Prepare")

        qc.h(1); qc.cx(1, 2)
        qc.barrier(label="Entangle")

        qc.cx(0, 1); qc.h(0)
        qc.barrier(label="Alice")

        qc.cx(1, 2); qc.cz(0, 2)
        qc.barrier(label="Bob")

        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(qc.draw(output='mpl'))
        with col2:
            st.info("🎯 **Look at Q2!** It perfectly matches the state you prepared for Q0.")
            fig_bloch = plot_bloch_multivector(Statevector.from_instruction(qc), reverse_bits=True)
            st.pyplot(fig_bloch)

        st.divider()
        
        # 2. Detailed Educational Explanation
        st.markdown("### 📚 The Mechanics of Teleportation")
        
        with st.expander("1. What is Quantum Teleportation?"):
            st.markdown(r"""
            In quantum mechanics, **Quantum Teleportation is the transfer of quantum *information* (the exact state of a qubit) from one location to another without physically moving the particle itself.**

            Imagine Alice wants to send a qubit (Q0) to Bob, but they only have a standard classical internet connection. Quantum mechanics forbids her from simply "reading" her qubit and copying the data because measuring a superposition destroys it, and the **No-Cloning Theorem** states it is impossible to make a perfect copy of an unknown quantum state. 

            Instead, Alice and Bob use an entangled pair of qubits as an invisible bridge. Alice interacts her message qubit with her half of the entangled pair. This destroys her original message, but instantly teleports the *information* to Bob's half. Bob then uses two classical bits of instruction from Alice to "unlock" his qubit, perfectly reconstructing the original message.
            """)
            
        with st.expander("2. The Gate Sequence (Step-by-Step)"):
            st.markdown(r"""
            Let's translate the circuit diagram into the exact sequence of gates applied:
            
            * **Step 1: Preparation (Q0):** We apply gates to Q0 to create the secret message. For example, applying an $X$ gate creates the state $|1\rangle$, or applying an $H$ gate creates the state $|+\rangle$.
            * **Step 2: Entanglement Distribution (Q1 & Q2):** We create a Bell State between Q1 (Alice's receiver) and Q2 (Bob's receiver). 
                * Apply a Hadamard ($H$) gate to Q1.
                * Apply a CNOT gate with Q1 as the control and Q2 as the target.
            * **Step 3: Alice's Interaction (Q0 & Q1):** Alice entangles her secret message (Q0) with her half of the shared pair (Q1).
                * Apply a CNOT gate with Q0 as the control and Q1 as the target.
                * Apply a Hadamard ($H$) gate to Q0.
                * *Result:* The information from Q0 is scrambled and injected into the global entanglement link.
            * **Step 4: Bob's Correction (Q1, Q0 $\rightarrow$ Q2):** * *In the real world:* Alice measures Q0 and Q1, resulting in two classical bits (e.g., `01` or `11`). She phones Bob and tells him these bits. Depending on what she says, Bob applies an $X$ gate, a $Z$ gate, both, or neither to his Q2.
                * *In our simulation:* We use "deferred measurement." We simulate Alice's classical phone call using quantum gates. We apply a CNOT (Q1 controlling Q2) to act as the $X$ correction, and a CZ gate (Q0 controlling Q2) to act as the $Z$ correction.
            """)

        with st.expander("3. How do Q2 and Q0 end up with the same values?"):
            st.markdown(r"""
            They end up with the same values because of the mathematics of **entanglement** and **interference**.

            When Alice applies her CNOT and Hadamard gates to Q0 and Q1, she forces her two qubits into one of four specific entangled states (the Bell basis). Because Q1 is already intimately linked to Bob's Q2, forcing Q1 into a new state causes Bob's Q2 to react instantly. 

            Mathematically, the entire 3-qubit system collapses into a state where Bob's Q2 becomes identical to the original state of Q0, *except* it might be flipped upside down (a Pauli-X error) or pointing in the wrong phase direction (a Pauli-Z error). 

            When Bob applies his final correction gates (the CNOT and CZ in our simulation), he is essentially rotating his qubit to fix those exact errors. Once the rotation is done, the information is unlocked, and Q2 is mathematically identical to what Q0 used to be.
            """)

        with st.expander("4. The Role of the Bloch Spheres"):
            st.markdown(r"""
            The Bloch Sphere is a 3D geometric representation of a single qubit's state. It shows us the exact probability (latitude) and phase (longitude) of the qubit. 

            **Why are they relevant here?** In quantum computing, you cannot "look" at the math midway through a physical execution without destroying it. However, in a simulated environment, the Bloch Spheres act as our **visual proof of success**.

            * **Before Teleportation:** If you set Q0 to a negative superposition ($|-\rangle$), its Bloch sphere arrow points to the back of the equator. Bob's Q2 sphere points straight up at $|0\rangle$.
            * **After Teleportation:** You will see the arrow on Q0's sphere has completely changed—the original state was destroyed (proving the No-Cloning Theorem). But if you look at Q2's sphere, the arrow is now pointing exactly to the back of the equator ($|-\rangle$). 

            The Bloch spheres visually prove that the exact geometric coordinates of the quantum state jumped from Qubit 0 to Qubit 2, completely bypassing the space in between!
            """)
   # --- TAB 2: SUPERDENSE CODING ---
    with tab2:
        st.markdown("### 🔒 Superdense Coding")
        st.write("Send **two** classical bits of information by transmitting only **one** quantum bit!")

        # 1. Interactive Simulation
        message = st.selectbox("1. Alice selects a 2-bit message to send:", ["00", "01", "10", "11"])
        qc_sdc = QuantumCircuit(2, 2)

        qc_sdc.h(0); qc_sdc.cx(0, 1)
        qc_sdc.barrier(label="Share Pair")

        if message == "01": qc_sdc.x(0)
        elif message == "10": qc_sdc.z(0)
        elif message == "11": qc_sdc.z(0); qc_sdc.x(0)
        qc_sdc.barrier(label="Encode")

        qc_sdc.cx(0, 1); qc_sdc.h(0)
        qc_sdc.barrier(label="Decode")
        qc_sdc.measure([0, 1], [0, 1])

        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(qc_sdc.draw(output='mpl'))
        with col2:
            counts_sdc = AerSimulator().run(qc_sdc, shots=1024).result().get_counts()
            st.success(f"🎯 Bob measured **{list(counts_sdc.keys())[0]}**!")
            st.pyplot(plot_histogram(counts_sdc))
            
        st.divider()

        # 2. Detailed Educational Explanation
        st.markdown("### 📚 The Mechanics of Superdense Coding")
        
        with st.expander("1. What is Superdense Coding?"):
            st.markdown(r"""
            Superdense Coding is the exact opposite of Quantum Teleportation. 
            * **Teleportation:** Uses 2 classical bits to send 1 quantum bit.
            * **Superdense Coding:** Uses 1 quantum bit to send 2 classical bits.

            Imagine Alice wants to send Bob a 2-bit classical message (`00`, `01`, `10`, or `11`). Classically, she must send two physical bits over a wire. But if Alice and Bob share an entangled pair of qubits, Alice can encode her entire 2-bit message by manipulating *only her half* of the pair. She then physically sends her single qubit to Bob, doubling the efficiency of the communication channel!
            """)
            

        with st.expander("2. The Gate Sequence (Step-by-Step)"):
            st.markdown(r"""
            Let's trace the circuit to see how Alice pulls off this trick:
            
            * **Step 1: Share Pair (Q0 & Q1):** First, we create a standard Bell State ($|\Phi^+\rangle$) using a Hadamard ($H$) and CNOT gate. Alice takes Q0, and Bob takes Q1.
            * **Step 2: Alice Encodes (Q0 only):** Alice wants to send a specific message. She applies a gate to *only her qubit* (Q0) based on her message:
                * To send `00`: She does nothing (Applies Identity $I$).
                * To send `01`: She applies an $X$ gate (Bit flip).
                * To send `10`: She applies a $Z$ gate (Phase flip).
                * To send `11`: She applies both $Z$ and $X$ gates.
            * **Step 3: Transmission:** Alice physically sends Q0 to Bob. Bob now holds both Q0 and Q1.
            * **Step 4: Bob Decodes (Q0 & Q1):** Bob applies a CNOT gate (Q0 controlling Q1) followed by a Hadamard gate on Q0. This perfectly reverses the entanglement and extracts the classical information. 
            * **Step 5: Measurement:** Bob measures both qubits. The resulting 2-bit string will perfectly match Alice's original message!
            """)

        with st.expander("3. How does manipulating ONE qubit change BOTH?"):
            st.markdown(r"""
            The secret lies in the 4 **Bell States**. Because Q0 and Q1 are perfectly entangled, they act as a single mathematical system.
            
            By applying a gate to just Q0, Alice isn't just changing Q0; she is shifting the *entire 2-qubit system* into one of four distinct, mutually exclusive (orthogonal) Bell states:
            
            1. Message `00` $\rightarrow$ System remains in $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$
            2. Message `01` $\rightarrow$ System shifts to $|\Psi^+\rangle = \frac{|01\rangle + |10\rangle}{\sqrt{2}}$
            3. Message `10` $\rightarrow$ System shifts to $|\Phi^-\rangle = \frac{|00\rangle - |11\rangle}{\sqrt{2}}$
            4. Message `11` $\rightarrow$ System shifts to $|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}$

            When Bob receives Q0, he possesses the complete Bell state. His decoding gates (CNOT and H) simply act as a map, translating these four complex Bell states back into the simple, readable classical states: $|00\rangle, |01\rangle, |10\rangle,$ or $|11\rangle$.
            """)
            

        with st.expander("4. Why is this important?"):
            st.markdown(r"""
            Superdense Coding proves that entanglement can be consumed as a resource to increase **channel capacity**. 
            
            While we cannot send information *faster* than light using quantum mechanics, we can send information much more *densely*. In the future quantum internet, this means fiber optic cables transmitting qubits could carry significantly more data than classical cables using the same number of physical particles.
            """)
    # --- TAB 3: DEUTSCH-JOZSA ---
    with tab3:
        st.markdown("### ⚖️ Deutsch-Jozsa Algorithm")
        st.write("Determine if a hidden black-box function is *Constant* (outputs all 0s or all 1s) or *Balanced* (outputs half 0s, half 1s) in exactly **one** guess!")
        
        # 1. Interactive Simulation
        func_type = st.radio("Choose the hidden Oracle function:", ["Constant (Always 0)", "Balanced (Identity)"])
        qc_dj = QuantumCircuit(2, 1) # 1 input, 1 ancilla, 1 classical bit
        
        # Prepare Ancilla in |-> state
        qc_dj.x(1)
        qc_dj.h(0); qc_dj.h(1)
        qc_dj.barrier()
        
        # Oracle
        if func_type == "Balanced (Identity)":
            qc_dj.cx(0, 1)
        qc_dj.barrier()
        
        # Interference
        qc_dj.h(0)
        qc_dj.measure(0, 0)
        
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(qc_dj.draw(output='mpl'))
        with col2:
            counts_dj = AerSimulator().run(qc_dj, shots=100).result().get_counts()
            st.pyplot(plot_histogram(counts_dj))
            if list(counts_dj.keys())[0] == '0':
                st.success("Result is 0: The algorithm correctly proved the function is **Constant**!")
            else:
                st.warning("Result is 1: The algorithm correctly proved the function is **Balanced**!")

        st.divider()

        # 2. Detailed Educational Explanation
        st.markdown("### 📚 The Mechanics of Deutsch-Jozsa")
        
        with st.expander("1. What is the Problem we are solving?"):
            st.markdown(r"""
            Imagine you are given a "black box" (an **Oracle**) that contains a hidden function $f(x)$. You input a binary number $x$, and it spits out either a `0` or a `1`. 
            
            You are promised that the function is either:
            * **Constant:** It returns the exact same output (e.g., all 0s) for *every* possible input.
            * **Balanced:** It returns `0` for exactly half of the inputs, and `1` for the other half.
            
            **The Classical Way:** If you have an $n$-bit input, there are $2^n$ possible inputs. To be 100% sure if the function is constant or balanced using a classical computer, you must query the Oracle $2^{n-1} + 1$ times in the worst-case scenario. 
            
            **The Quantum Way:** The Deutsch-Jozsa algorithm can figure it out in exactly **ONE** query, regardless of how large $n$ is!
            """)

        with st.expander("2. The Gate Sequence (Step-by-Step)"):
            st.markdown(r"""
            Let's walk through how the circuit achieves this incredible speedup:
            
            
            * **Step 1: Initialization:** We start with an input register (Q0) set to $|0\rangle$, and an "ancilla" (helper) register (Q1) set to $|1\rangle$.
            * **Step 2: Superposition:** We apply Hadamard ($H$) gates to both qubits. Q0 enters a perfect superposition of all possible inputs. Q1 enters the negative superposition $|-\rangle$.
            * **Step 3: The Oracle:** We pass both qubits through the black-box function $U_f$. Because Q0 is in superposition, the Oracle evaluates *all possible inputs at the exact same time* (Quantum Parallelism). 
            * **Step 4: Interference:** We apply a final Hadamard gate to the input register (Q0). This is where the magic happens. The quantum states interfere with each other. If the function was constant, the amplitudes constructively interfere to land back on $|0\rangle$. If it was balanced, they destructively interfere and shift to $|1\rangle$.
            * **Step 5: Measurement:** We measure Q0. If we read a `0`, it's Constant. If we read a `1`, it's Balanced.
            """)

        with st.expander("3. The Secret Sauce: Phase Kickback"):
            st.markdown(r"""
            How does the Oracle communicate its answer to the input register? Through a purely quantum phenomenon called **Phase Kickback**.
            
            
            When we run the Oracle, the answer of $f(x)$ is technically added to the ancilla qubit (Q1). However, because we initialized Q1 in the special $|-\rangle$ state, adding the function's output mathematically flips the *global sign* (phase) of the input register (Q0) instead! 
            
            Mathematically, the state becomes:
            $$ \sum_{x} (-1)^{f(x)} |x\rangle |-\rangle $$
            
            The Oracle writes its secret answer directly into the relative phase (the positive or negative sign) of the input superposition. The final Hadamard gate then easily converts that phase difference into a measurable `0` or `1`.
            """)


# --- TAB 4: SIMON'S ALGORITHM ---
    with tab4:
        st.markdown("### 🔍 Simon's Algorithm")
        st.write("Discover a hidden 2-bit string $s$ inside an Oracle exponentially faster than a classical machine.")
        
        # 1. Interactive Simulation
        secret_s = st.selectbox("1. Choose the hidden string $s$:", ["00", "01", "10", "11"], index=3)
        qc_simon = QuantumCircuit(4, 2)

        qc_simon.h(0); qc_simon.h(1)
        qc_simon.barrier()

        if secret_s == "00":
            qc_simon.cx(0, 2); qc_simon.cx(1, 3)
        elif secret_s == "01":
            qc_simon.cx(1, 2); qc_simon.cx(1, 3)
        elif secret_s == "10":
            qc_simon.cx(0, 2); qc_simon.cx(0, 3)
        elif secret_s == "11":
            qc_simon.cx(0, 2); qc_simon.cx(1, 2); qc_simon.cx(0, 3); qc_simon.cx(1, 3)
        qc_simon.barrier()

        qc_simon.h(0); qc_simon.h(1)
        qc_simon.measure([0, 1], [0, 1])

        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(qc_simon.draw(output='mpl'))
        with col2:
            counts_simon = AerSimulator().run(qc_simon, shots=1024).result().get_counts()
            st.write(f"The circuit outputs bitstrings $z$ where $z \cdot s = 0 \pmod 2$.")
            st.pyplot(plot_histogram(counts_simon))

        st.divider()

        # 2. Detailed Educational Explanation
        st.markdown("### 📚 The Mechanics of Simon's Algorithm")
        
        with st.expander("1. What is the Problem we are solving?"):
            st.markdown(r"""
            Imagine a "black box" (an **Oracle**) that calculates a function $f(x)$. You are promised that this function has a secret, hidden bitstring called $s$. 
            
            The rule of the Oracle is that two different inputs, $x$ and $y$, will produce the exact same output *if and only if* they are related by the secret string $s$ through an XOR operation ($\oplus$).
            
            Mathematically: **$f(x) = f(y)$ if and only if $x \oplus y = s$**
            
            If $s = 00$, the function is strictly 1-to-1 (every input gives a unique output). If $s$ is anything else, the function is 2-to-1 (two inputs map to the same output). **Our goal is to find $s$.**
            """)

        with st.expander("2. The Exponential Quantum Speedup"):
            st.markdown(r"""
            **The Classical Way:** To find $s$ classically, you have to guess inputs until you accidentally find two that produce the same output. If the input is $n$ bits long, there are $2^n$ possibilities. To guarantee finding a match, a classical computer requires $O(2^{n/2})$ queries. For a 100-bit string, this would take millions of years.
            
            **The Quantum Way:** Simon's Algorithm finds $s$ using only **$O(n)$ queries**. For a 100-bit string, a quantum computer would only need to query the Oracle roughly 100 times! This was the first time an algorithm proved a problem could be solved exponentially faster in the quantum realm.
            """)

        with st.expander("3. The Gate Sequence (Step-by-Step)"):
            st.markdown(r"""
            
            Let's walk through how the circuit finds the secret string:
            
            * **Step 1: Initialization:** We start with two registers. The input register (top qubits) and the output register (bottom qubits), all initialized to $|0\rangle$.
            * **Step 2: Superposition:** Apply Hadamard ($H$) gates to the input register. It is now in a superposition of all possible inputs.
            * **Step 3: The Oracle:** We query the Oracle $U_f$. Because the input is in superposition, it calculates the output for *all* inputs simultaneously and entangles the input register with the output register. 
            * **Step 4: Interference:** We apply a second set of Hadamard gates to the input register. Because of the structure of the Oracle, the quantum amplitudes of the incorrect answers destructively interfere and cancel each other out!
            * **Step 5: Measurement:** We measure the input register. The destructive interference guarantees that we will *never* measure a bitstring that doesn't align with our secret string $s$.
            """)

        with st.expander("4. How do we find the secret string?"):
            st.markdown(r"""
            When we measure the input register, we don't get $s$ directly. Instead, we measure a bitstring $z$. 
            
            The mathematics of the interference guarantees that the dot product of $z$ and our secret string $s$ will always be an even number (congruent to 0 modulo 2):
            $$ z \cdot s = 0 \pmod 2 $$
            
            **Try it yourself:** 1. Set the hidden string to `11` in the dropdown above.
            2. Look at the histogram. You will only ever measure `00` or `11`.
            3. Why? Because $(0\times1 + 0\times1) = 0$ (even), and $(1\times1 + 1\times1) = 2$ (even). The impossible answers like `01` ($0\times1 + 1\times1 = 1$, odd) perfectly canceled out to 0% probability!
            
            By running the circuit a few times, we collect several different $z$ values. We then use a classical computer to solve this simple system of linear equations to reveal $s$!
            """)
    
    
    # --- TAB 5: GROVER'S SEARCH ---
    with tab5:
        st.markdown("### 🔎 Grover's Search Algorithm")
        st.write("Find a specific hidden item in an unsorted database with a quadratic speedup using Amplitude Amplification!")
        
        # 1. Interactive Simulation
        target = st.selectbox("1. Select the 2-qubit state to hide (the 'Winner'):", ["00", "01", "10", "11"], index=3)
        qc_grover = QuantumCircuit(2, 2)
        
        # Superposition
        qc_grover.h([0, 1])
        qc_grover.barrier()
        
        # Oracle (Flips the phase of the target state)
        if target == "00":
            qc_grover.x([0, 1]); qc_grover.cz(0, 1); qc_grover.x([0, 1])
        elif target == "01":
            qc_grover.x(0); qc_grover.cz(0, 1); qc_grover.x(0)
        elif target == "10":
            qc_grover.x(1); qc_grover.cz(0, 1); qc_grover.x(1)
        elif target == "11":
            qc_grover.cz(0, 1)
        qc_grover.barrier(label="Oracle")
        
        # Diffuser (Amplifies the state with the flipped phase)
        qc_grover.h([0, 1]); qc_grover.x([0, 1]); qc_grover.cz(0, 1); qc_grover.x([0, 1]); qc_grover.h([0, 1])
        qc_grover.barrier(label="Diffuser")
        
        qc_grover.measure([0, 1], [0, 1])
        
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(qc_grover.draw(output='mpl'))
        with col2:
            counts_grover = AerSimulator().run(qc_grover, shots=1024).result().get_counts()
            st.success(f"🎯 Amplitude Amplification worked! The target state |{target}⟩ has near 100% probability.")
            st.pyplot(plot_histogram(counts_grover))

        st.divider()

        # 2. Detailed Educational Explanation
        st.markdown("### 📚 The Mechanics of Grover's Algorithm")
        
        with st.expander("1. What is the Problem we are solving?"):
            st.markdown(r"""
            Imagine you are looking for a specific name in a massive, completely unsorted telephone book with $N$ entries. 
            
            **The Classical Way:** Because it is unsorted, you have no choice but to check each entry one by one. On average, you will have to check $N/2$ entries before finding the right one. In the worst case, you check all $N$ entries. The time complexity is $O(N)$.
            
            **The Quantum Way:** Grover's Algorithm allows a quantum computer to find the specific entry in roughly $\sqrt{N}$ steps! This is a **quadratic speedup**. If you had a database of 1 million items, a classical computer takes ~500,000 steps. A quantum computer using Grover's Algorithm takes only 1,000 steps!
            """)

        with st.expander("2. Step 1: The Oracle (Phase Inversion)"):
            st.markdown(r"""
            How does the quantum computer find the hidden item? It uses a clever trick called **Amplitude Amplification**.
            
            First, we put all our qubits into a perfect superposition, meaning the computer is looking at every single database entry simultaneously with equal probability.
            
            Next, we pass this superposition into an **Oracle**. The Oracle acts like a highlighter. It recognizes the "winning" state and flips its phase (multiplies its amplitude by -1). 
            
            If our winner is $|11\rangle$, the Oracle changes the state from:
            $$ |\psi\rangle = \frac{1}{2}|00\rangle + \frac{1}{2}|01\rangle + \frac{1}{2}|10\rangle + \frac{1}{2}|11\rangle $$
            To:
            $$ |\psi\rangle = \frac{1}{2}|00\rangle + \frac{1}{2}|01\rangle + \frac{1}{2}|10\rangle - \frac{1}{2}|11\rangle $$
            
            *Note: The probability (which is the amplitude squared) hasn't changed yet, because $(1/2)^2$ is the same as $(-1/2)^2$. We just "marked" it mathematically.*
            """)

        with st.expander("3. Step 2: The Diffuser (Inversion About the Mean)"):
            st.markdown(r"""
            Now that the winning state is pointing downwards (negative amplitude), we apply the **Diffuser** operator.
            
            The Diffuser calculates the *average* amplitude of all the states, and then flips every state over that average line.
            
            Because the winning state was negative, the average gets pulled down slightly. When you invert everything over this new, lower average:
            1. The incorrect, positive states get squashed down (their probabilities shrink).
            2. The marked, negative state gets flipped high above the average (its probability dramatically spikes!).
            
            For a small 2-qubit system like our simulation, applying the Oracle and Diffuser just **one time** is enough to boost the winning state's probability from 25% to exactly 100%! For larger databases, you just repeat the Oracle $\rightarrow$ Diffuser sequence roughly $\sqrt{N}$ times.
            """)
    
    # --- TAB 6: QFT ---
    # --- TAB 6: QFT ---
    with tab6:
        st.markdown("### 🌊 Quantum Fourier Transform (QFT)")
        st.write("The QFT shifts a quantum state from the computational basis (the Z-axis) into the phase basis (the X-Y plane). It is the backbone of Shor's factoring algorithm.")
        
        # 1. Interactive Simulation
        input_state = st.selectbox("1. Select an initial 3-qubit binary state (0 to 7):", ["000 (0)", "001 (1)", "010 (2)", "011 (3)", "100 (4)", "101 (5)", "110 (6)", "111 (7)"], index=1)
        qc_qft = QuantumCircuit(3)
        
        # Prepare the initial state
        binary_val = input_state.split()[0]
        for i, bit in enumerate(reversed(binary_val)): # Qiskit orders qubits right-to-left (q2, q1, q0)
            if bit == '1':
                qc_qft.x(i)
        qc_qft.barrier(label="Input")
        
        # Apply QFT to 3 qubits
        qc_qft.h(2)
        qc_qft.cp(np.pi/2, 1, 2)
        qc_qft.cp(np.pi/4, 0, 2)
        qc_qft.barrier()
        
        qc_qft.h(1)
        qc_qft.cp(np.pi/2, 0, 1)
        qc_qft.barrier()
        
        qc_qft.h(0)
        qc_qft.barrier()
        
        qc_qft.swap(0, 2) # Reverse order to match standard output
        
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(qc_qft.draw(output='mpl'))
        with col2:
            st.write("**Visualizing the Phase Shift:**")
            st.info("Notice how the colors (phases) change based on the number you input! The data is now stored in the angles.")
            fig_qs = plot_state_qsphere(Statevector.from_instruction(qc_qft))
            st.pyplot(fig_qs)

        st.divider()

        # 2. Detailed Educational Explanation
        st.markdown("### 📚 The Mechanics of the QFT")
        
        with st.expander("1. What is the Quantum Fourier Transform?"):
            st.markdown(r"""
            In classical computing, the Discrete Fourier Transform (DFT) converts a signal from the time domain into the frequency domain. It's how your computer processes audio and compresses images.
            
            The **Quantum Fourier Transform (QFT)** is the exact mathematical equivalent, but performed on the amplitudes of quantum states. 
            
            Instead of storing a number as a sequence of hard `0`s and `1`s (the computational basis), the QFT translates that number into a series of **angles (phases)** spread across a perfect superposition. This is known as the *phase basis*. 
            
            **Why is this important?** Period finding! Peter Shor realized that finding the prime factors of a massive number can be reduced to finding the repeating period of a mathematical sequence. The QFT is exponentially faster at finding these periods than any classical algorithm.
            """)

        with st.expander("2. Encoding Numbers into Phase"):
            st.markdown(r"""
            
            
            Let's say we input the number 5 (binary `101`). 
            
            Normally, the qubits just point up or down ($|0\rangle$ or $|1\rangle$) on the Z-axis of the Bloch sphere.
            
            When we apply the QFT, all qubits are thrown onto the equator of the Bloch sphere (superposition), but they point in different horizontal directions based on the input number:
            * **The least significant qubit** rotates by a tiny fraction of a circle.
            * **The middle qubit** rotates twice as fast.
            * **The most significant qubit** rotates four times as fast.
            
            It is exactly like reading the hands of a clock! The hours, minutes, and seconds hands all rotate at different fractions of a full circle. By looking at their angles, you know exactly what time it is. The QFT encodes binary numbers into the "clock hands" of the qubits.
            """)

        with st.expander("3. The Gate Sequence (Step-by-Step)"):
            st.markdown(r"""
            
            
            The QFT circuit is beautifully highly structured. For each qubit (starting from the most significant bit to the least), we do two things:
            
            1. **Hadamard Gate ($H$):** We apply an $H$ gate to throw the qubit onto the equator of the Bloch sphere (superposition).
            2. **Controlled-Phase Gates ($CP$ or $R_k$):** We apply controlled rotations. If the neighboring qubits are in the $|1\rangle$ state, they "kick" the target qubit, causing it to rotate around the Z-axis by a highly specific fraction of Pi ($\pi/2, \pi/4, \pi/8$, etc.). 
            
            Because the $CP$ gates use exponentially smaller fractions of $\pi$ the further apart the qubits are, the circuit perfectly builds the "clock hands" mentioned above.
            
            *Note: At the very end of the circuit, we apply `SWAP` gates to reverse the order of the qubits. This is a mathematical formality to make sure the output binary sequence reads left-to-right correctly!*
            """)
    # --- TAB 7: KNOWLEDGE CHECK ---
    with tab7:
        st.subheader("🧠 Level 2 Final Quiz")
        st.write("Test your understanding of quantum algorithms, Oracles, and communication protocols!")
        st.divider()
        
        # Dictionary of 12 Quiz Questions
        quiz_data_l2 = [
            {
                "q": "1. In Quantum Teleportation, what exactly is being teleported from Alice to Bob?",
                "options": ["A physical electron", "Two classical bits", "The quantum information/state of a qubit", "Energy"],
                "answer": "The quantum information/state of a qubit",
                "explanation": "Teleportation destroys the quantum state at Alice's location and perfectly reconstructs it at Bob's location using entanglement."
            },
            {
                "q": "2. What resources are consumed to successfully teleport one qubit?",
                "options": ["1 classical bit and 1 Bell pair", "2 classical bits and 1 Bell pair", "2 Bell pairs", "1 quantum bit and 2 Bell pairs"],
                "answer": "2 classical bits and 1 Bell pair",
                "explanation": "Alice and Bob must share one entangled Bell pair, and Alice must send Bob two classical bits to tell him which correction gates to apply."
            },
            {
                "q": "3. Superdense Coding allows Alice to send 2 classical bits using how many physical qubits?",
                "options": ["One", "Two", "Three", "Four"],
                "answer": "One",
                "explanation": "Alice only manipulates and sends *her half* of the entangled pair (1 qubit) to transmit '00', '01', '10', or '11'."
            },
            {
                "q": "4. In Superdense Coding, if Alice wants to send the message '10', which gate does she apply to her entangled qubit?",
                "options": ["X gate", "Z gate", "Hadamard gate", "Both Z and X gates"],
                "answer": "Z gate",
                "explanation": "Applying a Z gate shifts the shared Bell state to |Φ⁻⟩, which Bob will later decode into the classical bits '10'."
            },
            {
                "q": "5. The Deutsch-Jozsa algorithm proves a function is Constant or Balanced in how many guesses?",
                "options": ["N/2 guesses", "Log(N) guesses", "One single guess", "An infinite number of guesses"],
                "answer": "One single guess",
                "explanation": "Thanks to quantum parallelism and interference, DJ evaluates the global property of the function in just one shot, compared to the classical worst-case of 2^(n-1) + 1."
            },
            {
                "q": "6. In the Deutsch-Jozsa algorithm, how does the Oracle communicate its answer to the input register?",
                "options": ["By measuring the qubit", "Through Phase Kickback", "By applying a SWAP gate", "By teleporting it"],
                "answer": "Through Phase Kickback",
                "explanation": "Because the ancilla qubit is in the |−⟩ state, the Oracle's output flips the global phase of the input register without changing its probabilities."
            },
            {
                "q": "7. What kind of speedup does Simon's Algorithm provide over the best classical algorithm?",
                "options": ["Quadratic speedup", "Exponential speedup", "Linear speedup", "No speedup"],
                "answer": "Exponential speedup",
                "explanation": "Simon's Algorithm finds the hidden string in O(n) queries, whereas a classical computer requires O(2^(n/2)) queries. It was the first algorithm to prove exponential speedup!"
            },
            {
                "q": "8. When you measure the final output (z) in Simon's Algorithm, what mathematical relationship does it have with the hidden string (s)?",
                "options": ["z is exactly equal to s", "z is the inverse of s", "The dot product of z and s is even (z · s = 0 mod 2)", "The dot product is always odd"],
                "answer": "The dot product of z and s is even (z · s = 0 mod 2)",
                "explanation": "Quantum interference cancels out all answers where the dot product is odd. You use these even equations to solve for the hidden string s."
            },
            {
                "q": "9. Grover's Algorithm provides a quadratic speedup for which type of problem?",
                "options": ["Factoring large prime numbers", "Finding a specific item in an unsorted database", "Simulating chemical molecules", "Encrypting classical data"],
                "answer": "Finding a specific item in an unsorted database",
                "explanation": "Grover's algorithm searches an unsorted database in O(√N) time, compared to the classical O(N) time."
            },
            {
                "q": "10. What are the two main operations that are repeated in Grover's Algorithm?",
                "options": ["Teleportation and Decoding", "Phase Inversion (Oracle) and Inversion about the Mean (Diffuser)", "QFT and Inverse QFT", "Entanglement and Measurement"],
                "answer": "Phase Inversion (Oracle) and Inversion about the Mean (Diffuser)",
                "explanation": "The Oracle flips the sign of the target state, and the Diffuser flips all amplitudes over the average, causing the target's probability to spike."
            },
            {
                "q": "11. The Quantum Fourier Transform (QFT) transforms states from the computational basis (Z-axis) into the:",
                "options": ["Phase basis (X-Y plane)", "Classical basis", "Entangled basis", "Binary basis"],
                "answer": "Phase basis (X-Y plane)",
                "explanation": "QFT maps states onto the equator of the Bloch sphere, encoding numerical information in their relative phase angles."
            },
            {
                "q": "12. In both Teleportation and Superdense Coding, Alice and Bob must share what specific state before the protocol begins?",
                "options": ["A GHZ State", "A random superposition", "A Bell State (|Φ⁺⟩)", "A pure |00⟩ state"],
                "answer": "A Bell State (|Φ⁺⟩)",
                "explanation": "The |Φ⁺⟩ Bell State provides the perfect maximal entanglement required to act as the quantum communication bridge."
            }
        ]

        # Quiz Logic
        for i, q in enumerate(quiz_data_l2):
            st.markdown(f"**{q['q']}**")
            ans = st.radio("Select an answer:", q["options"], key=f"quiz_l2_full_{i}", index=None, label_visibility="collapsed")
            if ans == q["answer"]:
                st.success(f"✅ **Correct!** {q['explanation']}")
            elif ans is not None:
                st.error("❌ **Incorrect.** Try reviewing the algorithm tabs to find the answer!")
            st.write("")

# ==========================================
# PAGE VIEW: LEVEL 3 (Real Hardware & Noise)
# ==========================================
# ==========================================
# PAGE VIEW: LEVEL 3 (Real Hardware & Noise)
# ==========================================
def render_level_3():
    from qiskit_aer.noise import NoiseModel, thermal_relaxation_error, depolarizing_error, ReadoutError
    import numpy as np
    
    if st.button("⬅️ Back to Home"):
        navigate_to('home')
        st.rerun()
        
    st.divider()
    st.title("🌐 Level 3: Real Hardware & Noise")
    st.write("Transition from perfect mathematical vectors to the messy reality of physical quantum processors.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📏 Measurement Postulate", 
        "📉 T1 & T2 Decoherence", 
        "🎯 Hardware Errors", 
        "🩹 Error Correction", 
        "📝 Quiz"
    ])

    # --- TAB 1: MEASUREMENT & COLLAPSE ---
    with tab1:
        st.markdown("### 📏 The Measurement Postulate (Wave Function Collapse)")
        st.write("The math says qubits exist in superposition, but physical hardware can only output classical 0s and 1s. Let's force a quantum state to 'choose' a classical reality.")
        
        col_ui, col_sim = st.columns([1, 2])
        
        with col_ui:
            st.subheader("1. Build the Experiment")
            st.write("We start with a perfectly entangled Bell State ($|\Phi^+\rangle$) between Q0 and Q1.")
            st.write("**Choose what to measure:**")
            meas_q0 = st.checkbox("Measure Q0", value=False)
            meas_q1 = st.checkbox("Measure Q1", value=False)
            
        qc_meas = QuantumCircuit(2, 2)
        qc_meas.h(0)
        qc_meas.cx(0, 1)
        qc_meas.barrier()
        
        if meas_q0: qc_meas.measure(0, 0)
        if meas_q1: qc_meas.measure(1, 1)
            
        with col_sim:
            st.subheader("2. Circuit & Results")
            st.pyplot(qc_meas.draw(output='mpl'))
            
            if meas_q0 or meas_q1:
                counts_meas = AerSimulator().run(qc_meas, shots=1024).result().get_counts()
                st.pyplot(plot_histogram(counts_meas))
            else:
                st.info("⚠️ No measurements applied! The quantum state remains a hidden superposition. Check the boxes to extract classical data.")

        st.divider()
        st.markdown("### 📚 The Mechanics of Measurement")
        
        with st.expander("1. The Observer Effect (Collapse)"):
            st.markdown("""
            In quantum mechanics, you cannot "look" at a superposition without destroying it. The moment a physical measurement device interacts with a qubit, the delicate quantum state **collapses** into a definite, classical state (0 or 1).
            """)
            
            st.markdown(r"""
            If a qubit is in the state $|\psi\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$, it has a 50% chance of collapsing to 0 and a 50% chance of collapsing to 1. Once it collapses, all phase information is permanently lost.
            """)
            
        with st.expander("2. Entanglement and 'Spooky Action'"):
            st.markdown("""
            **Try this:** Check *only* "Measure Q0" above. 
            
            Because Q0 and Q1 are perfectly entangled in a Bell state, measuring Q0 doesn't just collapse Q0... it **instantly collapses Q1 as well**, even if Q1 hasn't been touched by a measurement laser! 
            
            If Q0 collapses to 1, the entire universe updates instantly to ensure Q1 is also 1. Albert Einstein famously referred to this phenomenon as *"spooky action at a distance."*
            """)

    # --- TAB 2: T1 & T2 NOISE ---
    with tab2:
        st.markdown("### 📉 Quantum Noise (T1 and T2 Decoherence)")
        st.write("Real qubits are fragile. Heat and radiation constantly attack them, destroying their quantum information over time.")
        
        col_ui2, col_sim2 = st.columns([1, 2])
        
        with col_ui2:
            st.subheader("1. Hardware Specifications")
            experiment = st.radio("Select Experiment:", ["Test T1 (Energy Decay)", "Test T2 (Dephasing)"])
            
            t1_val = st.slider("T1 Relaxation Time (µs)", min_value=10.0, max_value=200.0, value=50.0)
            t2_val = st.slider("T2 Dephasing Time (µs)", min_value=10.0, max_value=200.0, value=50.0)
            gate_time = st.slider("Gate Execution Time (µs)", min_value=0.1, max_value=50.0, value=5.0)
            
            if t2_val > 2 * t1_val:
                st.warning("Physics constraint: T2 cannot be strictly greater than 2 * T1. Lowering T2 automatically.")
                t2_val = 2 * t1_val

        qc_noise = QuantumCircuit(1, 1)
        if experiment == "Test T1 (Energy Decay)":
            qc_noise.x(0)
            qc_noise.barrier()
            qc_noise.id(0) 
        else:
            qc_noise.h(0)
            qc_noise.barrier()
            qc_noise.id(0)
            qc_noise.h(0)
            
        qc_noise.measure(0, 0)
        
        noise_model = NoiseModel()
        t1_ns = t1_val * 1000
        t2_ns = t2_val * 1000
        time_ns = gate_time * 1000
        
        error = thermal_relaxation_error(t1_ns, t2_ns, time_ns)
        noise_model.add_all_qubit_quantum_error(error, ['id'])
        
        with col_sim2:
            st.subheader("2. Simulated Hardware Output")
            counts_ideal = AerSimulator().run(qc_noise, shots=1024).result().get_counts()
            counts_noisy = AerSimulator(noise_model=noise_model).run(qc_noise, shots=1024).result().get_counts()
            
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.write("**Ideal Mathematical Computer**")
                st.pyplot(plot_histogram(counts_ideal))
            with col_chart2:
                st.write("**Physical Hardware (With Noise)**")
                st.pyplot(plot_histogram(counts_noisy))

        st.divider()
        st.markdown("### 📚 The Thermodynamics of Qubits")
        
        with st.expander("1. What is T1 (Thermal Relaxation)?"):
            
            st.markdown(r"""
            **T1 Time** measures how long it takes for a qubit to lose its energy to the environment. Imagine a qubit is a spinning top. Pushing it into the $|1\rangle$ state is like spinning the top very fast. Over time, friction slows it down until it decays back to the ground state $|0\rangle$. 
            """)
            
        with st.expander("2. What is T2 (Dephasing)?"):
            
            st.markdown("""
            **T2 Time** measures how long a qubit can maintain its delicate quantum phase (superposition) before the environment scrambles it. Even tiny magnetic fluctuations in the lab can cause the qubit's angle on the Bloch sphere equator to drift randomly. 
            """)

    # --- TAB 3: HARDWARE ERRORS ---
    with tab3:
        st.markdown("### 🎯 Hardware Errors (Depolarizing & Readout Noise)")
        st.write("Beyond time-based decay, errors also occur when we actively try to manipulate or measure the qubits.")
        
        col_ui3, col_sim3 = st.columns([1, 2])
        
        with col_ui3:
            st.subheader("1. Inject Errors")
            depol_prob = st.slider("Gate Error Rate (%)", 0.0, 10.0, 1.0) / 100.0
            readout_prob = st.slider("Measurement Error Rate (%)", 0.0, 15.0, 2.0) / 100.0
            
        qc_hw = QuantumCircuit(2, 2)
        qc_hw.h(0)
        qc_hw.cx(0, 1)
        qc_hw.measure([0, 1], [0, 1])
        
        hw_noise_model = NoiseModel()
        depol_1q = depolarizing_error(depol_prob, 1)
        depol_2q = depolarizing_error(depol_prob * 2, 2) 
        hw_noise_model.add_all_qubit_quantum_error(depol_1q, ['h'])
        hw_noise_model.add_all_qubit_quantum_error(depol_2q, ['cx'])
        
        ro_matrix = [[1 - readout_prob, readout_prob], [readout_prob, 1 - readout_prob]]
        readout_error = ReadoutError(ro_matrix)
        
        # FIX: Using the correct dedicated function for readout errors!
        hw_noise_model.add_all_qubit_readout_error(readout_error)
        
        with col_sim3:
            st.subheader("2. Results")
            counts_ideal_hw = AerSimulator().run(qc_hw, shots=1024).result().get_counts()
            counts_noisy_hw = AerSimulator(noise_model=hw_noise_model).run(qc_hw, shots=1024).result().get_counts()
            
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Ideal Bell State**")
                st.pyplot(plot_histogram(counts_ideal_hw))
            with c2:
                st.write("**Noisy Hardware Output**")
                st.pyplot(plot_histogram(counts_noisy_hw))

        st.divider()
        st.markdown("### 📚 Understanding Active Errors")
        
        with st.expander("1. Gate Errors (Depolarizing Noise)"):
            st.markdown("""
            Unlike T1 and T2 which happen naturally over time, **Gate Errors** occur when we actively try to change the qubit's state. 
            
            Quantum gates are usually physical microwave pulses fired at a superconducting chip. If the pulse is slightly too long, too short, or hits the wrong frequency, the qubit is rotated incorrectly. This is simulated as "Depolarizing Noise," which essentially replaces the target state with completely random garbage data at a certain probability rate. Notice how 2-qubit gates (like CNOT) are significantly harder to perform and carry twice the error rate of 1-qubit gates.
            """)
            
        with st.expander("2. Readout Errors"):
            st.markdown("""
            **Readout Errors** happen at the very end of the circuit. Even if the entire calculation was flawless, the physical hardware used to "read" the qubit might misfire. 
            
            For example, the resonator used to measure the qubit's frequency might accidentally mistake a 1 for a 0, or vice versa. This means the final probability histogram you see on your screen might be lying to you about the true underlying state of the computer!
            """)

    # --- TAB 4: ERROR CORRECTION ---
    with tab4:
        st.markdown("### 🩹 Quantum Error Correction (3-Qubit Code)")
        st.write("Since we cannot look at a qubit without collapsing it, we use helper qubits to detect and correct errors mathematically.")
        
        col_ui4, col_sim4 = st.columns([1, 2])
        
        with col_ui4:
            st.subheader("1. Inject a Malfunction")
            error_target = st.radio("Force a Bit-Flip (X) Error on:", ["No Error", "Qubit 0 (Data)", "Qubit 1 (Ancilla)", "Qubit 2 (Ancilla)"])
            
        qc_qec = QuantumCircuit(3, 1)
        qc_qec.x(0)
        qc_qec.barrier(label="Data")
        
        # Encode
        qc_qec.cx(0, 1)
        qc_qec.cx(0, 2)
        qc_qec.barrier(label="Encode")
        
        # Inject Error
        if error_target == "Qubit 0 (Data)": qc_qec.x(0)
        elif error_target == "Qubit 1 (Ancilla)": qc_qec.x(1)
        elif error_target == "Qubit 2 (Ancilla)": qc_qec.x(2)
        qc_qec.barrier(label="Noise")
        
        # Decode & Correct
        qc_qec.cx(0, 1)
        qc_qec.cx(0, 2)
        qc_qec.ccx(1, 2, 0) 
        qc_qec.barrier(label="Correct")
        
        qc_qec.measure(0, 0)
        
        with col_sim4:
            st.subheader("2. Circuit & Healing Output")
            st.pyplot(qc_qec.draw(output='mpl'))
            
            counts_qec = AerSimulator().run(qc_qec, shots=1024).result().get_counts()
            if list(counts_qec.keys())[0] == '1':
                st.success("Target is perfectly preserved as 1! The Toffoli gate corrected the error.")
            else:
                st.error("Error destroyed the data!")
            st.pyplot(plot_histogram(counts_qec))

        st.divider()
        st.markdown("### 📚 The Mechanics of Error Correction")
        
        with st.expander("1. The No-Cloning Theorem & Redundancy"):
            st.markdown("""
            In classical computing, we correct errors by making backup copies of the data (like copying a hard drive). However, the **No-Cloning Theorem** proves it is physically impossible to create an exact copy of an unknown quantum state. 
            
            Instead of copying, we use **Entanglement**. In this circuit, we entangle our single logical data qubit (Q0) with two "Ancilla" or helper qubits (Q1 and Q2) using CNOT gates. This stretches the information of one qubit across three physical qubits.
            """)
            
            
        with st.expander("2. Parity Checks & Majority Voting"):
            st.markdown("""
            If an error occurs, how do we fix it without measuring (and thus destroying) the data? We use **Parity Checks**.
            
            The second set of CNOT gates compares the data qubit to the ancilla qubits. Finally, the **Toffoli (CCX) gate** acts as a physical "Majority Vote." It looks at the two helper qubits. If both of them suggest that Q0 flipped by accident, the Toffoli gate automatically flips Q0 back to its correct state—all while keeping the data safely inside its quantum superposition!
            """)

   # --- TAB 5: QUIZ ---
    with tab5:
        st.subheader("🧠 Level 3 Final Quiz")
        st.write("Test your knowledge of quantum measurement, hardware noise, and error correction!")
        st.divider()
        
        quiz_data_l3 = [
            {
                "q": "1. What happens when you physically measure a qubit that is in a superposition?",
                "options": ["It remains in superposition", "It collapses to a classical 0 or 1", "It duplicates itself", "It reverses time"],
                "answer": "It collapses to a classical 0 or 1",
                "explanation": "Measurement destroys the delicate quantum state, permanently forcing it into a classical reality and destroying its phase."
            },
            {
                "q": "2. In a perfectly entangled Bell state, measuring Qubit 0 instantly collapses Qubit 1. What did Albert Einstein call this phenomenon?",
                "options": ["Phase Kickback", "Quantum Parallelism", "Spooky action at a distance", "Decoherence"],
                "answer": "Spooky action at a distance",
                "explanation": "Einstein was skeptical that information could seem to travel faster than light, hence his famous 'spooky action' quote."
            },
            {
                "q": "3. Thermal Relaxation ($T_1$ time) refers to:",
                "options": ["The qubit losing its phase", "The qubit losing energy and decaying from $|1\\rangle$ to the ground state $|0\\rangle$", "A laser reading the wrong value", "Gate execution time"],
                "answer": "The qubit losing energy and decaying from $|1\\rangle$ to the ground state $|0\\rangle$",
                "explanation": "$T_1$ is energy decay, much like a spinning top losing momentum to friction and falling over."
            },
            {
                "q": "4. $T_2$ Dephasing primarily destroys which quantum property?",
                "options": ["The probability of measuring 0", "The physical hardware", "The relative phase (longitude on the Bloch sphere)", "The entanglement distance"],
                "answer": "The relative phase (longitude on the Bloch sphere)",
                "explanation": "$T_2$ scrambles the phase, ruining superpositions and destroying the interference patterns needed for algorithms to work."
            },
            {
                "q": "5. According to the laws of quantum physics, what is the strict relationship between $T_1$ and $T_2$ times?",
                "options": ["$T_2$ must always be exactly equal to $T_1$", "$T_2$ can never be greater than $2 \\times T_1$", "$T_1$ is always double $T_2$", "There is no relationship between them"],
                "answer": "$T_2$ can never be greater than $2 \\times T_1$",
                "explanation": "Because energy decay ($T_1$) inherently causes some phase loss, the pure dephasing time ($T_2$) is mathematically capped at twice the $T_1$ time."
            },
            {
                "q": "6. What is 'Depolarizing Noise' in physical quantum hardware?",
                "options": ["When the measurement laser misreads the qubit", "When the qubit gets too cold", "When an imperfect gate pulse replaces the qubit's state with random garbage data", "When two qubits get too close to each other"],
                "answer": "When an imperfect gate pulse replaces the qubit's state with random garbage data",
                "explanation": "Gate errors (depolarizing noise) occur when the microwave control pulses are slightly off, scrambling the intended rotation."
            },
            {
                "q": "7. On physical hardware, which types of quantum gates typically have a significantly higher error rate?",
                "options": ["1-qubit gates (like H or X)", "2-qubit gates (like CNOT)", "Measurement gates", "Identity gates"],
                "answer": "2-qubit gates (like CNOT)",
                "explanation": "Entangling two separate physical qubits via microwave pulses is highly complex and naturally much noisier than manipulating a single qubit."
            },
            {
                "q": "8. What occurs when a 'Readout Error' happens?",
                "options": ["The algorithm code fails to compile", "The measurement hardware misidentifies the physical state (e.g., reads a 1 as a 0)", "The qubit decays before it can be measured", "The quantum state refuses to collapse"],
                "answer": "The measurement hardware misidentifies the physical state (e.g., reads a 1 as a 0)",
                "explanation": "Readout errors mean the quantum operation was successful, but the final classical sensor simply made a mistake when looking at the result."
            },
            {
                "q": "9. Why can't we use standard classical error correction (like making simple backup copies of the data) on a quantum computer?",
                "options": ["Qubits are too expensive", "Classical computers don't have errors", "The No-Cloning Theorem forbids perfectly copying an unknown quantum state", "The QFT prevents it"],
                "answer": "The No-Cloning Theorem forbids perfectly copying an unknown quantum state",
                "explanation": "Because we cannot copy states, we must rely on entanglement and ancilla qubits to spread the information out redundantly."
            },
            {
                "q": "10. In Quantum Error Correction, how do we stretch the information of one logical qubit across multiple physical qubits?",
                "options": ["By applying a series of X gates", "By measuring it multiple times", "By using CNOT gates to entangle the data qubit with Ancilla (helper) qubits", "By running the circuit backwards"],
                "answer": "By using CNOT gates to entangle the data qubit with Ancilla (helper) qubits",
                "explanation": "CNOT gates allow us to encode the state of the primary data qubit into a larger, multi-qubit entangled system."
            },
            {
                "q": "11. How does the 3-qubit error correction circuit figure out if an error occurred without measuring the data?",
                "options": ["It guesses randomly", "It uses Parity Checks by comparing the data against the ancilla qubits", "It measures the data qubit anyway", "It pauses the decoherence timer"],
                "answer": "It uses Parity Checks by comparing the data against the ancilla qubits",
                "explanation": "By checking the relative differences (parity) between the qubits using CNOT gates, the circuit spots the anomaly without looking at the absolute values."
            },
            {
                "q": "12. In the 3-Qubit Bit-Flip code, what gate acts as a 'majority vote' to execute the final correction on the data qubit?",
                "options": ["The Hadamard gate", "The Pauli-Z gate", "The Toffoli (CCX) gate", "The SWAP gate"],
                "answer": "The Toffoli (CCX) gate",
                "explanation": "The Toffoli gate flips the data qubit back to its original state only if both ancilla qubits confirm that an error occurred on the data line."
            }
        ]

        # Quiz Logic
        for i, q in enumerate(quiz_data_l3):
            st.markdown(f"**{q['q']}**")
            ans = st.radio("Select an answer:", q["options"], key=f"quiz_l3_full_{i}", index=None, label_visibility="collapsed")
            if ans == q["answer"]:
                st.success(f"✅ **Correct!** {q['explanation']}")
            elif ans is not None:
                st.error("❌ **Incorrect.** Try reviewing the previous hardware and noise tabs!")
            st.write("")
# ==========================================
# PAGE VIEW: LEVEL 4 (Quantum Applications)
# ==========================================

def render_level_4():
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.visualization import plot_histogram, plot_state_qsphere
    from qiskit.quantum_info import Statevector
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    if st.button("⬅️ Back to Home"):
        navigate_to('home')
        st.rerun()
        
    st.divider()
    st.title("🧬 Level 4: Quantum Applications")
    st.write("Explore how quantum computers solve real-world problems in cryptography, chemistry, logistics, and AI.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔐 BB84 Cryptography", 
        "🧪 VQE Chemistry", 
        "🚚 QAOA Logistics", 
        "🤖 Quantum ML", 
        "📝 Quiz"
    ])

    # --- TAB 1: BB84 CRYPTOGRAPHY ---
    with tab1:
        st.markdown("### 🔐 Quantum Key Distribution (The BB84 Protocol)")
        st.write("Create an unhackable communication channel. If a hacker tries to intercept the key, the laws of quantum physics guarantee they will leave a permanent trace!")
        
        col_ui, col_sim = st.columns([1, 2])
        
        with col_ui:
            st.subheader("1. Protocol Setup")
            num_bits = st.slider("Number of Bits to Transmit", min_value=10, max_value=50, value=20)
            eve_present = st.toggle("🚨 Enable Eavesdropper (Eve)", value=False)
            
            if st.button("🚀 Run BB84 Protocol", type="primary"):
                # Simulate BB84 Protocol
                alice_bits = np.random.randint(2, size=num_bits)
                alice_bases = np.random.choice(['Z', 'X'], size=num_bits)
                bob_bases = np.random.choice(['Z', 'X'], size=num_bits)
                
                eve_bases = []
                bob_bits = []
                
                for i in range(num_bits):
                    bit = alice_bits[i]
                    basis = alice_bases[i]
                    
                    if eve_present:
                        e_basis = np.random.choice(['Z', 'X'])
                        eve_bases.append(e_basis)
                        if e_basis != basis:
                            current_bit = np.random.randint(2)
                        else:
                            current_bit = bit
                    else:
                        eve_bases.append("-")
                        current_bit = bit
                        
                    b_basis = bob_bases[i]
                    if b_basis != (eve_bases[i] if eve_present else basis):
                        bob_bits.append(np.random.randint(2))
                    else:
                        bob_bits.append(current_bit)
                
                df_bb84 = pd.DataFrame({
                    "Alice's Bit": alice_bits,
                    "Alice's Basis": alice_bases,
                    "Eve's Basis": eve_bases,
                    "Bob's Basis": bob_bases,
                    "Bob's Bit": bob_bits
                })
                
                df_bb84["Valid Key?"] = df_bb84["Alice's Basis"] == df_bb84["Bob's Basis"]
                valid_mask = df_bb84["Valid Key?"] == True
                df_bb84.loc[valid_mask, "Error Detected?"] = df_bb84["Alice's Bit"] != df_bb84["Bob's Bit"]
                df_bb84.loc[~valid_mask, "Error Detected?"] = "-"
                
                st.session_state.bb84_data = df_bb84
                
        with col_sim:
            st.subheader("2. Transmission Log")
            if 'bb84_data' in st.session_state:
                df = st.session_state.bb84_data
                st.dataframe(df, use_container_width=True)
                
                valid_keys = df[df["Valid Key?"] == True]
                error_count = valid_keys[valid_keys["Error Detected?"] == True].shape[0]
                error_rate = (error_count / valid_keys.shape[0]) * 100 if valid_keys.shape[0] > 0 else 0
                
                st.write(f"**Total Valid Key Bits Generated:** {valid_keys.shape[0]}")
                
                if eve_present:
                    st.error(f"🚨 **WARNING!** Error Rate is {error_rate:.1f}%. The theoretical threshold is ~25%. An eavesdropper has collapsed your wave functions! The key must be discarded.")
                else:
                    st.success(f"✅ **SECURE!** Error Rate is {error_rate:.1f}%. The quantum channel is safe. The key can be used to encrypt data.")
            else:
                st.info("Click 'Run BB84 Protocol' to simulate the quantum transmission.")
                
        st.divider()
        st.markdown("### 📚 The Mechanics of BB84")
        with st.expander("1. Encoding with Bases (Z and X)"):
            st.markdown(r"""
            Alice wants to send a secret key to Bob. She encodes each bit into a qubit, randomly choosing one of two "bases":
            * **The Z-Basis (Standard):** Uses $|0\rangle$ for `0`, and $|1\rangle$ for `1`.
            * **The X-Basis (Superposition):** Uses $|+\rangle$ for `0`, and $|-\rangle$ for `1`.
            
            Bob receives the qubits, but cannot copy them. He must randomly guess which basis to use for measurement. If he guesses correctly, he gets Alice's exact bit. If he guesses wrong, the state collapses and he gets a random 50/50 result.
            """)
        with st.expander("2. Sifting the Key"):
            st.markdown("""
            After all qubits are sent, Alice and Bob call each other on a public line. They only tell each other the *bases* they used (not the bits!). They throw away all bits where they used different bases. The remaining bits form the perfectly matching **Sifted Key**.
            """)
        with st.expander("3. Catching the Eavesdropper (Eve)"):
            
            st.markdown("""
            If Eve intercepts the qubits, she must measure them to read them. Since she doesn't know Alice's bases, she has to guess. When she guesses wrong, she physically alters the qubit (Wave Function Collapse). When she forwards the damaged qubit to Bob, Bob will sometimes measure the wrong bit, introducing a ~25% error rate that instantly alerts Alice and Bob!
            """)

    # --- TAB 2: VQE CHEMISTRY ---
    with tab2:
        st.markdown("### 🧪 Variational Quantum Eigensolver (VQE)")
        st.write("Act as the classical optimizer in a hybrid algorithm to find the ground state energy of a simulated molecule!")
        
        col_ui2, col_sim2 = st.columns([1, 2])
        
        with col_ui2:
            st.subheader("1. The Classical Optimizer")
            st.write("Adjust the parameterized angle $\\theta$ to rotate the quantum state and search for the lowest possible energy (the trough of the graph).")
            theta = st.slider("Ansatz Angle (θ)", 0.0, 2 * np.pi, 0.0, step=0.1)
            
            # Simulated Energy Landscape
            current_energy = -2.5 * np.cos(theta) + 1.2 * np.sin(theta) + 1.5
            
            st.metric(label="Calculated Energy (Hartrees)", value=f"{current_energy:.4f}")
            if current_energy < -1.2:
                st.success("🎉 You found the Ground State!")
                
        with col_sim2:
            st.subheader("2. The Energy Landscape")
            theta_vals = np.linspace(0, 2 * np.pi, 100)
            energy_vals = -2.5 * np.cos(theta_vals) + 1.2 * np.sin(theta_vals) + 1.5
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(theta_vals, energy_vals, label="Energy Landscape", color="blue")
            ax.plot(theta, current_energy, marker="o", markersize=10, color="red", label="Current Trial State")
            ax.set_xlabel("Ansatz Angle (θ)")
            ax.set_ylabel("Energy")
            ax.set_title("VQE Optimization Loop")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
            
            qc_vqe = QuantumCircuit(1)
            qc_vqe.ry(theta, 0)
            st.write("**Quantum Circuit (The Ansatz):**")
            st.pyplot(qc_vqe.draw(output='mpl'))

        st.divider()
        st.markdown("### 📚 The Mechanics of VQE")
        with st.expander("1. Why use Quantum Computers for Chemistry?"):
            st.markdown("""
            Simulating molecules is incredibly difficult for classical computers because the number of electron interactions grows exponentially. A quantum computer operates using the exact same quantum mechanical rules as the electrons themselves!
            """)
        with st.expander("2. The Hybrid Classical-Quantum Loop"):
            
            st.markdown(r"""
            VQE splits the workload:
            1. **The Quantum Computer** prepares a trial wave function (*Ansatz*) using parameterized gates (like $R_y(\theta)$) and measures its energy.
            2. **The Classical Computer** (acting as the optimizer) looks at the result, calculates a better angle for $\theta$, and sends it back.
            This loop repeats until it finds the Ground State.
            """)

    # --- TAB 3: QAOA LOGISTICS ---
    with tab3:
        st.markdown("### 🚚 Quantum Approximate Optimization Algorithm (QAOA)")
        st.write("Solve complex logistics problems, like finding the optimal way to divide a network (MaxCut), by using quantum interference to amplify the best solutions.")
        
        col_ui3, col_sim3 = st.columns([1, 2])
        
        with col_ui3:
            st.subheader("1. The MaxCut Problem")
            st.write("We have a simple 3-node network. The goal is to divide the nodes into two groups (Group 0 and Group 1) such that we cut the **maximum number of connecting lines**.")
            
            # Draw the 3-node graph using basic matplotlib
            fig_graph, ax_graph = plt.subplots(figsize=(4, 3))
            ax_graph.plot([0, 1, 2], [0, 1, 0], 'k-', lw=2) # Edges
            ax_graph.plot([0, 1, 2], [0, 1, 0], 'bo', markersize=20) # Nodes
            ax_graph.text(0, 0, 'Q0', color='white', ha='center', va='center', fontweight='bold')
            ax_graph.text(1, 1, 'Q1', color='white', ha='center', va='center', fontweight='bold')
            ax_graph.text(2, 0, 'Q2', color='white', ha='center', va='center', fontweight='bold')
            ax_graph.axis('off')
            st.pyplot(fig_graph)
            
            st.info("💡 **Optimal Solution:** The best cuts separate Q1 from both Q0 and Q2. Thus, the bitstrings `010` and `101` are the correct answers!")
            
            layers = st.slider("QAOA Layers (p)", min_value=1, max_value=3, value=1)
            
        with col_sim3:
            st.subheader("2. QAOA Circuit & Results")
            # Build QAOA Circuit
            qc_qaoa = QuantumCircuit(3)
            qc_qaoa.h([0, 1, 2])
            qc_qaoa.barrier()
            
            # Pre-optimized parameters for demonstration
            gamma, beta = 0.8, 0.4 
            
            for _ in range(layers):
                # Cost Hamiltonian (Edges: 0-1 and 1-2)
                qc_qaoa.cx(0, 1); qc_qaoa.rz(2 * gamma, 1); qc_qaoa.cx(0, 1)
                qc_qaoa.cx(1, 2); qc_qaoa.rz(2 * gamma, 2); qc_qaoa.cx(1, 2)
                qc_qaoa.barrier()
                # Mixer Hamiltonian
                qc_qaoa.rx(2 * beta, [0, 1, 2])
                qc_qaoa.barrier()
                
            qc_qaoa.measure_all()
            
            st.pyplot(qc_qaoa.draw(output='mpl'))
            
            counts_qaoa = AerSimulator().run(qc_qaoa, shots=1024).result().get_counts()
            st.success("Notice how the probability spikes for `010` and `101`! The algorithm amplified the correct answers.")
            st.pyplot(plot_histogram(counts_qaoa))

        st.divider()
        st.markdown("### 📚 The Mechanics of QAOA")
        with st.expander("1. What is MaxCut?"):
            
            st.markdown("""
            MaxCut is an NP-Hard problem used in logistics, clustering, and network design. You are given a graph of nodes and edges. You must color the nodes using two colors (e.g., Black and White) so that the maximum number of edges connect a Black node to a White node. In quantum computing, we represent the colors as `0` and `1`.
            """)
        with st.expander("2. The Cost and Mixer Hamiltonians"):
            st.markdown(r"""
            QAOA alternates between two operations (Hamiltonians):
            * **The Cost Hamiltonian:** Applies phase shifts based on the edges of the graph. It mathematically "rewards" states that represent good cuts by rotating their quantum phase.
            * **The Mixer Hamiltonian:** Applies $R_x$ gates to create interference. It mixes the probabilities, allowing the "rewarded" phases from the Cost step to constructively interfere, amplifying the probability of the correct answers.
            
            By increasing the number of layers ($p$), you give the algorithm more chances to amplify the right answer!
            """)

    # --- TAB 4: QUANTUM MACHINE LEARNING ---
    with tab4:
        st.markdown("### 🤖 Quantum Machine Learning (Feature Maps)")
        st.write("How do we feed classical data (like images or financial data) into a quantum computer? We encode it into the angles of qubits!")
        
        col_ui4, col_sim4 = st.columns([1, 2])
        
        with col_ui4:
            st.subheader("1. Classical Data Input")
            st.write("Input two classical data points (e.g., features of a dataset):")
            x1 = st.slider("Data Feature x1", 0.0, np.pi, 0.5)
            x2 = st.slider("Data Feature x2", 0.0, np.pi, 1.5)
            
        with col_sim4:
            st.subheader("2. Quantum Feature Map Circuit")
            
            # Build ZZ Feature Map manually for clear visualization
            qc_qml = QuantumCircuit(2)
            qc_qml.h([0, 1])
            qc_qml.barrier()
            
            # Encode single features
            qc_qml.rz(2 * x1, 0)
            qc_qml.rz(2 * x2, 1)
            qc_qml.barrier()
            
            # Entangle and encode correlated features
            qc_qml.cx(0, 1)
            qc_qml.rz(2 * x1 * x2, 1)
            qc_qml.cx(0, 1)
            
            st.pyplot(qc_qml.draw(output='mpl'))
            
            st.write("**Data Mapped to Quantum Hilbert Space:**")
            state_qml = Statevector.from_instruction(qc_qml)
            st.pyplot(plot_state_qsphere(state_qml))

        st.divider()
        st.markdown("### 📚 The Mechanics of Data Encoding")
        with st.expander("1. What is a Quantum Feature Map?"):
            
            st.markdown(r"""
            In classical Machine Learning, algorithms like Support Vector Machines (SVMs) use a "Kernel Trick" to map low-dimensional data into a higher dimension to make it easier to classify. 
            
            A **Quantum Feature Map** does this by using classical data ($x_1, x_2$) as the rotation angles for quantum gates. This maps standard data into a highly complex, multi-dimensional quantum state space (a Hilbert space) where quantum AI models can find hidden patterns that classical AI cannot see.
            """)
        with st.expander("2. The Role of Entanglement in AI"):
            st.markdown(r"""
            Notice the `CNOT` gates in the circuit. If we just encode $x_1$ on Qubit 0 and $x_2$ on Qubit 1, the data points remain independent. 
            
            By applying `CNOT` gates and an $R_z(2 x_1 x_2)$ rotation, we entangle the qubits. This allows the quantum computer to natively calculate the non-linear correlations and relationships *between* the data points, which is a massive advantage for complex AI tasks!
            """)

 # --- TAB 5: QUIZ ---
    with tab5:
        st.subheader("🧠 Level 4 Final Quiz")
        st.write("Test your knowledge of quantum cryptography, chemistry, logistics, and AI!")
        st.divider()
        
        quiz_data_l4 = [
            {
                "q": "1. In the BB84 protocol, which quantum principle prevents an eavesdropper (Eve) from secretly copying the qubits in transit?",
                "options": ["Phase Kickback", "The No-Cloning Theorem", "Thermal Relaxation", "Amplitude Amplification"],
                "answer": "The No-Cloning Theorem",
                "explanation": "The No-Cloning Theorem states that it is physically impossible to create an identical copy of an unknown quantum state, forcing Eve to measure (and potentially destroy) the original."
            },
            {
                "q": "2. What happens during the 'sifting' phase of the BB84 Quantum Key Distribution protocol?",
                "options": ["Alice and Bob publicly compare the bases they used and discard bits where they didn't match.", "Eve attempts to decrypt the key.", "Alice and Bob shout their secret bits over a public line.", "The quantum states are entangled."],
                "answer": "Alice and Bob publicly compare the bases they used and discard bits where they didn't match.",
                "explanation": "By comparing only the bases (Z or X) and not the 1s and 0s, they build a shared secret key without ever exposing the actual data."
            },
            {
                "q": "3. Why does Eve's presence in the BB84 protocol introduce a ~25% error rate into the sifted key?",
                "options": ["Her computer is too slow.", "Her measurements collapse the superpositions, physically altering the qubits before they reach Bob.", "She applies too many Hadamard gates.", "She causes T1 thermal relaxation."],
                "answer": "Her measurements collapse the superpositions, physically altering the qubits before they reach Bob.",
                "explanation": "When Eve guesses the wrong measurement basis, she collapses the wave function. When Bob receives that collapsed qubit, his own measurement becomes randomized."
            },
            {
                "q": "4. Why is the Variational Quantum Eigensolver (VQE) considered a 'hybrid' algorithm?",
                "options": ["It uses both qubits and classical bits.", "It uses a quantum computer to measure energy and a classical computer to optimize the parameters.", "It solves both chemistry and logistics problems.", "It works on both IBM and Google hardware."],
                "answer": "It uses a quantum computer to measure energy and a classical computer to optimize the parameters.",
                "explanation": "Because modern quantum computers are noisy, VQE offloads the heavy mathematical optimization to a classical CPU, using the QPU only to evaluate the complex wave functions."
            },
            {
                "q": "5. What is the primary goal of VQE in quantum chemistry?",
                "options": ["To factor large prime numbers.", "To encrypt chemical data.", "To find the ground state (lowest possible energy) of a molecule.", "To search an unsorted chemical database."],
                "answer": "To find the ground state (lowest possible energy) of a molecule.",
                "explanation": "Finding the lowest energy state allows chemists to simulate how molecules naturally form and interact without having to synthesize them in a lab."
            },
            {
                "q": "6. In VQE, what is the 'Ansatz'?",
                "options": ["The final measurement result.", "A parameterized trial wave function (circuit) whose angles are adjusted to find the minimum energy.", "The classical optimizer algorithm.", "The error correction code."],
                "answer": "A parameterized trial wave function (circuit) whose angles are adjusted to find the minimum energy.",
                "explanation": "The Ansatz is essentially the quantum computer's 'best guess' at the molecule's shape, which is continuously refined by rotating the parameterized gates."
            },
            {
                "q": "7. The Quantum Approximate Optimization Algorithm (QAOA) is typically used to solve which type of problems?",
                "options": ["Combinatorial optimization and logistics problems (like MaxCut).", "Factoring prime numbers.", "Simulating molecular bonds.", "Quantum Key Distribution."],
                "answer": "Combinatorial optimization and logistics problems (like MaxCut).",
                "explanation": "QAOA excels at finding near-optimal solutions to massive network, routing, and scheduling problems that are too complex for classical computers."
            },
            {
                "q": "8. In QAOA, what is the purpose of the Cost Hamiltonian?",
                "options": ["To measure the qubits.", "To apply phase shifts that mathematically 'reward' states representing good solutions.", "To scramble the data.", "To correct hardware errors."],
                "answer": "To apply phase shifts that mathematically 'reward' states representing good solutions.",
                "explanation": "The Cost Hamiltonian rotates the phase of the qubits based on the rules of the problem (like the edges in a graph), marking the best answers."
            },
            {
                "q": "9. How does increasing the number of layers (p) affect QAOA?",
                "options": ["It makes the algorithm run faster.", "It turns QAOA into Grover's search.", "It gives the algorithm more opportunities to create constructive interference, improving the accuracy.", "It forces the quantum state to collapse."],
                "answer": "It gives the algorithm more opportunities to create constructive interference, improving the accuracy.",
                "explanation": "More layers allow the Cost and Mixer Hamiltonians to finely tune the interference, causing the probability of the correct answer to spike higher."
            },
            {
                "q": "10. In Quantum Machine Learning (QML), what is the purpose of a Quantum Feature Map?",
                "options": ["To draw a physical map of the quantum chip.", "To encode classical data (like images or numbers) into the angles and phases of a quantum state.", "To decode quantum data back into classical data.", "To find the shortest path between two data points."],
                "answer": "To encode classical data (like images or numbers) into the angles and phases of a quantum state.",
                "explanation": "Feature maps translate standard classical datasets into rotations on the Bloch sphere, feeding the data into the quantum computer for processing."
            },
            {
                "q": "11. Why are CNOT (entangling) gates crucial in Quantum Feature Maps for AI?",
                "options": ["They allow the quantum computer to capture non-linear correlations and complex relationships between different classical data points.", "They make the circuit run faster.", "They prevent thermal relaxation.", "They measure the data automatically."],
                "answer": "They allow the quantum computer to capture non-linear correlations and complex relationships between different classical data points.",
                "explanation": "By entangling the qubits that hold the data, the quantum computer naturally evaluates how the different data features interact with one another."
            },
            {
                "q": "12. Which of the following is a major reason researchers are exploring quantum computers for Machine Learning?",
                "options": ["Quantum computers don't need electricity.", "Quantum Hilbert spaces offer exponentially large, complex dimensions that may classify dense data better than classical models.", "Quantum AI cannot make mistakes.", "Quantum computers are cheaper to build."],
                "answer": "Quantum Hilbert spaces offer exponentially large, complex dimensions that may classify dense data better than classical models.",
                "explanation": "The vast, multi-dimensional nature of quantum superposition gives AI models an incredibly rich environment to separate and classify complex patterns."
            }
        ]

        # Quiz Logic
        for i, q in enumerate(quiz_data_l4):
            st.markdown(f"**{q['q']}**")
            ans = st.radio("Select an answer:", q["options"], key=f"quiz_l4_full_{i}", index=None, label_visibility="collapsed")
            if ans == q["answer"]:
                st.success(f"✅ **Correct!** {q['explanation']}")
            elif ans is not None:
                st.error("❌ **Incorrect.** Try reviewing the application tabs to find the answer!")
            st.write("")
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
