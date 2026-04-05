from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path="./models/yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, imgsz=640)

        detections = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = self.model.names[cls]
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy()

                detections.append({
                    "label": label,
                    "conf": conf,
                    "bbox": xyxy
                })

        return detections