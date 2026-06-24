import pandas as pd
import docker
import datetime

def sync_docker_inventory():
    print("🔄 Connecting to local Docker daemon...")
    try:
        # Connect to Docker (works natively in WSL)
        client = docker.from_env()
        containers = client.containers.list()
    except Exception as e:
        print(f"❌ Failed to connect to Docker. Is Docker running? Error: {e}")
        return

    data = []
    
    for container in containers:
        labels = container.labels
        
        # Only process containers that have our 'sap_role' label
        if 'sap_role' in labels:
            system_id = container.name.upper()
            health = labels.get('sap_health', 'Unknown')
            
            # Simulate Ansible logic based on the health label
            ansible_status = 'Success' if health == 'Healthy' else 'Failed' if health == 'Critical' else 'Success'
            
            # Add to our dataset
            data.append({
                'System ID': system_id,
                'Role': labels.get('sap_role', 'Unknown'),
                'Cloud Provider': labels.get('sap_cloud', 'Unknown'),
                'Health Status': health,
                'Last Ansible Sync': "Just now",  # Since we are querying live
                'Last Playbook Run': ansible_status,
                'Pending OS Patches': int(labels.get('sap_patches', 0)),
                'Cert Expiry (Days)': int(labels.get('sap_cert_days', 0))
            })

    if not data:
        print("⚠️ No SAP containers found. Did you run 'docker compose up -d'?")
        return

    # Export to CSV for the Streamlit dashboard to read
    df = pd.DataFrame(data)
    df.to_csv('sap_nodes.csv', index=False)
    
    print(f"✅ Successfully synced {len(data)} nodes from Docker to sap_nodes.csv!")
    print(df.to_string(index=False))

if __name__ == "__main__":
    sync_docker_inventory()