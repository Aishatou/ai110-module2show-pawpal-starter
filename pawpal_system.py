from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    description: str
    duration: int  # in minutes
    priority: str  # "high", "medium", "low"
    frequency: str  # "once", "daily", "weekly"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed and return a new recurring task if applicable."""
        from datetime import datetime, timedelta
        self.completed = True
        today = datetime.today().date()
        if self.frequency == "daily":
            return Task(
                description=self.description,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency
            )
        elif self.frequency == "weekly":
            return Task(
                description=self.description,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency
            )
        return None
    def __str__(self):
        status = "✅" if self.completed else "⬜"
        return f"{status} {self.description} ({self.duration} mins) [{self.priority} priority]"

@dataclass
class Pet:
    name: str
    species: str
    age: int
    allergies: List[str] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self):
        """Return only incomplete tasks."""
        return [t for t in self.tasks if not t.completed]

    def __str__(self):
        return f"{self.name} ({self.species}, {self.age} yrs)"

class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's roster."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return all tasks across all pets as (pet_name, Task) tuples."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet.name, task))
        return all_tasks

    def __str__(self):
        return f"Owner: {self.name} | Pets: {len(self.pets)}"

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self):
        """Return all pending tasks sorted by priority."""
        priority_order = {"high": 1, "medium": 2, "low": 3}
        pending = [(name, task) for name, task in self.owner.get_all_tasks() 
                   if not task.completed]
        return sorted(pending, key=lambda x: priority_order.get(x[1].priority.lower(), 4))

    def sort_by_priority(self):
        """Sort all tasks by priority level."""
        priority_order = {"high": 1, "medium": 2, "low": 3}
        return sorted(self.owner.get_all_tasks(), 
                      key=lambda x: priority_order.get(x[1].priority.lower(), 4))

    def detect_conflicts(self):
        """Flag tasks with the same description scheduled for the same pet."""
        warnings = []
        seen = {}
        for pet_name, task in self.owner.get_all_tasks():
            key = (pet_name, task.description.lower())
            if key in seen:
                warnings.append(f"⚠️ Duplicate task '{task.description}' for {pet_name}")
            else:
                seen[key] = task
        return warnings

    def filter_by_status(self, completed: bool):
        """Filter tasks by completion status."""
        return [(name, task) for name, task in self.owner.get_all_tasks() 
                if task.completed == completed]

    def todays_schedule(self):
        """Return a formatted string of today's schedule."""
        schedule = self.generate_schedule()
        if not schedule:
            return "No pending tasks for today!"
        lines = ["📅 Today's Schedule", "=" * 35]
        for pet_name, task in schedule:
            lines.append(f"  {pet_name:10} | {task}")
        return "\n".join(lines)
    def mark_task_complete(self, pet_name: str, description: str) -> str:
        """Mark a task complete and auto-schedule if recurring."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                for task in pet.tasks:
                    if task.description.lower() == description.lower() and not task.completed:
                        new_task = task.mark_complete()
                        if new_task:
                            pet.add_task(new_task)
                            return f"✅ '{description}' marked complete. Next occurrence added!"
                        return f"✅ '{description}' marked complete."
                return f"❌ Task '{description}' not found for {pet_name}."
        return f"❌ Pet '{pet_name}' not found."

    


