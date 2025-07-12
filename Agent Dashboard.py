from pathlib import Path
import streamlit as st
from streamlit_searchbox import st_searchbox
import pandas as pd
from report_sorter import get_sorted_reports


def display_info_column(column_title, column_info):
    """Function to display agent basic information"""
    with st.container():
        st.markdown(
            f"""
				<div style='
					background-color:#f9f9f9;
					padding:19px;
					border-radius:15px;
					display:flex;
					gap:15px;
					align-items:center;'>
					<div>
						<h6 style='margin-bottom:5px;'>{column_title}</h6>
						<p style='margin:0; font-size:15px;'>
							{column_info}
						</p>
						<p style='font-size:12px; color:gray;'></p>
					</div>
				</div>
				""",
            unsafe_allow_html=True,
        )


def monitoring_score(label, value, delta, bg_color="#f9f9f9"):
    """Function to display score results"""
    st.markdown(
        f"""
		<div style='
			background-color:{bg_color};
			padding: 20px;
			border-radius: 15px;
			border: 1px solid #ddd;
			text-align: center;
			font-family: sans-serif;
		'>
			<div style='font-size: 14px; font-weight: bold; margin-bottom: 5px;'>{label}</div>
			<div style='font-size: 14px; '>{value}</div>
			<div style='font-size: 12px; color: {"green" if "-" not in delta else "red"};'>{delta}</div>
		</div>
		""",
        unsafe_allow_html=True,
    )


def search_agents(search_term):
    """Helper function for use in st_searchbox"""
    return [a for a in agents_list if search_term.lower() in a.lower()]


def load_month_df(file_names, base_path):
    "Function that merges L1, L2 and night shift DF into for displaying purposes"
    dfs = [pd.read_excel(base_path / f"data/Mesečni/{name}") for name in file_names]
    return pd.concat(dfs)


# Script path
path = Path(__file__).parent.resolve()

# Paths to other files
database_path = path / "data/book.xlsx"
agents_df = pd.read_excel(database_path)

# List of all agents used for search_agents function
agents_list = agents_df["Agent_name"].to_list()


# Page config settings
st.set_page_config(
    page_title="Agent Dashboard", page_icon="📞", initial_sidebar_state="expanded"
)


# Page background color
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
st.header("Agent Dashboard 🎧", divider="rainbow")

# Storing results in selected_agent by using searchbox
selected_agent = st_searchbox(search_agents, key="agent_search")

# If there is selected_agent variable display further info
if selected_agent:

    # Setting DF filter in order to get all info about selected agent
    filt = agents_df["Agent_name"] == selected_agent
    # Turning that info from data series to basic list
    agent_info = agents_df[filt].squeeze()

    # All gathered "basic info"
    agent_name = agent_info["Agent_name"]
    agent_role = agent_info["Position"]
    city = agent_info["City"]
    agent_mentor = agent_info["Mentor"]
    contact_number = agent_info["Contact"]
    qm = agent_info["QM"]
    tl = agent_info["TL"]
    img_link = path / agent_info["Image"]

    # Formating date if it exists
    if pd.notnull(agent_info["Join_date"]):
        unformated_date = agent_info["Join_date"]
        join_date = unformated_date.strftime("%d.%m.%Y")
    else:
        join_date = " / "

    # Setting up columns for image and basic info
    (
        img_col,
        name_col,
    ) = st.columns(2, border=False)

    # Image column
    with img_col:
        st.image(img_link.resolve(), width=170)

    # Basic info column
    with name_col:
        st.markdown(
            f"""
		
			<h4 style='margin-left:0px;'>{agent_name}</h4>
			<p style='margin-left:0px; font-size:18px;'>{agent_role}</p>
			<p style='margin-left:0px; font-size:16px;'>Kontakt centar - 🏙️ {city}</p>
			<p style='margin-left:0px; font-size:16px;'>Broj telefona: 📱 {contact_number}</p>
		</div>
		""",
            unsafe_allow_html=True,
        )

        # Checking if agent has any special status and adding badge if he has
        special_status = (agents_df.loc[filt, "Poseban status"]).iloc[0]
        if pd.notnull(special_status):
            st.badge(f"{special_status}", color="green")

        # Checking if agent is still active if not adding badge
        if not agent_info["is_working"]:
            st.badge("Raskinut ugovor ili PO❌", color="red")

        # Header for next row of columnns
        st.header("", divider="rainbow")

    # Columns that indicate Join date, Mentor, TL and QM
    date_col, mentor_col, tl_col, qm_col = st.columns(4)

    with date_col:
        display_info_column("Početak rada", join_date)

    with mentor_col:
        display_info_column("Mentor", agent_mentor)

    with tl_col:
        display_info_column("Tim lider", tl)

    with qm_col:
        display_info_column("QM", qm)
        
	# Returns sorted by month list of all reports
    report_list = get_sorted_reports()
	# Gets combined DF of previes month L1, L2 and night shift
    complete_last_month_df = load_month_df(report_list[-3:], path)
	# Gets combined DF of month before previous L1, L2 and night shift
    complete_df_2_month_ago = load_month_df(report_list[-6:-3], path)

	# Display Score info if agent was graded in specific month
    if selected_agent in complete_last_month_df["Name"].values:

        st.subheader(f"Monitoring - {report_list[-1].split("-")[0]}", divider="rainbow")

        agent_filter = complete_last_month_df["Name"] == selected_agent.strip()

        agent_row = complete_last_month_df[agent_filter].values.tolist()

        qm_score = agent_row[0][3]
        tl_score = agent_row[0][4]
        total_score = agent_row[0][5]

        qm_score_col, tl_score_col, total_score_col = st.columns(3)

        with qm_score_col:
            monitoring_score("Ocena QM", "{:.1%}".format(qm_score), "")
        with tl_score_col:
            monitoring_score("Ocena TL", "{:.1%}".format(tl_score), "")
        with total_score_col:
            monitoring_score("Konačna ocena", "{:.1%}".format(total_score), "")
	# Display Score info if agent was graded in specific month
    if selected_agent in complete_df_2_month_ago["Name"].values:
        st.subheader(f"Monitoring - {report_list[-4].split("-")[0]}", divider="rainbow")

        agent_filter_2 = complete_df_2_month_ago["Name"] == selected_agent.strip()

        agent_row_2 = complete_df_2_month_ago[agent_filter_2].values.tolist()

        qm_score_2 = agent_row_2[0][3]
        tl_score_2 = agent_row_2[0][4]
        total_score_2 = agent_row_2[0][5]

        qm_score_col_2, tl_score_col_2, total_score_col_2 = st.columns(3)

        with qm_score_col_2:
            monitoring_score("Ocena QM", "{:.1%}".format(qm_score_2), "")
        with tl_score_col_2:
            monitoring_score("Ocena TL", "{:.1%}".format(tl_score_2), "")
        with total_score_col_2:
            monitoring_score("Konačna ocena", "{:.1%}".format(total_score_2), "")
