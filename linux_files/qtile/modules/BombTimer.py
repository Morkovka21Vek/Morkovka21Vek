import time
import asyncio

class BombTimer():
    def __init__(self, **config):
        self.text = "";
        self.timer_task = None
        self.end_time = 0

    def start_timer(self, duration):
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()

        self.end_time = time.time() + duration
        self.timer_task = asyncio.create_task(self.run_timer())

    async def run_timer(self):
        while time.time() < self.end_time:
            remaining = self.end_time - time.time()
            if remaining <= 0:
                break
            self.text = f"{remaining:.1f}"
            await asyncio.sleep(0.1)
        self.text = ""

    def get(self):
        return self.text;


    def cmd_start(self, duration=40):
        self.start_timer(duration)

