from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates
from libqtile import widget

class NvidiaGpuWidget(widget.base.ThreadPoolText):
    """Виджет для отображения загрузки GPU (CUDA) с помощью NVML."""

    def __init__(self, **config):
        super().__init__("", **config)
        nvmlInit()
        self.handle = nvmlDeviceGetHandleByIndex(0)  # Используем первый GPU (индекс 0)

    def poll(self):
        try:
            utilization = nvmlDeviceGetUtilizationRates(self.handle)
            gpu_usage = utilization.gpu
            #return f"GPU: {gpu_usage}%"
            return f"{gpu_usage}%\n<small><small>GPU</small></small>"
        except Exception as e:
            return f"{Err}%\n<small><small>GPU</small></small>"
            #return f"GPU: Err"
