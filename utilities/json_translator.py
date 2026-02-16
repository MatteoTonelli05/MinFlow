import json

def graphJsonLoad(file_path):
    try:
        with open(file_path, 'r') as file_json:
            graph_data = json.load(file_json)
        
        if "nodes" not in graph_data or not graph_data["nodes"]:
            print("Errore: Grafo privo di nodi o campo 'nodes' mancante.")
            return None
        
        if "edges" not in graph_data or not graph_data["edges"]:
            print("Errore: Grafo privo di archi o campo 'edges' mancante.")
            return None

        return graph_data
    
    except FileNotFoundError:
        print(f"Errore: File non trovato in {file_path}")
    except json.JSONDecodeError:
        print("Errore: Il file non è un JSON valido.")
    except Exception as e:
        print(f"Errore imprevisto: {e}")

# Esempio di utilizzo
file_path = r"resource\grafo_iniziale.json" # la 'r' serve per gestire i backslash di Windows
grafo = graphJsonLoad(file_path)