import pandas as pd
import streamlit as st
from pathlib import Path
import datetime


def display_filtered_df(pozicija, df):
    """Displays formated DF based on specific filter"""

    pos_filter = df["Position"] == pozicija
    is_working_filter = df["is_working"] == True

    new_df = df[pos_filter & is_working_filter]
    new_df.reset_index(drop=True, inplace=True)
    new_df.index = new_df.index + 1

    new_df = new_df.rename(
        columns={"Agent_name": "Ime", "Join_date": "Početak rada", "City": "Grad"}
    )
    st.dataframe(new_df[["Ime", "Početak rada", "Grad", "QM", "TL"]])



book_path = Path(__file__).parent.parent.resolve() / "data/book.xlsx"

agent_list = pd.read_excel(book_path)
# Format time string
agent_list["Join_date"] = agent_list["Join_date"].dt.strftime("%d-%m-%Y")


st.set_page_config(
    page_title="Lista agenata", page_icon="📞", initial_sidebar_state="expanded"
)


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

st.header("Liste agenata🧾", divider="rainbow")

select_box_lista = [
    "Izaberi listu 🧾",
    "Agenti ulaznih poziva 🎧",
    "Agenti tehničke podrške ⚙️",
    "Agenti noćne smene 🌑",
    "Mentori/Buddy 👩‍🏫",
    "Novi agenti 🌟",
]

izbor = st.selectbox("Izbor listi", select_box_lista, label_visibility="hidden")

# L1
if izbor == select_box_lista[1]:

    display_filtered_df("Agent ulaznih poziva", agent_list)

# L2
elif izbor == select_box_lista[2]:

    display_filtered_df("Napredna podrška", agent_list)

# Noćna
elif izbor == select_box_lista[3]:

    display_filtered_df("Agent noćne smene", agent_list)

# List of agents that have mentor or buddy status
elif izbor == select_box_lista[4]:

    mentor_filter = agent_list["Poseban status"] == "Mentor"
    buddy_filter = agent_list["Poseban status"] == "Buddy"
    lista_b_m = agent_list[mentor_filter | buddy_filter].reset_index(drop=True)

    mentor_buddy_list = lista_b_m["Agent_name"].tolist()

    final_df = pd.DataFrame()

    for mentor in mentor_buddy_list:

        ucenik_filter = (agent_list["Mentor"]) == mentor
        ucenik_df = agent_list[ucenik_filter].tail(1)
        final_df = pd.concat([final_df, ucenik_df])

    final_df = final_df.rename(
        columns={"Agent_name": "Poslednji učenik", "Join_date": "Prvi dan rada"}
    )
    final_df.reset_index(drop=True, inplace=True)
    final_df.index = final_df.index + 1

    st.dataframe(final_df[["Mentor", "Poslednji učenik", "Prvi dan rada"]])

# New agents ( agents that joined 60 or less day ago)
elif izbor == select_box_lista[5]:

    date_now = datetime.datetime.today()
    delta_date = datetime.timedelta(days=60)
    days = date_now - delta_date

    agent_list = pd.read_excel(book_path)
    date_filter = agent_list["Join_date"] > days

    new_agents_df = agent_list[date_filter]
    new_agents_df.reset_index(drop=True, inplace=True)
    new_agents_df.index = new_agents_df.index + 1

    new_agents_df["Join_date"] = new_agents_df["Join_date"].dt.strftime("%d-%m-%Y")
    new_agents_df = new_agents_df.rename(
        columns={"Agent_name": "Ime", "Join_date": "Početak rada"}
    )
    st.dataframe(new_agents_df[["Ime", "Početak rada", "Mentor", "QM", "TL"]])
