import streamlit as st
import sympy as sp

st.set_page_config(page_title="Matrix Diagonalizer", layout="centered")

# 🔁 SESSION STATE INIT (ADDED)
if "computed" not in st.session_state:
    st.session_state.computed = False

# 🔥 FORCE DARK + ORIGINAL COLOR SCHEME
st.markdown("""
<style>

/* 🔥 FORCE DARK BACKGROUND */
.stApp {
    background-color: #0f172a;
    color: white;
}

/* Title */
.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    background: -webkit-linear-gradient(#00f5ff, #00ff87);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #aaa;
    margin-bottom: 20px;
}

/* Inputs */
div[data-baseweb="input"] input {
    text-align: center;
    border-radius: 10px;
    border: 1px solid #00f5ff;
    background-color: #111;
    color: #00ffcc;
    font-size: 16px;
}

/* 🔥 BUTTON (ENHANCED BUT SAME STYLE) */
.stButton>button {
    width: 100%;
    height: 90px;
    border-radius: 16px;
    background: linear-gradient(90deg, #00f5ff, #00ff87);
    color: black;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 3px;
    border: none;
    box-shadow: 0 10px 25px rgba(0, 255, 200, 0.25);
    transition: all 0.25s ease-in-out;
}

.stButton>button:hover {
    transform: scale(1.03);
}

.stButton>button:active {
    transform: scale(0.98);
}

/* Result box */
.result-box {
    background: #111;
    padding: 20px;
    border-radius: 12px;
    margin-top: 10px;
}

/* Section titles */
.section-title {
    font-size: 20px;
    margin-top: 10px;
    color: #00f5ff;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">Matrix Diagonalizer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Exact Eigenvalues • Fractions • Roots Supported</div>', unsafe_allow_html=True)

# Input Instructions (UNCHANGED)
with st.expander("ℹ️ Input Instructions"):
    st.write("""
You can enter:

• Fractions → `1/2`, `3/4`  
• Square roots → `sqrt(2)`, `sqrt(5)`  
• Mixed → `1/2 + sqrt(3)`  
• Decimals → `0.5`, `1.25`  

Examples:
- 1/2  
- sqrt(2)  
- 3 + sqrt(5)  
""")

# Matrix size
size = st.selectbox("📐 Matrix Size", [2, 3, 4])

st.markdown("### 🔢 Enter Matrix")

# Matrix input
matrix = []
for i in range(size):
    cols = st.columns(size)
    row = []
    for j in range(size):
        val = cols[j].text_input("", "0", key=f"{i}{j}")

        try:
            parsed = sp.sympify(val)
            if parsed.is_Float:
                parsed = sp.nsimplify(parsed)
            row.append(parsed)
        except:
            row.append(0)

    matrix.append(row)

st.markdown("---")

# Button
col1, col2, col3 = st.columns([0.1, 8, 0.1])
with col2:
    clicked = st.button("DIAGONALIZE")

# 🔁 STORE RESULTS (ADDED, NO STRUCTURE CHANGE)
if clicked:
    try:
        A = sp.Matrix(matrix)
        eigenvals = A.eigenvals()
        P, D = A.diagonalize()

        st.session_state.A = A
        st.session_state.P = P
        st.session_state.D = D
        st.session_state.eigenvals = eigenvals
        st.session_state.computed = True

    except Exception:
        st.error("❌ Matrix is not diagonalizable or input is invalid.")
        st.session_state.computed = False

# 🔁 SHOW RESULTS WITHOUT RESET
if st.session_state.computed:

    A = st.session_state.A
    P = st.session_state.P
    D = st.session_state.D
    eigenvals = st.session_state.eigenvals

    # 🔁 TOGGLE (AFTER CLICK ONLY)
    mode = st.radio("🔁 Answer Format", ["Exact (Fractions / Roots)", "Decimal (Approx)"], key="mode_toggle")

    # 🔧 FORMAT FUNCTIONS
    def format_expr(expr):
        expr = sp.simplify(expr)
        return expr.evalf(6) if "Decimal" in mode else sp.nsimplify(expr)

    def format_matrix(M):
        M = sp.simplify(M)
        return M.evalf(6) if "Decimal" in mode else sp.nsimplify(M)

    tab1, tab2 = st.tabs(["📊 Fundamental Results", "📄 Mathematical Proof"])

    with tab1:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Eigenvalues</div>', unsafe_allow_html=True)

        for val, mult in eigenvals.items():
            val = format_expr(val)
            if mult == 1:
                st.latex(f"\\lambda = {sp.latex(val)}")
            else:
                st.latex(f"\\lambda = {sp.latex(val)} \\quad (multiplicity\\ {mult})")

        st.markdown('<div class="section-title">Matrix P</div>', unsafe_allow_html=True)
        st.latex(sp.latex(format_matrix(P)))

        st.markdown('<div class="section-title">Matrix D</div>', unsafe_allow_html=True)
        st.latex(sp.latex(format_matrix(D)))

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        # ORIGINAL PROOF KEPT
        st.markdown("### The central proof of diagonalization:")
        st.write("A matrix **A** is diagonalizable if:")
        st.latex("A = P D P^{-1}")

        # 🔥 ADDITION (CORRECT VERIFICATION)
        st.markdown("### Equivalent form:")
        st.latex("D = P^{-1} A P")

        colA, colB = st.columns(2)

        with colA:
            st.markdown("**Matrix A:**")
            st.latex(sp.latex(format_expr(A)))

        with colB:
            st.markdown("**P D P⁻¹:**")
            st.latex(sp.latex(format_expr(P * D * P.inv())))

        # 🔥 STEP-BY-STEP ADDITION
        st.markdown("### Step-by-step verification:")

        P_inv = P.inv()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**P⁻¹**")
            st.latex(sp.latex(format_expr(P_inv)))

        with col2:
            st.markdown("**A · P**")
            st.latex(sp.latex(format_expr(A * P)))

        with col3:
            st.markdown("**P⁻¹ (A P)**")
            st.latex(sp.latex(format_expr(P_inv * A * P)))

        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🚀 Developed by IT-M FYBTech | Matrix Diagonalizer")
