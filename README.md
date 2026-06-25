# SAP Cloud Operations & Automation Dashboard

This prototype is designed to visualize and manage a massive SAP cloud landscape (AWS, Azure, GCP) by integrating infrastructure monitoring with actionable Ansible automation.

# Overview

Managing an enterprise-grade SAP landscape (Virtual Machines, HANA DBs, Web-dispatchers) across multiple hyperscalers requires an exception-based monitoring approach. This dashboard filters out the noise, highlighting systems that require human intervention for:

System Health: Identifying offline or critical nodes.

OS Patch Compliance: Tracking pending package updates across the fleet.

Certificate Management: Highlighting SSL/SSO certificates approaching expiration.

Automation Sync: Tracking the success/failure rate of backend Ansible playbooks.

# Features

Dynamic Mock Data Generation: Instantly spin up a realistic dataset of SAP nodes using lightweight Docker containers to simulate enterprise environments.

Live Filtering: Drill down by Cloud Provider, System Role, and Health Status.

Actionable UIs: Remediation buttons demonstrating how UI elements trigger targeted Ansible playbooks directly against the container infrastructure.

Instant KPIs: High-visibility metrics for Total Nodes, Critical Systems, Pending Patches, and Expiring Certs.

# Getting Started

Follow these steps to run the dashboard locally on your machine.

## Prerequisites

- Windows Subsystem for Linux running Ubuntu

- Docker Desktop installed and integrated with WSL distro

- Python installed inside WSL

- Git

- Ansible

1. Clone the Repository

```bash
git clone [https://github.com/AryanK0202/sap-dashboard.git](https://github.com/AryanK0202/sap-dashboard.git)
cd sap-ansible-ops-dashboard
```
2. Set Up the Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies. Since you are operatig  withing a WSL, run the following commands to create and activate the environment. 
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Start simulated infrastructure

Ensure Docker desktop is open and running on your Windows host. In your WSL terminal run the following to start up 6 docker containers simulating SAP nodes
```bash
docker compose up -d
```

5. Launch the dashboard

Sync the initial state from Docker and start Streamlit
```bash
python3 generate_data.py
streamlit run app.py
```
Open a browser and navigate to the localhost

# Automation simulation

Since this is a prototype dasbaord, we are going to simulate infrastrcuture failures and use the dashbords Ansible integration to remediate them.

1. Break them environment

Open a separate WSL terminal, ensure you are in the project directory and run these commands:
```bash
#Simulate 24 pending patches on a Web-Dispatcher node
docker exec sap-web-03 sh -c "echo '24' > /tmp/pending_patches.txt"

#Simulate a critical system failure by stopping an App server node
docker stop sap-app-05
```

2. Remediate via Dashboard

- Return to web browser and click "Sync all nodes from Docker" to refresh
- You will now see sap-web-03 flagged as Warning and sap-app-05 flagged as Critical
- Select either of these sytems from the dropdown in the Targeted Remediation sandbox
- Click the "Run Remediation Playbook"
- Dashboard will execute remediate.yml in the background, updating the UI once done. 
