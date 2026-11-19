import json
import time


class Benchmark:
    """Records time per task and a routing trace; saves to benchmarks.json."""

    def __init__(self, query: str):
        self.query = query
        self.start = self.last = time.time()
        self.tasks, self.trace = [], []

    def log_step(self, step):
        self.trace.append({"t": round(time.time() - self.start, 2),
                           "step": str(step)[:200]})

    def log_task(self, output):
        now = time.time()
        self.tasks.append({
            "task": (getattr(output, "description", "") or "")[:80],
            "agent": str(getattr(output, "agent", "unknown")),
            "seconds": round(now - self.last, 2),
        })
        self.last = now

    def save(self, path="benchmarks.json"):
        data = {"query": self.query,
                "total_seconds": round(time.time() - self.start, 2),
                "tasks": self.tasks, "routing_trace": self.trace}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data
