import streamlit as st
import pandas as pd
import time
import subprocess
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

# 3. Global Ansible Control
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

# 5. Interactive Data Table (NOW WITH COLOR CODING)
st.subheader("Fleet Inventory & Playbook Integration")

# Function to apply CSS styling to the Health Status column
def color_health_status(val):
    if val == 'Critical':
        return 'background-color: #ffcccc; color: #cc0000; font-weight: bold;'
    elif val == 'Warning':
        return 'background-color: #ffffcc; color: #b3b300; font-weight: bold;'
    elif val == 'Healthy':
        return 'background-color: #ccffcc; color: #008000; font-weight: bold;'
    return ''

# Apply the style to the dataframe. We use a try/except to handle different versions of Pandas
try:
    styled_df = filtered_df.style.map(color_health_status, subset=['Health Status'])
except AttributeError:
    styled_df = filtered_df.style.applymap(color_health_status, subset=['Health Status'])

# Display a clean data table for the presentation
st.dataframe(
    styled_df,
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
            if selected_node['Pending OS Patches'] > 0 or selected_node['Health Status'] == 'Critical':
                if st.button(f"🚀 Run Remediation Playbook on {target_system}", type="primary"):
                    
                    with st.spinner(f"Executing Ansible on {target_system}..."):
                        # 1. Format the target name (e.g. SAP-APP-05 to sap-app-05)
                        container_name = target_system.lower()
                        
                        # 2. Build the Ansible CLI command
                        ansible_cmd = f"ansible-playbook -i '{container_name},' remediate.yml"
                        
                        # 3. Execute the command and CAPTURE the output
                        result = subprocess.run(ansible_cmd, shell=True, capture_output=True, text=True)
                        
                        # 4. Check if Ansible succeeded (Return code 0 means success)
                        if result.returncode != 0:
                            st.error("❌ Ansible Playbook Failed!")
                            st.code(result.stderr or result.stdout, language='bash')
                            st.stop() # Stop the script so we don't pretend it succeeded
                        else:
                            st.success(f"✅ Successfully remediated {target_system}!")
                            with st.expander("View Ansible Execution Logs"):
                                st.code(result.stdout, language='yaml')
                        
                        # 5. Re-sync the Docker state so the dashboard updates
                        sync_docker_inventory()
                        
                    time.sleep(1.5)
                    st.rerun()