import cv2

from perception.yolo_detector import YOLODetector
from perception.depth_model import DepthEstimator
from fusion.scene_analyzer import SceneAnalyzer
from decision.decision_engine import DecisionEngine
from audio.tts_engine import TTSEngine

def main():
    cap = cv2.VideoCapture(0)

    detector = YOLODetector()
    depth_estimator = DepthEstimator()
    analyzer = SceneAnalyzer(detector, depth_estimator)
    decision_engine = DecisionEngine()
    tts = TTSEngine()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        scene = analyzer.analyze(frame)
        alerts = decision_engine.decide(scene)

        if alerts:
            message = alerts[0]["message"]
        else:
            message = "No obstacles ahead"

        changed = decision_engine.has_changed(scene)

        # ⚡ Immediate alert if something changes
        if changed:
            tts.speak(message, force=True)

        tts.speak(message)
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    tts.stop() # Ensure TTS engine is gracefully stopped

if __name__ == "__main__":
    main()