from enum import Enum


class SimulationState(Enum):
    """
    Represents the possible states of the simulation.

    Attributes:
        IDLE: The simulation has not started or has been reset.
        RUNNING: The simulation is actively playing through turns.
        PAUSED: The simulation has been manually paused mid-playback.
        FINISHED: All drones have reached the destination.
    """

    IDLE = 0
    RUNNING = 1
    PAUSED = 2
    FINISHED = 3
