import os
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv

load_dotenv()

ZABBIX_URL = os.getenv('ZABBIX_URL')
ZABBIX_TOKEN = os.getenv('ZABBIX_TOKEN')
auth_token = ZABBIX_TOKEN

group_name = "UMS/HOST/URL/API" #Passe o nome do grupo
host_data = []
output_data = {}

def get_hostgroup_id(auth_token, group_name):
    payload = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": ["groupid"],
            "filter": {
                "name": [group_name]
            }
        },
        "auth": auth_token,
        "id": 1
    }
    try:
        response = requests.post(ZABBIX_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json-rpc'}, verify=False)
        response.raise_for_status() 
        print(f"Grupos de hosts: {response.text}")
        result = response.json().get('result')
        if result:
            return result[0].get('groupid')
    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação HTTP: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    return None

def get_hosts(auth_token, groupid):
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "name", "status"],
            "groupids": groupid,
            "filter": {
                "status": "0"
            }
        },
        "auth": auth_token,
        "id": 1
    }
    try:
        response = requests.post(ZABBIX_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json-rpc'}, verify=False)
        response.raise_for_status()
        return response.json().get('result')
    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação HTTP: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    return None

if auth_token:
    groupid = get_hostgroup_id(auth_token, group_name)
    if groupid:
        hosts = get_hosts(auth_token, groupid)
        if hosts:
            print(f"Total de hosts: {len(hosts)}")
            for host in hosts:
                host_data.append({
                        "host": host['name']
                    })
        else:
            print("Falha ao obter dados de hosts")
    else:
        print(f"Falha ao obter o ID do grupo de hosts '{group_name}'")
else:
    print("Falha na autenticação")

if not os.path.exists('data'):
    os.makedirs('data')

safe_group_name = group_name.replace('/', '_')

filename = f"data/hosts_{safe_group_name}.json"

output_data["hosts"] = host_data

with open(filename, 'w') as f:
    json.dump(output_data, f, indent=4)
