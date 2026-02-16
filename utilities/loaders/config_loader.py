import yaml
import os

def configYmlLoad(file_path: str):
    if not os.path.exists(file_path):
        print(f"Errore: Il file '{file_path}' non esiste.")
        return None
    
    with open(file_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            print(f"Errore di sintassi nel file YAML: {e}")
            return None