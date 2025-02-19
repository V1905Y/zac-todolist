import streamlit as st
import json  # To save tasks persistently

# File to store tasks
TASKS_FILE = "tasks.json"
# Function to load tasks from a file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)  # TODO: Handle JSON errors properly!
    except FileNotFoundError:
        return []  # HINT: What should we return instead of None?
    except json.JSONDecodeError:
        return []  # HINT: If JSON is empty or corrupted, return an empty list

# Function to save tasks
def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file)
    except Exception as e:
        st.warning(f"Could not save tasks: {e}")  # HINT: Show a user-friendly message

# Function to add a new task
def add_task(task_text):
    if task_text.strip():
        tasks = st.session_state["tasks"]

        # HINT: Check if task_text already exists before appending
        # Convert everything to lowercase to avoid duplicates like "Homework" and "homework"
        if any(t["task"].lower() == task_text.lower() for t in tasks):
            st.warning("Task already exists!")  # HINT: Display a warning instead of adding
            return

        tasks.append({"task": task_text, "completed": False})
        save_tasks(tasks)
        st.session_state["tasks"] = tasks
        st.experimental_rerun()

# Function to toggle task completion
def toggle_task(index):
    tasks = st.session_state["tasks"]
    
    # TODO: Ensure this correctly flips the completed status of the task
    # HINT: Use `not` operator to toggle between True and False
    tasks[index]["completed"] = not tasks[index]["completed"]
    
    save_tasks(tasks)
    st.experimental_rerun()

# Function to delete a task
def delete_task(index):
    tasks = st.session_state["tasks"]

    # HINT: Instead of removing the first task (pop(0)), remove the correct one (pop(index))
    tasks.pop(index)  # FIXED: Now removes the correct task

    save_tasks(tasks)
    st.experimental_rerun()

# BONUS TODO: Add a feature to clear only completed tasks
# HINT: Use a list comprehension to filter out completed tasks
# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state["tasks"] = load_tasks()

st.title("📝 Simple To-Do List")

# Input field for adding new tasks
new_task = st.text_input("Enter a new task", "")

if st.button("Add Task"):
    add_task(new_task)  # This function needs to be completed properly

# Display tasks
st.subheader("Your Tasks:")

if st.session_state["tasks"]:
    for i, task in enumerate(st.session_state["tasks"]):
        col1, col2 = st.columns([0.85, 0.15])

        # Checkbox to mark task as completed
        completed = col1.checkbox(task["task"], value=task["completed"], key=f"task_{i}")
        if completed != task["completed"]:
            toggle_task(i)  # Function needs fixing!

        # Delete button
        if col2.button("❌", key=f"delete_{i}"):
            delete_task(i)  # Function needs fixing!

else:
    st.write("No tasks added yet. Add a task above!")

# TODO: Add a feature to clear only completed tasks
