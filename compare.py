import json

def load_hosts(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return set(host['host'] for host in data['hosts'])

hosts_file_1 = 'data/hosts_UMS_HOST_URL_API.json'
hosts_file_2 = 'data/hosts_UMS_JIRA_PRD_URL.json'

hosts_1 = load_hosts(hosts_file_1)
hosts_2 = load_hosts(hosts_file_2)

hosts_missing_integration = hosts_1 - hosts_2

output_filename = 'data/hosts_missing_integration.json'
output_data = {
    "hosts_missing_integration": [{"host": host} for host in hosts_missing_integration]
}

with open(output_filename, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"Total de hosts sem integração: {len(hosts_missing_integration)}")
print(f"Resultado salvo em: {output_filename}")