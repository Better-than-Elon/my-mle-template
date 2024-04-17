import configparser
from ansible_vault import Vault

class AnsibleDecoder:
    def __init__(self, config: configparser.ConfigParser) -> None:
        self.secrets = config['secrets']
        with open(self.secrets["ansible_file_path"]) as anse_file:
            self.vault = Vault(anse_file.read()[:-1])
            
            
    @classmethod
    def default_config(cls):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return cls(config)
       
       
    def get_secrets(self, name: str):
        return self.vault.load(open(self.secrets[name]).read())


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(AnsibleDecoder(config).get_secrets('db'))
