import streamlit as st
import sympy as sp

# Page config
st.set_page_config(page_title="Matrix Diagonalizer", layout="centered")

# 🔥 FUTURISTIC CSS
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    background: -webkit-linear-gradient(#00f5ff, #00ff87);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #aaa;
    margin-bottom: 30px;
}

div[data-baseweb="input"] input {
    text-align: center;
    font-size: 18px;
    border-radius: 10px;
    border: 1px solid #00f5ff;
    background-color: #111;
    color: #00ffcc;
}

/* 🔥 CENTERED BIG BUTTON */
.center-button {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.stButton>button {
    border-radius: 15px;
    height: 60px;
    width: 300px;
    background: linear-gradient(90deg, #00f5ff, #00ff87);
    color: black;
    font-size: 22px;
    font-weight: bold;
}

.result-box {
    background: #111;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 25px rgba(0,255,255,0.3);
}
</style>
""", unsafe_allow_html=True)

# 🔥 Title
st.markdown('<div class="title">Matrix Diagonalizer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Exact Eigenvalues & Diagonalization Tool</div>', unsafe_allow_html=True)

# Info
with st.expander("ℹ️ What is Diagonalization?"):
    st.write("""
Diagonalization converts a matrix into:

A = P D P⁻¹

• D → Eigenvalues  
• P → Eigenvectors  

Used in engineering, physics, and advanced mathematics.
""")

# Size selection
size = st.selectbox("📐 Matrix Size", [2, 3, 4])

st.markdown("### 🔢 Input Matrix")

# Matrix input
matrix = []
for i in range(size):
    cols = st.columns(size)
    row = []
    for j in range(size):
        val = cols[j].text_input("", "0", key=f"{i}{j}")
        try:
            row.append(sp.sympify(val))
        except:
            row.append(0)
    matrix.append(row)

st.markdown("---")

# 🔥 CENTERED BUTTON
st.markdown('<div class="center-button">', unsafe_allow_html=True)
clicked = st.button("⚡ Diagonalize")
st.markdown('</div>', unsafe_allow_html=True)

# Compute
if clicked:
    try:
        A = sp.Matrix(matrix)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        st.subheader("🔷 Eigenvalues")
        eigenvals = A.eigenvals()
        for val, mult in eigenvals.items():
            st.latex(f"\\lambda = {sp.latex(val)} \\quad (x{mult})")

        P, D = A.diagonalize()

        st.success("✅ Matrix is diagonalizable")

        st.subheader("📌 Matrix P")
        st.latex(sp.latex(P))

        st.subheader("📌 Matrix D")
        st.latex(sp.latex(D))

        st.subheader("✔️ Verification")
        st.latex(sp.latex(P * D * P.inv()))

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception:
        st.error("❌ Matrix is not diagonalizable or input is invalid.")

# Footer
st.markdown("---")
st.caption("🚀 Developed by IT M 25-26 | Matrix Diagonalizer")
