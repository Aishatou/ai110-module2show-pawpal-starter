from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    description: str
    duration: int
    priority: str
    frequency: str
    completed: bool = False

    def mark_complete(self):
        pass

@dataclass
class Pet:
    name: str
    species: str
    age: int
    allergies: List[str] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_tasks(self):
        pass

class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def get_all_tasks(self):
        pass

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self):
        pass

    def sort_by_priority(self):
        pass

    def detect_conflicts(self):
        pass

    def filter_by_status(self, completed: bool):
        pass
    