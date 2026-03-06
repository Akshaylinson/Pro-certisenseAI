# placeholder showing where AI integration goes
# not used in the basic flow

import torch

class DummyModel:
    def __init__(self):
        # minimal torch artifact for demonstration
        self.model = None

    def run(self, data_bytes: bytes):
        # placeholder: returns length and dummy score
        return {"length": len(data_bytes), "score": 0.0}
