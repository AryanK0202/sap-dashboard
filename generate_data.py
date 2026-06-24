import pandas as pd
import docker
import os

def sync_docker_inventory():
    print("🔄 Connecting to local Docker daemon...")
    try:
        # Connects natively to the Docker daemon running in WSL
        client = docker.from_env()
        containers = client.containers.list(all=True) # Get all containers, even stopped ones
    except Exception as e:
        print(f"❌ Failed to connect to Docker. Is Docker running? Error: {e}")
        return

    data = []
    
    for container in containers:
        labels = container.labels
        
        # Only process containers that have our 'sap_role' label
        if 'sap_role' in labels:
            system_id = container.name.upper()
            role = labels.get('sap_role', 'Unknown')
            cloud = labels.get('sap_cloud', 'Unknown')
            
            # 1. Check if container is actually running (Simulate System Down)
            if container.status != 'running':
                health = 'Critical'
                ansible_status = 'Failed'
                patches = int(labels.get('sap_patches', 0))
            else:
                # 2. Check for our dummy "pending patches" file (Simulate Warning)
                # We use docker exec to run a command inside the container
                exit_code, output = container.exec_run("cat /tmp/pending_patches.txt")
                
                if exit_code == 0: # File exists!
                    health = 'Warning'
                    ansible_status = 'Success'
                    # Read the number from the file, clean up whitespace
                    patches = int(output.decode('utf-8').strip()) 
                else:
                    # System is running and no patch file exists
                    health = 'Healthy'
                    ansible_status = 'Success'
                    patches = 0

            # Add to our dataset
            data.append({
                'System ID': system_id,
                'Role': role,
                'Cloud Provider': cloud,
                'Health Status': health,
                'Last Ansible Sync': "Just now", 
                'Last Playbook Run': ansible_status,
                'Pending OS Patches': patches,
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