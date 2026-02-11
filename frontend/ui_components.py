import streamlit as st

def inject_css():
    st.markdown("""
        <style>
        /* Main container */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        /* Page titles */
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }

        /* Card style */
        .card {
            background-color: #1f2937;
            padding: 20px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 20px;
        }

        /* KPI number */
        .kpi {
            font-size: 28px;
            font-weight: 700;
            margin-top: 8px;
        }

        /* Buttons */
        .stButton button {
            border-radius: 10px !important;
            padding: 0.6rem 1rem !important;
        }

        /* Dataframe border */
        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.08);
        }

        </style>
    """, unsafe_allow_html=True)



def card_start(title):
    st.markdown(f"<div class='card'><h3>{title}</h3>", unsafe_allow_html=True)


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def kpi_card(title, value):
    st.markdown(f"""
        <div class='card'>
            <h4>{title}</h4>
            <div class='kpi'>{value}</div>
        </div>
    """, unsafe_allow_html=True)


def empty_state(msg):
    st.info(msg)


def show_error(e):
    st.error(str(e))
