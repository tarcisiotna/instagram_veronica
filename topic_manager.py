#!/usr/bin/env python3
import json
import os
from datetime import datetime

TOPICS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posted_topics.json")

def load_topics():
    if not os.path.exists(TOPICS_FILE):
        return {"topics": []}
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_topics(data):
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_topic(topic, notes="Postado no Instagram"):
    data = load_topics()
    topic_lower = topic.lower().strip()
    
    for t in data["topics"]:
        if t["topic"].lower() == topic_lower:
            print(f"AVISO: O assunto '{topic}' já foi postado em {t['date']}")
            return False
    
    data["topics"].append({
        "topic": topic,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "notes": notes
    })
    save_topics(data)
    print(f"Assunto '{topic}' registrado com sucesso!")
    return True

def check_topic(topic):
    data = load_topics()
    topic_lower = topic.lower().strip()
    
    for t in data["topics"]:
        if topic_lower in t["topic"].lower() or t["topic"].lower() in topic_lower:
            print(f"JÁ POSTADO: '{t['topic']}' em {t['date']} - {t['notes']}")
            return True
    
    print(f"NÃO ENCONTRADO: O assunto '{topic}' não foi postado ainda.")
    return False

def list_topics():
    data = load_topics()
    if not data["topics"]:
        print("Nenhum assunto registrado ainda.")
        return
    
    print("\n=== ASSUNTOS JÁ POSTADOS ===")
    for i, t in enumerate(data["topics"], 1):
        print(f"{i}. {t['topic']} - {t['date']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python topic_manager.py add 'assunto'")
        print("  python topic_manager.py check 'assunto'")
        print("  python topic_manager.py list")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) >= 3:
        topic = " ".join(sys.argv[2:])
        add_topic(topic)
    elif command == "check" and len(sys.argv) >= 3:
        topic = " ".join(sys.argv[2:])
        check_topic(topic)
    elif command == "list":
        list_topics()
    else:
        print("Comando inválido. Use: add, check ou list")
