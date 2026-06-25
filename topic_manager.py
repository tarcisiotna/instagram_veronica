import json
import sys
from pathlib import Path
from datetime import date

DATA_FILE = Path(__file__).parent / "posted_topics.json"

def load_topics():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def save_topics(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def check(topic):
    data = load_topics()
    for t in data["topics"]:
        if topic.lower() in t["topic"].lower():
            print(f"'{t['topic']}' foi postado em {t['date']}")
            return
    print(f"'{topic}' ainda não foi postado")

def add(topic):
    data = load_topics()
    for t in data["topics"]:
        if t["topic"].lower() == topic.lower():
            print(f"'{topic}' já está registrado (postado em {t['date']})")
            return
    data["topics"].append({"topic": topic, "date": str(date.today()), "notes": "postado no instagram"})
    save_topics(data)
    print(f"'{topic}' registrado como postado em {date.today()}")

def list_topics():
    data = load_topics()
    if not data["topics"]:
        print("Nenhum tópico registrado.")
        return
    for t in data["topics"]:
        print(f"- {t['topic']} ({t['date']})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python topic_manager.py <check|add|list> [assunto]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "check":
        if len(sys.argv) < 3:
            print("Uso: python topic_manager.py check \"assunto\"")
            sys.exit(1)
        check(sys.argv[2])
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Uso: python topic_manager.py add \"assunto\"")
            sys.exit(1)
        add(sys.argv[2])
    elif cmd == "list":
        list_topics()
    else:
        print(f"Comando desconhecido: {cmd}")
        print("Use: check, add, list")
        sys.exit(1)
