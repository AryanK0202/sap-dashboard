# SAP Cloud Operations & Automation Dashboard

This prototype is designed to visualize and manage a massive SAP cloud landscape (AWS, Azure, GCP) by integrating infrastructure monitoring with actionable Ansible automation.

# Overview

Managing an enterprise-grade SAP landscape (Virtual Machines, HANA DBs, Web-dispatchers) across multiple hyperscalers requires an exception-based monitoring approach. This dashboard filters out the noise, highlighting systems that require human intervention for:

System Health: Identifying offline or critical nodes.

OS Patch Compliance: Tracking pending package updates across the fleet.

Certificate Management: Highlighting SSL/SSO certificates approaching expiration.

Automation Sync: Tracking the success/failure rate of backend Ansible playbooks.

# Features

Dynamic Mock Data Generation: Instantly spin up a realistic dataset of 100 SAP nodes to simulate enterprise environments.

Live Filtering: Drill down by Cloud Provider, System Role, and Health Status.

Actionable UIs: Mock remediation buttons demonstrating how UI elements trigger targeted Ansible playbooks (e.g., batch_patch.yml).

Instant KPIs: High-visibility metrics for Total Nodes, Critical Systems, Pending Patches, and Expiring Certs.

# Getting Started

Follow these steps to run the dashboard locally on your machine.

Prerequisites

Python 3.8+ installed

Git

1. Clone the Repository

```bash
git clone [https://github.com/AryanK0202/sap-dashboard.git](https://github.com/AryanK0202/sap-dashboard.git)
cd sap-ansible-ops-dashboard
```
2. Set Up the Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies. 

First connect to the WSL, then run:
```bash
python -m venv .venv
.venv\Scripts\activate
```
3. Also make sure you have Docker Desktop installed 

# Automation
## Since this is a prototype dasbaord, we are going to simulate automation

To do so, run these commands:
```bash
docker exec sap-web-03 sh -c "echo '24' > /tmp/pending_patches.txt"

docker stop sap-app-05
```
These commands break the docker containers
