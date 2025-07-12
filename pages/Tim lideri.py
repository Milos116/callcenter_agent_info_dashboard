import pandas as pd
import streamlit as st
from pathlib import Path


def chosen_team(tl, book_path):
    """Function that is used to filter agents that are part of specifict team"""
    df = pd.read_excel(book_path)
    filt = (df["TL"] == tl) & (df["is_working"] == True)
    tl_df = df[filt]
    tl_df.reset_index(drop=True, inplace=True)
    tl_df.index = tl_df.index + 1
    tl_df.rename(columns={"Agent_name": "Članovi tima"}, inplace=True)
    st.write(tl_df["Članovi tima"])



# Database path
book_path = Path(__file__).parent.parent.resolve() / "data/book.xlsx"


# Page configuration
st.set_page_config(
    page_title="Tim Lideri", page_icon="📞", initial_sidebar_state="expanded"
)

# Background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d6e4f0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.header("Tim lideri 💻", divider="rainbow")

# Making DF out of TL excel sheet
tl_info_df = pd.read_excel(book_path, sheet_name="TL")

# List of all TL-s
lista_tl = tl_info_df["Tl_name"].values.tolist()

lista_tl.insert(0, "Izaberi TL-a")
selected_tl = st.selectbox(
    "Izbor tim lidera",
    [tl for tl in lista_tl],
    placeholder="Izaberi mesec",
    label_visibility="hidden",
)

if selected_tl != "Izaberi TL-a":
    # Filtering based on picked TL
    tl_filt = tl_info_df["Tl_name"] == selected_tl
    selected_tl_df = tl_info_df[tl_filt]
    # Taking info
    tl_info = selected_tl_df.squeeze()
    role = tl_info["Position"]
    city = tl_info["City"]
    phone_num = tl_info["Contact"]
    # Displaying info
    col_1, col_2 = st.columns(2)
    with col_1:
        st.markdown(
            f"""
        <div style='background-color:#FFFFFF; padding:20px; border-radius:10px; border:1px solid #ddd;'>
            <h4 style='margin-left:0px;'>{selected_tl}</h4>
            <p style='margin-left:0px; font-size:16px;'>{role}</p>
            <p style='margin-left:0px; font-size:16px;'>Kontakt centar - 🏙️{city}</p>
            <p style='margin-left:0px; font-size:16px;'>Broj telefona 📱: {phone_num}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    # Displaying team DF returned by chosen_team function
    with col_2:
        chosen_team(selected_tl, book_path)
