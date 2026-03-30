from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner("Alex")

buddy = Pet(name="Buddy", species="Dog", age=3)
whiskers = Pet(name="Whiskers", species="Cat", age=5)

owner.add_pet(buddy)
owner.add_pet(whiskers)

# --- Add Tasks ---
buddy.add_task(Task("Morning Walk", 30, "high", "daily"))
buddy.add_task(Task("Evening Feed", 15, "medium", "daily"))
buddy.add_task(Task("Vet Checkup", 60, "high", "once"))

whiskers.add_task(Task("Morning Feed", 10, "high", "daily"))
whiskers.add_task(Task("Playtime", 20, "low", "daily"))

# --- Scheduler ---
scheduler = Scheduler(owner)

print(scheduler.todays_schedule())
print()

# --- Conflicts ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    for c in conflicts:
        print(c)
else:
    print("✅ No conflicts detected.")


# --- Test Recurring Tasks ---
print("\n--- Testing Recurring Tasks ---")
result = scheduler.mark_task_complete("Buddy", "Morning Walk")
print(result)

# Show updated task count
print(f"\nBuddy's tasks after completion: {len(buddy.tasks)}")
for task in buddy.tasks:
    print(f"  {task}")

