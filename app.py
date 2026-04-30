import streamlit as st
import sympy as sp

# Page config
st.set_page_config(page_title="Matrix Diagonalization Tool", layout="centered")

# Custom styling
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #4CAF50;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: gray;
    margin-bottom: 20px;
}
.matrix-input input {
    text-align: center;
    font-size: 16px;
}
.result-box {
    background-color: #111;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">Matrix Diagonalization Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find Eigenvalues and Diagonalize Matrices Easily</div>', unsafe_allow_html=True)

# Info section
with st.expander("ℹ️ What is Diagonalization?"):
    st.write("""
Diagonalization is the process of converting a matrix into a diagonal matrix.
It simplifies complex matrix operations and is widely used in engineering, physics, and data science.

A matrix A is diagonalizable if:
A = P D P⁻¹

Where:
- D is a diagonal matrix (contains eigenvalues)
- P contains eigenvectors
""")

# Select size
size = st.selectbox("📏 Select Matrix Size", [2, 3, 4])

st.markdown("### ✏️ Enter Matrix Values")

# Matrix input
matrix = []
for i in range(size):
    cols = st.columns(size)
    row = []
    for j in range(size):
        val = cols[j].text_input(f"a{i+1}{j+1}", "0", key=f"{i}{j}")
        try:
            row.append(sp.sympify(val))
        except:
            row.append(0)
    matrix.append(row)

st.markdown("---")

# Compute button
if st.button("🚀 Compute Diagonalization"):
    try:
        A = sp.Matrix(matrix)

        st.markdown("## 📊 Results")

        # Eigenvalues
        eigenvals = A.eigenvals()
        st.subheader("🔢 Eigenvalues")
        for val, mult in eigenvals.items():
            st.latex(f"\\lambda = {sp.latex(val)} \\quad (multiplicity\\ {mult})")

        # Diagonalization
        P, D = A.diagonalize()

        st.success("✅ Matrix is diagonalizable!")

        # Matrix P
        st.subheader("📌 Matrix P")
        st.latex(sp.latex(P))

        # Matrix D
        st.subheader("📌 Matrix D")
        st.latex(sp.latex(D))

        # Verification
        st.subheader("✔️ Verification (A = P D P⁻¹)")
        st.latex(sp.latex(P * D * P.inv()))

    except Exception:
        st.error("❌ Matrix is not diagonalizable or input is invalid.")

# Footer
st.markdown("---")
st.caption("Developed by Parth | Matrix Diagonalization Project 🚀")