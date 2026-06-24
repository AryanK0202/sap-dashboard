import pandas as pd
import random

#Core conig vectors that match a real SAP landscape
roles = ['HANA DB', 'App server', 'Web Dispatcher']
clouds = ['AWS', 'Azure', 'GCP']
health_states = ['Healthy', 'Warning', 'Critical']
ansible_states = ['Success', 'Failed']

data = []

for i in range(1, 101):
    #Determine realistic distribution weights
    health = random.choices(health_states, weights = [85, 10, 5])[0]

    #Assign Ansible status
    if health == 'Critical':
        ansible = 'Failed'
        sync = 'Offline'
        patches = random.randint(15, 40)
    elif health == 'Warning':
        ansible = 'Warning'
        sync = f"{random.randint(1, 4)}h ago"
        patches = random.randint(5, 20)
    else:
        ansible = 'Success'
        sync = f"{random.randint(2, 45)}m ago"
        patches = 0

    data.append({
        'System ID': f"SAP-{random.choice(['PRD', 'QAS', 'DEV'])}-{i:02d}",
        'Role': random.choice(roles),
        'Cloud Provider': random.choice(clouds),
        'Health Status': health,
        'Last Ansible Sync': sync,
        'Last Playbook Run': ansible,
        'Pending OS Patches': patches,
        'Cert Expiry (Days)': random.randint(-2, 120) if health != 'Healthy' else random.randint(31, 365)
    })

    df = pd.DataFrame(data)
    df.to_csv('sap_nodes.csv', index = False)
    print("Sucessfully generated sap_nodes.csv")
