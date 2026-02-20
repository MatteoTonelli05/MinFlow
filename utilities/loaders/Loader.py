import json
import yaml
from pathlib import Path

class Loader:

    @staticmethod
    def from_json(file_path: str):
        """
        carica un dizionario da un file json (usato per il grafo)
        
        :type file_path: percorso del file
        :return dizionario rappresentante il file
        """
        path = Path(file_path)
        if not path.exists():
            print(f"File non trovato: '{path}'")
            return None
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON non valido in '{path}'")
            return None
        except Exception as e:
            print("Errore sconosciuto")
            return None
        return data

    @staticmethod
    def from_yaml(file_path: str):
        """
        carica un dizionario da un file yaml (usato per le configurazioni)
        
        :type file_path: percorso del file
        :return dizionario rappresentante il file
        """
        path = Path(file_path)
        if not path.exists():
            print(f"File non trovato: '{path}'")
            return None
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"YAML non valido in '{path}'")
            return None
        except Exception as e:
            print("Errore sconosciuto")
            return None
        return data