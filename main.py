"""
Тестовое задание:
Сделать мини-приложение на Python, которое:
Загружает первые 100 тендеров с сайта https://www.b2b-center.ru/market/ или https://rostender.info/extsearch
Извлекает ключевые показатели для каждого тендера (Например: номер, ссылка, покупатель, товары, дата окончания и т.п.):
Сохраняет эти данные в SQLite или CSV;
Имеет простой CLI-интерфейс:
python main.py --max 10 --output tenders.csv
(опционально) Есть FastAPI endpoint /tenders — возвращает JSON с данными;
Разместить на github
README с пояснением: как работает, как запускать, что использовал, что бы улучшил.
"""
import argparse
import csv
from parser import get_tenders

FIELDS = [
    'id', 'title', 'link', 'region'
]

def save_to_csv(tenders, path):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()

        for tender in tenders:
            filtered = {key: tender.get(key, '') for key in FIELDS}
            writer.writerow(filtered)

def main():
    parser = argparse.ArgumentParser(description='Сбор тендеров с rostender.info')
    parser.add_argument('--max', type=int, default=100, help='Максимум тендеров (по умолчанию 100)')
    parser.add_argument('--output', type=str, default='tenders.csv', help='Путь к CSV-файлу')

    args = parser.parse_args()

    print(f"Собираем до {args.max} тендеров...")
    tenders = get_tenders(max_count=args.max)
    print(f"Собрано: {len(tenders)} тендеров")

    print(f"Сохраняем в файл: {args.output}")
    save_to_csv(tenders, args.output)
    print("Готово! Проверь файл:", args.output)

if __name__ == '__main__':
    main()