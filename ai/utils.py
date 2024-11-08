from typing import Any

class ProcessingResult:
    def __init__(self, success: bool, data: Any, error: str = ""):
        self.success = success
        self.data = data
        self.error = error

    def __str__(self):
        if self.success:
            return f"Success: {self.success}"
        else:
            return f"Failed: {self.error}"
