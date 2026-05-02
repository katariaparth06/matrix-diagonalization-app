import streamlit as st
import sympy as sp

st.set_page_config(page_title="Matrix Diagonalizer", layout="centered")

if "computed" not in st.session_state:
    st.session_state.computed = False

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp { background-color: #0f172a; color: white; }

.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    background: -webkit-linear-gradient(#00f5ff, #00ff87);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle { text-align: center; color: #aaa; }

div[data-baseweb="input"] input {
    text-align: center;
    border-radius: 10px;
    border: 1px solid #00f5ff;
    background-color: #111;
    color: #00ffcc;
}

/* disable autofill */
input { autocomplete: off !important; }

.stButton>button {
    width: 100%;
    height: 75px;
    border-radius: 14px;
    background: linear-gradient(90deg, #00f5ff, #00ff87);
    color: black;
    font-size: 20px;
    font-weight: bold;
}

.result-box {
    background: #111;
    padding: 20px;
    border-radius: 12px;
    margin-top: 10px;
}

.section-title {
    font-size: 20px;
    margin-top: 10px;
    color: #00f5ff;
}

.matrix-label {
    text-align:center;
    font-size:12px;
    color:#00f5ff;
}

.matrix-bracket {
    color:#00f5ff;
    text-align:center;
    font-size:26px;
    text-shadow: 0 0 8px #00f5ff;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="title">Matrix Diagonalizer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Exact Eigenvalues • Fractions • Roots Supported</div>', unsafe_allow_html=True)

# ---------- INSTRUCTIONS ----------
with st.expander("ℹ️ Input Instructions"):
    st.markdown("""
✨ **Fractions** → `1/2`  
✨ **Square roots** → `sqrt(2)`  
✨ **Mixed** → `1/2 + sqrt(3)`  
✨ **Decimals** → `0.5`  
""")

# ---------- MATRIX ----------
size = st.selectbox("📐 Matrix Size", [2,3,4])  # ✅ restored 4x4
st.markdown("### 🔢 Enter Matrix")

def lb(i,n): return "⎡" if i==0 else "⎣" if i==n-1 else "⎢"
def rb(i,n): return "⎤" if i==0 else "⎦" if i==n-1 else "⎥"

def clean(expr):
    if not expr: return "0"
    return expr.replace("√","sqrt").replace("^","**")

matrix=[]
for i in range(size):
    cols_main = st.columns([1,8,1])

    with cols_main[0]:
        st.markdown(f"<div class='matrix-bracket'>{lb(i,size)}</div>", unsafe_allow_html=True)

    with cols_main[1]:
        cols = st.columns(size)
        row=[]
        for j in range(size):
            cols[j].markdown(f"<div class='matrix-label'>a{i+1}{j+1}</div>", unsafe_allow_html=True)

            val = cols[j].text_input("", key=f"{i}{j}", label_visibility="collapsed", placeholder="")

            try:
                row.append(sp.sympify(clean(val)))
            except:
                row.append(0)

        matrix.append(row)

    with cols_main[2]:
        st.markdown(f"<div class='matrix-bracket'>{rb(i,size)}</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------- BUTTON ----------
clicked = st.button("DIAGONALIZE")

if clicked:
    try:
        A = sp.Matrix(matrix)

        lam = sp.symbols('λ')
        char_poly = (A - lam*sp.eye(A.shape[0])).det()
        eigenvals = sp.solve(char_poly, lam)

        eigen_data = []
        vectors = []

        for val in eigenvals:
            M = A - val*sp.eye(A.shape[0])
            basis = M.nullspace()

            if not basis:
                raise Exception("Eigenvector calculation failed")

            eigen_data.append((val, basis))
            vectors.extend(basis)

        if len(vectors) < A.shape[0]:
            raise Exception("Matrix is NOT diagonalizable")

        P = sp.Matrix.hstack(*vectors[:A.shape[0]])
        D = sp.simplify(P.inv() * A * P)

        st.session_state.A = A
        st.session_state.eigen_data = eigen_data
        st.session_state.P = P
        st.session_state.D = D
        st.session_state.computed = True

    except Exception as e:
        st.error(f"❌ {str(e)}")
        st.session_state.computed = False

# ---------- RESULTS ----------
if st.session_state.computed:

    A = st.session_state.A
    P = st.session_state.P
    D = st.session_state.D
    eigen_data = st.session_state.eigen_data

    mode = st.radio("🔁 Answer Format", ["Exact","Decimal"])

    def fmt(x):
        return x.evalf(5) if mode=="Decimal" else sp.simplify(x)

    tab1, tab2 = st.tabs(["📊 Fundamental Results","📄 Mathematical Proof"])

    with tab1:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Eigenvalues</div>', unsafe_allow_html=True)
        for i,(val,_) in enumerate(eigen_data,1):
            st.latex(f"\\lambda_{i} = {sp.latex(fmt(val))}")

        st.markdown('<div class="section-title">Matrix P</div>', unsafe_allow_html=True)
        st.latex(sp.latex(fmt(P)))

        st.markdown('<div class="section-title">Matrix D</div>', unsafe_allow_html=True)
        st.latex(sp.latex(fmt(D)))

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        lam = sp.symbols('λ')

        st.markdown('<div class="section-title">Characteristic Equation</div>', unsafe_allow_html=True)
        st.latex("det(A-\\lambda I)=0")

        I = sp.eye(A.shape[0])

        st.markdown("Step 1: Identity Matrix I")
        st.latex(sp.latex(I))

        st.markdown("Step 2: λI")
        st.latex(sp.latex(lam * I))

        st.markdown("Step 3: A - λI")
        M = A - lam*I
        st.latex(sp.latex(A) + " - " + sp.latex(lam * I))
        st.latex(sp.latex(M))

        det = sp.expand(M.det())
        st.latex(sp.latex(det))
        st.latex(f"{sp.latex(det)}=0")

        st.markdown('<div class="section-title">Eigenvectors</div>', unsafe_allow_html=True)
        st.markdown("Using formula:")
        st.latex("(A - \\lambda I)\\mathbf{x} = 0")

        for idx,(val,basis) in enumerate(eigen_data,1):
            st.markdown(f"**Eigenvalue λ{idx} = {sp.latex(val)}**")

            st.markdown("Step: Construct (A - λI)")
            I = sp.eye(A.shape[0])
            M = A - val*I
            st.latex(sp.latex(A) + " - " + sp.latex(val*I))
            st.latex(sp.latex(M))

            x = sp.symbols(f'x1:{A.shape[0]+1}')
            eqs = M*sp.Matrix(x)

            for eq in eqs:
                if eq != 0:
                    st.latex(sp.latex(eq)+"=0")

            st.markdown("Row Reduction:")
            rref,_ = M.rref()
            st.latex(sp.latex(rref))

            st.markdown("Eigenvector:")
            for v in basis:
                st.latex(sp.latex(fmt(v)))

        st.markdown('<div class="section-title">Verification: D = P⁻¹AP</div>', unsafe_allow_html=True)

        Pinv = P.inv()
        AP = A*P
        final = Pinv*AP

        st.markdown("Step 1: P⁻¹")
        st.latex(sp.latex(fmt(Pinv)))

        st.markdown("Step 2: A·P")
        st.latex(sp.latex(fmt(AP)))

        st.markdown("Step 3: P⁻¹(AP)")
        st.latex(sp.latex(Pinv) + " \\cdot " + sp.latex(AP))
        st.latex(sp.latex(fmt(final)))

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🚀 Developed by IT-M FYBTech | Matrix Diagonalizer")
