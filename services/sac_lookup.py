import csv
from pathlib import Path

_LOOKUP_CACHE = None

def load_lookup():
    global _LOOKUP_CACHE

    if _LOOKUP_CACHE is not None:
        return _LOOKUP_CACHE

    csv_path = Path(__file__).resolve().parent.parent / "data" / "small_area_lookup.csv"

    lookup = {}

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            object_id = row["OBJECT_ID"].strip()
            sa2022 = row["SA2022"].strip()
            lookup[object_id] = sa2022

    _LOOKUP_CACHE = lookup
    return lookup


def get_sa2022(small_area_id: str):
    lookup = load_lookup()

    try:
        formatted_id = f"B{int(small_area_id):05d}"
    except ValueError:
        raise Exception(f"Invalid small_area_id: {small_area_id}")

    return lookup.get(formatted_id)
