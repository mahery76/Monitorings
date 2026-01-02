import subprocess
import re
import threading
import queue
import matplotlib.pyplot as plt


class PingWorker(threading.Thread):
    """Thread responsible ONLY for ping collection (no plotting)."""

    def __init__(self, host: str, output_queue: queue.Queue):
        super().__init__(daemon=True)
        self.host = host
        self.queue = output_queue
        self.pattern = re.compile(r'(time|temps)[=<]\s*([\d.]+)')
        self.process = None

    def run(self):
        self.process = subprocess.Popen(
            ["ping", self.host, "-t"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )

        for line in self.process.stdout:
            match = self.pattern.search(line)
            if match:
                self.queue.put(float(match.group(2)))


class PingPlot:
    """Plot handled STRICTLY in main thread."""

    def __init__(self, host: str):
        self.host = host
        self.data = []

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])

        self.ax.set_title(f"Ping Results to {host}")
        self.ax.set_xlabel("Ping Count")
        self.ax.set_ylabel("Latency (ms)")
        self.ax.set_ylim(0, 1000)

    def update(self, value: float):
        self.data.append(value)
        self.line.set_data(range(len(self.data)), self.data)
        self.ax.relim()
        self.ax.autoscale_view()


if __name__ == "__main__":
    # Queues for thread-safe communication
    q_google = queue.Queue()
    q_microsoft = queue.Queue()

    # Start ping workers
    PingWorker("8.8.8.8", q_google).start()
    PingWorker("allpro.alphaciment.com", q_microsoft).start()

    # Create plots in MAIN thread
    plot_google = PingPlot("Google public DNS")
    plot_microsoft = PingPlot("Allpro")
    plt.ion()

    try:
        while True:
            while not q_google.empty():
                plot_google.update(q_google.get())

            while not q_microsoft.empty():
                plot_microsoft.update(q_microsoft.get())

            plt.pause(0.05)

    except KeyboardInterrupt:
        pass

    plt.ioff()
    plt.show()
