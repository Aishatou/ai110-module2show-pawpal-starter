import streamlit as st 
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session State --- : Keep owner alive between reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = None

st.title("🐾 PawPal+")
# --- Step 1 : Owner + Pet Setup ---
st.subheader("👤 Owner & Pet Info")

owner_name = st.text_input("Owner Name", value = "Jordan")
pet_name = st.text_input("Pet Name", value = "Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet Age", min_value=0, max_value=30, value=2)

if st.button("Set Owner & Pet"): 
     pet = Pet(name=pet_name, species=species, age=age)
     owner = Owner(name=owner_name)
     owner.add_pet(pet)
     st.session_state.owner = owner
     st.success(f"✅ {owner_name}'s pet {pet_name} is ready!")

#st.markdown(
    #"""
# Welcome to the PawPal+ starter app.

# This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
#but **it does not implement the project logic**. Your job is to design the system and build it.

# Use this app as your interactive demo once your backend classes/functions exist.
#"""
# )

#with st.expander("Scenario", expanded=True):
    #st.markdown(
       # """
#**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
#for their pet(s) based on constraints like time, priority, and preferences.

#You will design and implement the scheduling logic and connect it to this Streamlit UI.
#"""
    #)

#with st.expander("What you need to build", expanded=True):
    #st.markdown(
        #"""
#At minimum, your system should:
#- Represent pet care tasks (what needs to happen, how long it takes, priority)
#- Represent the pet and the owner (basic info and preferences)
#- Build a plan/schedule for a day that chooses and orders tasks based on constraints
#- Explain the plan (why each task was chosen and when it happens)
#"""
    #)

st.divider()
# --- Step 2 : Add Tasks ---
st.subheader("📝 Add Tasks")


#st.markdown("### Tasks")
#st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if st.session_state.owner is None:
    st.info("Set your owner and pet above first.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (mins)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["high", "medium", "low"])
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "once", "weekly"])

    if st.button("Add Task"):
        if task_title.strip():
            pet = st.session_state.owner.pets[0]
            pet.add_task(Task(task_title.strip(), int(duration), priority, frequency))
            st.success(f"Added '{task_title}'!")
        else:
            st.error("Please enter a task name.")
#if st.session_state.tasks:
    #st.write("Current tasks:")
    #st.table(st.session_state.tasks)
#else:
    #st.info("No tasks yet. Add one above.")

st.divider()
# --- Step 3 : Generate Daily Schedule ---

st.subheader("📅 Generate Daily Schedule")
#st.caption("This button should call your scheduling logic once you implement it.")
if st.session_state.owner is None:
    st.info("Set your owner and pet above first.")
else:
    scheduler = Scheduler(st.session_state.owner)

    # Conflict warnings always visible
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.subheader("⚠️ Conflicts Detected")
        for c in conflicts:
            st.warning(c)

    if st.button("Generate Schedule"):
        schedule = scheduler.generate_schedule()

        if not schedule:
            st.warning("No pending tasks found!")
        else:
            st.success("Here's your plan for today, sorted by priority:")
            table = []
            for pname, task in schedule:
                table.append({
                    "Pet": pname,
                    "Task": task.description,
                    "Duration": f"{task.duration} mins",
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Status": "✅ Done" if task.completed else "⬜ Pending"
                })
            st.table(table)

    # --- Mark Task Complete ---
    st.subheader("✅ Mark Task Complete")
    pending = scheduler.filter_by_status(False)
    if pending:
        options = [f"{n} — {t.description}" for n, t in pending]
        choice = st.selectbox("Select task to complete", options)
        if st.button("Mark Complete"):
            idx = options.index(choice)
            pname, task = pending[idx]
            result = scheduler.mark_task_complete(pname, task.description)
            st.success(result)
            st.rerun()
    else:
        st.success("🎉 All tasks are complete for today!")
#if st.button("Generate schedule"):
    #st.warning(
        #"Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    #)
    #st.markdown(
       # """
#Suggested approach:
#1. Design your UML (draft).
#2. Create class stubs (no logic).
#3. Implement scheduling behavior.
#4. Connect your scheduler here and display results.
#"""
    #)


