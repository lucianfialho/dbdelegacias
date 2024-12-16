class BaseState:
    def __init__(self, uf, label, slug):
        self.uf = uf
        self.label = label
        self.slug = slug
        self.data = {"uf": uf, "label": label, "slug": slug, "cities": []}

    def save_to_json(self, path):
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_city(self, city_name, delegacies):
        self.data["cities"].append({
            "name": city_name,
            "label": city_name,
            "delegacies": delegacies
        })
