import torch
import cv2
import numpy as np

class DepthEstimator:
    def __init__(self):
        # Select device (CUDA > CPU)
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        print(f"Using device: {self.device}")

        # Load MiDaS Small model
        self.midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
        self.midas.to(self.device)
        self.midas.eval()

        # Load transforms
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        self.transform = midas_transforms.small_transform

        # Use FP16 for faster inference on CUDA
        if self.device.type == "cuda":
            self.midas = self.midas.half()
            print("Using FP16 for inference")

        # Compile model for extra speed (PyTorch 2.0+)
        if hasattr(torch, "compile"):
            try:
                self.midas = torch.compile(self.midas)
                print("Model compiled using torch.compile")
            except Exception as e:
                print(f"Failed to compile model: {e}")

        # Warmup the model
        self._warmup()

    def _warmup(self):
        """Run a dummy frame through the model to initialize CUDA kernels."""
        print("Warming up depth estimator...")
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.get_depth_map(dummy_frame)
        print("Warmup complete.")

    def get_depth_map(self, frame, target_size=None):
        """Estimates depth from a BGR image. 
        If target_size is None, returns raw model output (fastest).
        """
        # Convert BGR to RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Apply transforms and move to device
        input_batch = self.transform(img).to(self.device)
        
        # Match model precision
        if self.device.type == "cuda":
            input_batch = input_batch.half()

        with torch.no_grad():
            # Run inference
            prediction = self.midas(input_batch)

            # Resize if a target size is explicitly requested
            if target_size:
                prediction = torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=target_size,
                    mode="bicubic",
                    align_corners=False,
                ).squeeze()

        # Convert to numpy and return
        depth_map = prediction.cpu().numpy()
        return depth_map