import pyttsx3
import time
import threading
import config
from queue import Queue

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', config.SPEECH_RATE)

        self.queue = Queue()

        self.last_spoken_time = 0
        self.MIN_INTERVAL = 2      # 🔥 speak every 2 sec
        self.EVENT_COOLDOWN = 0.5  # fast alerts

        # Start background thread
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while True:
            text = self.queue.get()
            self.engine.say(text)
            self.engine.runAndWait()   # ✅ REQUIRED
            self.queue.task_done()

    def speak(self, text, force=False):
        now = time.time()

        # ⚡ Immediate alert (high priority)
        if force:
            if now - self.last_spoken_time > self.EVENT_COOLDOWN:
                self._enqueue(text)
            return

        # 🔁 Periodic speaking
        if now - self.last_spoken_time > self.MIN_INTERVAL:
            self._enqueue(text)

    def _enqueue(self, text):
        # 🚫 prevent queue spam
        if self.queue.qsize() > 2:
            return

        self.queue.put(text)
        self.last_spoken_time = time.time()

    def stop(self):
        self.engine.stop()