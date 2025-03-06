import redis
from models import Quote, Author
import re

# Підключення до Redis
cache = redis.Redis(host='localhost', port=6379, decode_responses=True)

def find_by_author(name):
    cached = cache.get(f"name:{name}")
    if cached:
        return cached

    pattern = re.compile(f"^{name}", re.IGNORECASE)
    authors = Author.objects(fullname__iregex=pattern)
    quotes = []
    for author in authors:
        results = Quote.objects(author=author)
        quotes.extend(q.quote for q in results)

    cache.set(f"name:{name}", str(quotes), ex=600)  # Кешуємо на 10 хвилин
    return quotes

def find_by_tag(tag):
    cached = cache.get(f"tag:{tag}")
    if cached:
        return cached

    quotes = [q.quote for q in Quote.objects(tags__icontains=tag)]
    cache.set(f"tag:{tag}", str(quotes), ex=600)
    return quotes

if __name__ == "__main__":
    while True:
        command = input("Введіть команду (name:, tag:, tags:, exit): ").strip()
        if command.startswith("name:"):
            print(find_by_author(command[5:]))
        elif command.startswith("tag:"):
            print(find_by_tag(command[4:]))
        elif command == "exit":
            break
