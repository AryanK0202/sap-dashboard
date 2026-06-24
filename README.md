📊 SAP Cloud Operations & Automation Dashboard

A presentation-ready, interactive operations dashboard built with Python and Streamlit. This prototype is designed to visualize and manage a massive SAP cloud landscape (AWS, Azure, GCP) by integrating infrastructure monitoring with actionable Ansible automation.

🎯 Overview

Managing an enterprise-grade SAP landscape (Virtual Machines, HANA DBs, Web-dispatchers) across multiple hyperscalers requires an exception-based monitoring approach. This dashboard filters out the noise, highlighting systems that require human intervention for:

System Health: Identifying offline or critical nodes.

OS Patch Compliance: Tracking pending package updates across the fleet.

Certificate Management: Highlighting SSL/SSO certificates approaching expiration.

Automation Sync: Tracking the success/failure rate of backend Ansible playbooks.

✨ Features

Dynamic Mock Data Generation: Instantly spin up a realistic dataset of 100 SAP nodes to simulate enterprise environments.

Live Filtering: Drill down by Cloud Provider, System Role, and Health Status.

Actionable UIs: Mock remediation buttons demonstrating how UI elements trigger targeted Ansible playbooks (e.g., batch_patch.yml).

Instant KPIs: High-visibility metrics for Total Nodes, Critical Systems, Pending Patches, and Expiring Certs.

🚀 Getting Started

Follow these steps to run the dashboard locally on your machine.

Prerequisites

Python 3.8+ installed

Git

1. Clone the Repository

git clone [https://github.com/AryanK0202/sap-dashboard.git](https://github.com/AryanK0202/sap-dashboard.git)
cd sap-ansible-ops-dashboard

2. Set Up the Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

# Windows

py -m venv .venv
.venv\Scripts\activate

🔮 Future Roadmap (Production Integration)

While this is a presentation prototype, the architecture is designed to scale:

API Integration: Replace the static CSV data layer with API calls to a centralized database populated by Ansible fact-gathering playbooks.

Webhooks: Connect the "Run Playbook" buttons to an automation controller (like AWX/Ansible Tower) via REST APIs to trigger real-time targeted remediation.

Containerization: Package the frontend using Docker for high availability.
