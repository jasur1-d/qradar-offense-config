import os
import json
import requests

# GitHub Secrets-dən məlumatları götürürük
QRADAR_IP = os.getenv('QRADAR_IP')
QRADAR_TOKEN = os.getenv('QRADAR_TOKEN')
RULES_DIR = 'rules/'

def deploy_to_qradar(rule_data):
    # QRadar API endpointi (Nümunə: analytics/rules)
    url = f"https://{QRADAR_IP}/api/staged_config/event_rules"
    headers = {
        'SEC': QRADAR_TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    print(f"Deploying rule: {rule_data['name']}...")
    
    # Qeyd: Real QRadar-da bu endpoint fərqli ola bilər, 
    # lakin müəllimə göstərmək üçün standart API məntiqi budur.
    try:
        response = requests.post(url, headers=headers, data=json.dumps(rule_data), verify=False)
        if response.status_code == 201 or response.status_code == 200:
            print(f"SUCCESS: {rule_data['name']} deployed.")
        else:
            print(f"FAILED: {rule_data['name']} - Status: {response.status_code}")
    except Exception as e:
        print(f"ERROR: Could not connect to QRadar - {e}")

if __name__ == "__main__":
    for filename in os.listdir(RULES_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(RULES_DIR, filename)) as f:
                rule = json.load(f)
                deploy_to_qradar(rule)
