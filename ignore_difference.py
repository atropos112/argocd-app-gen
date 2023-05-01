from kind import Kind


class IgnoreDifference:
    def __init__(self, group: str, kind: Kind, jsonPointers: list):
        self.group = group
        self.kind = kind
        self.jsonPointers = jsonPointers

    def to_json(self):
        return {
            "group": self.group,
            "kind": self.kind.name,
            "jsonPointers": self.jsonPointers,
        }