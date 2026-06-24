import streamlit as st
import pandas as pd
import time
from generate_data import sync_docker_inventory

# Set up the browser layout parameters
st.set_page_config(layout="wide", page_title="SAP Cloud Ops Dashboard")

st.title("📊 SAP Cloud Fleet & Automation Dashboard")
st.markdown("---")

# 1. Read the generated infrastructure data
try:
    df = pd.read_csv('sap_nodes.csv')
except FileNotFoundError:
    st.warning("Data source file 'sap_nodes.csv' not found. Let's sync with Docker...")
    sync_docker_inventory()
    try:
        df = pd.read_csv('sap_nodes.csv')
    except FileNotFoundError:
        st.error("Still couldn't find the data. Make sure your Docker containers are running!")
        st.stop()

# 2. Sidebar Filters (User Controls)
st.sidebar.header("Filter Landscape")
cloud_filter = st.sidebar.multiselect("Cloud Provider", options=df['Cloud Provider'].unique(), default=df['Cloud Provider'].unique())
role_filter = st.sidebar.multiselect("System Role", options=df['Role'].unique(), default=df['Role'].unique())
status_filter = st.sidebar.multiselect("Health Status", options=df['Health Status'].unique(), default=df['Health Status'].unique())

# Filter dataset based on selections
filtered_df = df[
    (df['Cloud Provider'].isin(cloud_filter)) &
    (df['Role'].isin(role_filter)) &
    (df['Health Status'].isin(status_filter))
]

# 3. Global Ansible Control - NOW CONNECTED TO DOCKER
col_title, col_btn = st.columns([4, 1])
with col_title:
    st.subheader("Global Automation Controls")
with col_btn:
    if st.button("🔄 Sync All Nodes from Docker", use_container_width=True):
        with st.spinner("Connecting to Docker daemon & updating facts..."):
            sync_docker_inventory()
            time.sleep(1) # Brief pause so the user can read the spinner text
        st.success("Global facts refreshed across the fleet!")
        time.sleep(0.5)
        st.rerun() # Immediately refresh the UI with the new data

# 4. Top-Level Operational Metrics (KPIs)
st.markdown("### Operational Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_nodes = len(filtered_df)
critical_nodes = len(filtered_df[filtered_df['Health Status'] == 'Critical'])
pending_patches = filtered_df['Pending OS Patches'].sum()
expiring_certs = len(filtered_df[filtered_df['Cert Expiry (Days)'] < 30])

kpi1.metric("Total Monitored Nodes", total_nodes)
kpi2.metric("Critical Systems (Down)", critical_nodes, delta=f"{critical_nodes} require attention" if critical_nodes > 0 else "All Good", delta_color="inverse")
kpi3.metric("Total Pending Patches", pending_patches)
kpi4.metric("Certs Expiring < 30 Days", expiring_certs)

st.markdown("---")

# 5. Interactive Data Table
st.subheader("Fleet Inventory & Playbook Integration")

# Display a clean data table for the presentation
st.dataframe(
    filtered_df,
    column_config={
        "Pending OS Patches": st.column_config.NumberColumn(format="%d packages"),
        "Cert Expiry (Days)": st.column_config.NumberColumn(format="%d days left"),
        "Health Status": st.column_config.TextColumn()
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# 6. Presentation Action Sandbox (Targeted Playbook Execution)
st.subheader("Targeted Remediation Sandbox")
st.write("Select a target node from the filtered list to simulate targeted remediation playbooks.")

if not filtered_df.empty:
    target_system = st.selectbox("Select Target System ID", options=filtered_df['System ID'].unique())

    if target_system:
        selected_node = filtered_df[filtered_df['System ID'] == target_system].iloc[0]
        
        # Dynamic buttons appear based on system state
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Current Status:** {selected_node['Health Status']} | **Pending Patches:** {selected_node['Pending OS Patches']}")
        
        with col2:
            if selected_node['Pending OS Patches'] > 0:
                if st.button(f"🚀 Run batch_patch.yml on {target_system}", type="primary"):
                    with st.spinner(f"Running OS Patching on {target_system}..."):
                        time.sleep(2)
                    st.success(f"Successfully applied patches! {target_system} is now compliant.")
            
            if selected_node['Cert Expiry (Days)'] < 30:
                if st.button(f"🔒 Run check_cert_expiry.yml (Renew) on {target_system}"):
                    with st.spinner(f"Renewing SSL profile via Ansible..."):
                        time.sleep(2)
                    st.success(f"Certificates renewed for {target_system}.")