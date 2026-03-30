# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
1. Add owner and pet info - Enter basic details about the owner and their pet 
2. Add and manage tasks -- Create care tasks( walks, feeding, med, etc) with duration and priority 
3. Generate and view a daily plan -- Get a scheduled plan for the day based on constraints and priorities, with an explanation of why taks were ordered that way. 

I designed four classes:

- Task: Represents a single care activity. It stores a description, 
  duration, priority, frequency, and completion status. It can mark 
  itself complete.

- Pet: Stores the pet's name, species, age, allergies, and preferences. 
  It holds a list of tasks and can add new ones.

- Owner: Holds the owner's name and a list of their pets. It can add 
  pets and retrieve all tasks across all pets.

- Scheduler: The brain of the app. It references the Owner and handles 
  generating the schedule, sorting by priority, detecting conflicts, 
  and filtering tasks.

**b. Design changes**

The mark_complete() method was originally just a simple boolean toggle. I updated it to also return a new Task object for recurring tasks (daily/weekly), so the Scheduler could automatically add the next occurrence. This kept recurrence logic inside the Task class where it belongs.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**
The scheduler considers priority (high, medium, low) and completion status. Priority was the most important constraint because a pet owner needs to know which tasks are critical (like medication) vs optional (like playtime).

**b. Tradeoffs**
The scheduler considers priority (high, medium, low) and completion status. Priority was the most important constraint because a pet owner needs to know which tasks are critical (like medication) vs optional (like playtime).
---

## 3. AI Collaboration

**a. How you used AI**
I used AI for design brainstorming (identifying class attributes), debugging (fixing indentation and typos in app.py), and generating code stubs. The most helpful prompts were specific ones like "add a mark_task_complete method to the Scheduler that handles recurring tasks."

**b. Judgment and verification**
The AI initially suggested a nested double loop for conflict detection (O(n²)). I replaced it with a single-pass dictionary approach which is cleaner and more efficient. I verified it by running main.py and checking that duplicate tasks were correctly flagged.

---

## 4. Testing and Verification

**a. What you tested**
I tested: task completion status change, recurring task creation for daily tasks, non-recurrence for once tasks, schedule filtering by status, priority sorting, and empty schedule edge cases. These were important because they cover the core scheduling behaviors the app relies on.

**b. Confidence**
⭐⭐⭐⭐ (4/5). The core logic is well tested. I would next test adding multiple pets with conflicting tasks, and testing the Streamlit session state behavior across multiple reruns.
---

## 5. Reflection

**a. What went well**
I am most satisfied with the Scheduler class. It cleanly separates the scheduling intelligence from the data storage, making it easy to extend with new features like recurring tasks and conflict detection.

**b. What you would improve**
I would add a time attribute to Task so the scheduler could detect overlapping durations, not just duplicate descriptions. I would also add support for multiple pets in the UI.
**c. Key takeaway**

AI is a powerful co-pilot but a poor architect. It accelerates boilerplate and surfaces options quickly, but every structural decision — which class owns which responsibility, what tradeoffs to accept — requires human judgment and oversight.

