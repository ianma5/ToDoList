'''App code for the todolist'''

import customtkinter
import database
from tkcalendar import DateEntry
from datetime import datetime

class NewWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("250x500")
        self.attributes('-topmost', True)
        self.title("Add/Edit Tasks")
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.checkboxes = []
        self.labels = []
        self.toplevel_window = None
        self.textbox = None
        self.date_picker = None

        self.load_tasks()

    def new_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():

            self.toplevel_window = NewWindow(self)

            self.textbox = customtkinter.CTkTextbox(self.toplevel_window)
            self.textbox.grid(row=0, column=0, padx=10,pady=10,sticky="nsew")
        
            #add the date picker
            self.date_picker = DateEntry(self.toplevel_window, width=12, background='black', foreground='white', borderwidth=2)
            self.date_picker.grid(row=1, column=0, padx=20, pady=10, sticky='ew')

            self.add_task_button = customtkinter.CTkButton(self.toplevel_window, text="Add Task",command=self.add_checkbox)
            self.add_task_button.grid(row=2, column=0, padx=10, pady=10)

            self.edit_checkbox_button = customtkinter.CTkButton(self.toplevel_window, text="Edit Task",command=self.edit_checkbox)
            self.edit_checkbox_button.grid(row=3, column=0, padx=10, pady=10)

        else:
            self.toplevel_window.focus()  # if window exists focus it

    def load_tasks(self, task_name=None):
        tasks = database.list_tasks() # returns the tasks
        if task_name:
            for task in tasks:
                if task[1]==task_name:
                    return task[0]
        else:
            for task in tasks:
                task_id = task[0]
                task_text = task[1]
                date_created = task[2]
                date_due = task[3]
                checked_variable = task[4]

                self.add_checkbox(task_text=task_text, checked_variable=checked_variable, date_created = date_created, date_due=date_due, task_id=task_id) # adds pre-existing tasks from the database
        

    def add_checkbox(self, task_text=None, checked_variable=False, date_due = None,date_created=None, task_id=None):
        if task_text is None and self.toplevel_window: # Check if this variable is passed, otherwise get from the textbox and pass to the database
            # If the window is open, that means that the user is inputting a task
            task_text = self.textbox.get(0.0,'end').strip()

            #check if the length of the string is >70 characters, slice the string at 70 chrs
            if len(task_text)>70: task_text = task_text[:70] 

            #create the task in the database
            date_created = datetime.now().strftime("%m-%d-%y %I:%M %p")
            date_due = self.date_picker.get_date().strftime('%m-%d-%y'+' 11:59 PM')
            database.create_task(task_text, date_created, date_due, 0)
            self.toplevel_window.destroy()
            self.toplevel_window = None
        if task_text: #check the string contains any characters, this is for creating the actual frame on the screen
            tasksamt = len(self.checkboxes) # number of tasks based on amount of items in the checkbox list

            frame = customtkinter.CTkCheckBox(self, text=task_text, command=lambda: self.mark_box(task_id,frame.get())) # create a checkbox for the task

            # if the task is marked as completed, select the checkbox
            if checked_variable: frame.select()

            frame.grid(row=tasksamt+1,column=0,padx=10,pady=10, sticky='w')
            if task_id == None: task_id = self.load_tasks(task_name=task_text) # If there is no task_id, get it from the function
            self.checkboxes.append((task_id,frame)) # Add to list of checkboxes
        
            # create a label for the time task was created and append it to list of labels    
            created_label = customtkinter.CTkLabel(self, text="Created Date: \n"+ date_created)
            created_label.grid(row=tasksamt+1,column = 1, padx=20, pady=5, sticky='e')
            self.labels.append(created_label)

            # create another label for the time the task is due
            due_label = customtkinter.CTkLabel(self, text="Due Date: \n"+date_due)
            due_label.grid(row=tasksamt+1,column = 2, padx=20, pady=5, sticky='e')
            self.labels.append(due_label)

    def remove_checkbox(self):
        boxes = self.get()
        for box in (boxes):
            task_id, checkbox = box
            database.delete_task(task_id)
            taken_index = self.checkboxes.index((task_id,checkbox))
            checkbox.destroy()
            label = self.labels.pop(taken_index*2)
            label.destroy()

            label = self.labels.pop(taken_index*2)
            label.destroy()

            self.checkboxes.pop(taken_index)
    
    def edit_checkbox(self):
        new_text = self.textbox.get(0.0,'end').strip()
        if len(new_text)==0: return
        boxes = self.get()
        if len(boxes)>1:
            return
        elif len(boxes)==1:
            task_id, checkbox = boxes[0]
            checkbox.configure(self, text=new_text, command=lambda: self.mark_box(task_id, checkbox.get()))
            self.textbox.delete("1.0", 'end')
            database.update_task(new_text, task_id)
            

    def mark_box(self, task_id, checked):
        database.mark_task(task_id, checked)

    def get(self):
        checked_checkboxes = []
        for task_id, checkbox in self.checkboxes:
            if checkbox.get() == 1: # its checked
                checked_checkboxes.append((task_id, checkbox))
        return checked_checkboxes
        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.geometry("800x580")
        self.title("ToDoList")
        
        database.create_table() # Initialize table if not already created

        # grid layout configuration

        self.grid_columnconfigure(0, weight=0)  # sidebar column for buttons
        self.grid_columnconfigure(1, weight=1)  # main frame for task list
        self.grid_rowconfigure(0, weight=0)  # for buttons
        self.grid_rowconfigure(1, weight=1)  # for the task list frame
        
        # Create the task frame
        self.my_frame = ScrollFrame(master=self, label_text="Task List")
        self.my_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')

        # Open new task window toggle button
        self.toggle_button = customtkinter.CTkButton(self, text="+", width=30, command=self.my_frame.new_window)
        self.toggle_button.grid(row=0, column=0, padx=5, pady=(10,5), sticky='n')

        # Remove task button
        self.remove_task_button = customtkinter.CTkButton(self, text="-", width=30, command=self.my_frame.remove_checkbox)
        self.remove_task_button.grid(row=1, column=0, padx=5, pady=5, sticky='n')


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
