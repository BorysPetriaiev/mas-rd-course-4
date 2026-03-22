import os
import trafilatura
from ddgs import DDGS
from config import MAX_TEXT_LENGTH,OUTPUT_DIR

def web_search_func(query: str) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    return "\n---\n".join([f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}" for r in results])

def read_url_func(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded) if downloaded else None
    if not text:
        return "Помилка: не вдалося витягти текст зі сторінки."
    text = text.strip()

    return text[:MAX_TEXT_LENGTH] 

def write_report_func(filename: str, content: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"✅ Звіт успішно збережено у файл: {path}"

tools_map = {
    "web_search": web_search_func,
    "read_url": read_url_func,
    "write_report": write_report_func
}

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Пошук в інтернеті. Повертає список результатів.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_url",
            "description": "Читає текст веб-сторінки за URL.",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_report",
            "description": "Зберігає Markdown звіт у файл.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["filename", "content"]
            }
        }
    }
]