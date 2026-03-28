import json
import os

JSON_FILE = "disciplinas.json"

def init_db():
    """Inicializa o arquivo JSON caso ele não exista."""
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def load_data():
    """Lê todos os dados do arquivo JSON."""
    init_db()
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """Salva a lista de dados no arquivo JSON."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def insert_disciplina(disciplina, av1, av2, av3, av4, media, situacao):
    data = load_data()
    # Criamos o dicionário sem o campo ID
    nova_disciplina = {
        "disciplina": disciplina,
        "av1": av1,
        "av2": av2,
        "av3": av3,
        "av4": av4,
        "media": media,
        "situacao": situacao
    }
    data.append(nova_disciplina)
    save_data(data)

def get_all_disciplinas():
    data = load_data()
    # Retorna como lista de tuplas para manter compatibilidade com o Treeview do main.py
    return [tuple(d.values()) for d in data]

def search_disciplinas(termo_busca):
    data = load_data()
    termo_busca = termo_busca.lower()
    resultado = [
        tuple(d.values()) for d in data 
        if termo_busca in d["disciplina"].lower()
    ]
    return resultado

def update_disciplina(old_discipline, new_discipline, av1, av2, av3, av4, media, situacao):
    data = load_data()
    for d in data:
        if d["disciplina"] == old_discipline:
            d.update({
                "disciplina": new_discipline,
                "av1": av1,
                "av2": av2,
                "av3": av3,
                "av4": av4,
                "media": media,
                "situacao": situacao
            })
            break
    save_data(data)

def delete_disciplina(disciplina_nome):
    data = load_data()
    # Filtra a lista removendo a disciplina selecionada
    data = [d for d in data if d["disciplina"] != disciplina_nome]
    save_data(data)

# Inicializa o arquivo ao importar o módulo
init_db()
