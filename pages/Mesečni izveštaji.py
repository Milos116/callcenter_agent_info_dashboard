from pathlib import Path
import pandas as pd
import streamlit as st


# Gets list of all report files in directory
report_path = Path(__file__).parent.parent.resolve() / "data/Mesečni"
file_names = [f.name for f in report_path.glob("*.xlsx")]

# Dict used for maping
month_order = {
    "Januar": 1,
    "Februar": 2,
    "Mart": 3,
    "April": 4,
    "Maj": 5,
    "Jun": 6,
    "Jul": 7,
    "Avgust": 8,
    "Septembar": 9,
    "Oktobar": 10,
    "Novembar": 11,
    "Decembar": 12,
}
# Function used to sort months
sorted_file_names = sorted(
    file_names, key=lambda x: month_order[x.split()[0]], reverse=True
)

# Inseting as first index plase holder value "Choose Month"
sorted_file_names.insert(0, "Izaberi mesec 📅")

# Page configs
st.set_page_config(
    page_title="Mesečni izveštaji", page_icon="📞", initial_sidebar_state="expanded"
)

# Page backgrounnd color
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
st.header("Mesečni izveštaji :clipboard:", divider="rainbow")

# Select box for picking out report from list
selected_month = st.selectbox(
    "Izbor meseca",
    [f.split(".")[0] for f in sorted_file_names],
    placeholder="Izaberi mesec",
    label_visibility="hidden",
)


if selected_month != "Izaberi mesec 📅":
    df = pd.read_excel(
        report_path / f"{selected_month}.xlsx"
    )  # Takes report and turns it into DF
    df.index = df.index + 1
    styled_df = df[
        [
            "Name",
            "Score QM",
            "Score TL",
            "Final Score",
            "Review Num. QM",
            "Review Num. TL",
        ]
    ].style.format(
        {"Score QM": "{:.2%}", "Score TL": "{:.2%}", "Final Score": "{:.2%}"}
    )
    # Displays formated report DF
    st.dataframe(styled_df)
