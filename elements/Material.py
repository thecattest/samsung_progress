class Material:
    def __init__(self, material_id, link, title):
        self.id = material_id
        self.link = link
        self.title = title

    def __str__(self):
        return f"{self.title} {self.link}"
