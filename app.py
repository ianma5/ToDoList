'''Central code for the todolist.'''

import customtkinter
import database
from tkcalendar import DateEntry
from datetime import datetime

'''Add editing name feature, sync to calendar? display date created/due, fix incrementing? add due date feature'''

class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, textbox, date_picker, **kwargs):
        super().__init__(master, **kwargs)

        self.checkboxes = []
        self.labels = []

        self.textbox = textbox # reference to textbox
        
        #self.sidelabel = sidelabel # title above textbox
        self.date_picker = date_picker
        self.load_tasks()
        
    def load_tasks(self):
        tasks = database.list_tasks() # returns the tasks
        for task in tasks:
            date_created = task[2]
            date_due = task[3]
            checked_variable = task[4]

            self.add_checkbox(task_text=task[1], checked_variable=checked_variable, date_created = date_created, date_due=date_due) # adds pre-existing tasks from the database

    def add_checkbox(self, task_text=None, checked_variable=False, date_due = None,date_created=None):
        if task_text is None: # Check if this variable is passed, otherwise get from the textbox
            task_text = self.textbox.get(0.0,'end').strip()
            if task_text: # check if there are any characters
                date_created = datetime.now().strftime("%m-%d-%y %I:%M %p")
                date_due = self.date_picker.get_date().strftime("%m-%d-%y")

                database.create_task(task_text)

        if task_text: #check the string contains any characters
            tasksamt = len(self.checkboxes) # number of tasks based on amount of items in the checkbox list

            frame = customtkinter.CTkCheckBox(self, text=task_text, command=lambda: self.mark_box(task_text,frame.get()))

            # if the task is marked as completed, select the checkbox
            if checked_variable: frame.select()

            frame.grid(row=tasksamt+1,column=0,padx=10,pady=10, sticky='w')
            self.checkboxes.append(frame)
            self.textbox.delete("1.0", 'end')

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
            database.delete_task(box.cget('text'))
            taken_index = self.checkboxes.index(box)
            box.destroy()
            #print(taken_index)
            label = self.labels.pop(taken_index*2)
            label.destroy()

            label = self.labels.pop(taken_index*2)
            label.destroy()

            self.checkboxes.pop(taken_index)
            

    def mark_box(self, task_name, checked):
        database.mark_task(task_name, checked)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1: # its checked
                checked_checkboxes.append(checkbox)
        return checked_checkboxes

class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, master, sidebar_visible, **kwargs):
        super().__init__(master, **kwargs)
       
        self.sidebar_visible = sidebar_visible
    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.grid_remove()  # Hide the sidebar
            self.grid_columnconfigure(0, weight=0, minsize=0)  # Adjust grid configuration
        else:
            self.grid()  # Show the sidebar
            self.grid_columnconfigure(0, weight=0, minsize=140)  # Reset grid configuration
        self.sidebar_visible = not self.sidebar_visible
        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")
        self.geometry("800x580")
        self.title("ToDoList")
        database.create_table()

        # grid layout configuration

        self.grid_columnconfigure(0,weight=0) # sidebar column
        self.grid_columnconfigure(1, weight=1) # scrollframe column
        self.grid_rowconfigure(0, weight=1) # row for scrollframe

        #side bar configuration
        #self.sidebar_frame = customtkinter.CTkFrame(self,width=140,corner_radius=0)
        
        self.sidebar_visible = True
        self.sidebar_frame = SidebarFrame(master=self, width=140, corner_radius=0,sidebar_visible=self.sidebar_visible)

        self.sidebar_frame.grid(row=0,column=0,rowspan=4,sticky="nsew")
        self.sidebar_frame.grid_rowconfigure((0,1,2,3), weight=0)  # Top row (button)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_visible = True
        #self.my_frame = scroll_frame

        self.sidebar_frame_label = customtkinter.CTkLabel(self.sidebar_frame,text="Settings")
        self.sidebar_frame_label.grid(row=0, column=0, padx=10, pady=(20,10))

        self.sidebar_frame_instructions = customtkinter.CTkLabel(self.sidebar_frame,text="Enter your task:")
        self.sidebar_frame_instructions.grid(row=3, column=0, padx=10, pady=10)


         # add textbox tosidebar
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame)
        self.textbox.grid(row=4, column=0, padx=10,pady=10,sticky="nsew")

        self.date_picker = DateEntry(self.sidebar_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_picker.grid(row=5, column=0, padx=10, pady=10)

        self.my_frame = ScrollFrame(master=self,label_text="Task List", textbox = self.textbox, date_picker=self.date_picker)
        self.my_frame.grid(row=0,column=1,padx=10,pady=10, sticky='nsew')

        self.add_task_button = customtkinter.CTkButton(self.sidebar_frame, text="Add Task",command=self.my_frame.add_checkbox)
        self.add_task_button.grid(row=1, column=0, padx=10, pady=10)

        self.remove_task_button = customtkinter.CTkButton(self.sidebar_frame, text="Remove Task",command=self.my_frame.remove_checkbox)
        self.remove_task_button.grid(row=2, column=0, padx=10, pady=10)

        self.toggle_button = customtkinter.CTkButton(self, text="☰", width=30, command=self.sidebar_frame.toggle_sidebar)
        self.toggle_button.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
          #task list scrollframe
        
       
if __name__== "__main__":
    app = App()
    app.mainloop()