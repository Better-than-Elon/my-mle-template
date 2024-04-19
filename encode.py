from ansible_vault import Vault
import yaml
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ansib_file_pass = config['secrets']['ansible_file_path']
secrets_file_pass = config['secrets']['db']

data = yaml.safe_load(open(secrets_file_pass, 'r'))
vault = Vault(open(ansib_file_pass, 'r').read()[:-1])
vault.dump(data, open(secrets_file_pass, 'w'))

print(vault.dump(data))
