class SpecimenRegistry:
    def __init__(self):
        self.specimens = {}
        self.by_family = {}

    def clear(self):
        self.specimens.clear()
        self.by_family.clear()

    def add(self, spec):
        sid = spec.get("id")
        if not sid:
            return
        self.specimens[sid] = spec
        family   = spec.get("standard", "Other")
        standard = spec.get("standard_number", "Unknown")
        fam_bucket = self.by_family.setdefault(family, {})
        fam_bucket.setdefault(standard, []).append(sid)

    def get(self, sid):
        return self.specimens.get(sid)

    def families(self):
        return sorted(self.by_family.keys())

    def standards(self, family):
        return sorted(self.by_family.get(family, {}).keys())

    def specimens_for(self, family, standard):
        return list(self.by_family.get(family, {}).get(standard, []))

    def is_custom(self, sid):
        spec = self.specimens.get(sid)
        return bool(spec and spec.get("library", {}).get("type") == "custom")

    def all_custom(self):
        return [s for s in self.specimens.values()
                if s.get("library", {}).get("type") == "custom"]


registry = SpecimenRegistry()
