from utils.helper import get_position, get_distance
import config

class SceneAnalyzer:
    def __init__(self, detector, depth_estimator):
        self.detector = detector
        self.depth_estimator = depth_estimator

    def analyze(self, frame):
        detections = self.detector.detect(frame)
        depth_map = self.depth_estimator.get_depth_map(frame)

        h, w = frame.shape[:2]
        dh, dw = depth_map.shape[:2] # Dimensions of the low-res depth map
        
        scene_objects = []

        for det in detections:
            x1, y1, x2, y2 = map(int, det["bbox"])

            # Scale center coordinates to depth map resolution
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            
            dcx = int(cx * dw / w)
            dcy = int(cy * dh / h)

            # Ensure coordinates are within bounds
            dcx = min(max(0, dcx), dw - 1)
            dcy = min(max(0, dcy), dh - 1)

            depth_value = depth_map[dcy, dcx]

            position = get_position(cx, w, config)
            distance = get_distance(depth_value, config)

            scene_objects.append({
                "label": det["label"],
                "position": position,
                "distance": distance
            })

        return scene_objects