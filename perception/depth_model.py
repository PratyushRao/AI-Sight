import torch
import cv2

class DepthEstimator:
     
    def __init__(self):
        self.midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
        self.midas.eval()

        transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        self.transform = transforms.small_transform
    


    def get_depth_map(self, frame):
        import cv2
        import torch

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # ❗ FIXED LINE (no unsqueeze)
        input_batch = self.transform(img)

        with torch.no_grad():
            prediction = self.midas(input_batch)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        depth_map = prediction.cpu().numpy()
        return depth_map