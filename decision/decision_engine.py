import config

class DecisionEngine:
    def __init__(self):
        self.prev_scene = []

    def has_changed(self, scene):
        if scene != self.prev_scene:
            self.prev_scene = scene
            return True
        return False

    def decide(self, objects):
        alerts = []

        for obj in objects:
            label = obj["label"]
            pos = obj["position"]
            dist = obj["distance"]

            priority = self.get_priority(label, dist)

            if priority > 0:
                alerts.append({
                    "message": self.format_message(label, pos, dist),
                    "priority": priority,
                    "distance": dist
                })

        # 🔥 Sort: highest priority + closest first
        alerts = sorted(
            alerts,
            key=lambda x: (-x["priority"], self.dist_score(x["distance"]))
        )

        return alerts

    # 🚨 PRIORITY LOGIC
    def get_priority(self, label, dist):
        if label in ["car", "bus", "truck", "motorcycle"]:
            return 3 if dist == "near" else 2

        elif label == "person":
            return 2 if dist == "near" else 1

        else:
            return 1 if dist == "near" else 0

    # 🧠 DISTANCE SORTING
    def dist_score(self, dist):
        return {"near": 0, "medium": 1, "far": 2}.get(dist, 2)

    # 🔊 MESSAGE FORMATTING
    def format_message(self, label, pos, dist):
        if label in ["car", "bus", "truck", "motorcycle"]:
            return f"Warning vehicle {pos}"

        elif label == "person":
            if dist == "near":
                return f"Person very close {pos}"
            return f"Person {pos}"

        else:
            return f"Obstacle {pos}"