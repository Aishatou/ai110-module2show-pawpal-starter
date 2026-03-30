import pytest
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Fixtures ---
@pytest.fixture
def sample_owner():
    owner = Owner("Test Owner")
    dog = Pet("Rex", "Dog", 4)
    cat = Pet("Luna", "Cat", 2)
    dog.add_task(Task("Morning Walk", 30, "high", "daily"))
    dog.add_task(Task("Evening Feed", 15, "medium", "daily"))
    cat.add_task(Task("Playtime", 20, "low", "daily"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner

# --- Task Tests ---
def test_mark_complete_changes_status():
    """mark_complete() should set task.completed to True."""
    task = Task("Feed", 10, "high", "once")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True

def test_add_task_increases_count():
    """Adding a task should increase the pet's task count."""
    pet = Pet("Spot", "Dog", 2)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", 20, "medium", "daily"))
    assert len(pet.tasks) == 1

# --- Scheduler Tests ---
def test_sort_by_priority(sample_owner):
    """Tasks should be sorted high before medium before low."""
    scheduler = Scheduler(sample_owner)
    sorted_tasks = scheduler.sort_by_priority()
    priorities = [task.priority.lower() for _, task in sorted_tasks]
    priority_order = {"high": 1, "medium": 2, "low": 3}
    assert priorities == sorted(priorities, key=lambda x: priority_order[x])

def test_filter_by_status(sample_owner):
    """filter_by_status(False) should return only pending tasks."""
    scheduler = Scheduler(sample_owner)
    pending = scheduler.filter_by_status(False)
    assert all(not task.completed for _, task in pending)

def test_recurring_daily_task_creates_new_task():
    """Marking a daily task complete should add a new task for the pet."""
    owner = Owner("Test")
    pet = Pet("Rex", "Dog", 3)
    pet.add_task(Task("Morning Walk", 30, "high", "daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    
    initial_count = len(pet.tasks)
    scheduler.mark_task_complete("Rex", "Morning Walk")
    
    assert len(pet.tasks) == initial_count + 1

def test_once_task_does_not_recur():
    """Marking a 'once' task complete should NOT add a new task."""
    owner = Owner("Test")
    pet = Pet("Luna", "Cat", 2)
    pet.add_task(Task("Vet Visit", 60, "high", "once"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    
    initial_count = len(pet.tasks)
    scheduler.mark_task_complete("Luna", "Vet Visit")
    
    assert len(pet.tasks) == initial_count

    