from enum import Enum


class SimulationState(Enum):
    IDLE = 0
    RUNNING = 1
    PAUSED = 2
    FINISHED = 3
