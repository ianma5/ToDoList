import customtkinter
import database
from datetime import datetime

'''Add editing name feature, sync to calendar? display date created/due, fix incrementing? add due date feature'''

class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, textbox, **kwargs):
        super().__init__(master, **kwargs)

        self.checkboxes = []
        self.labels = []

        self.textbox = textbox
        self.load_tasks()

    def load_tasks(self):
        tasks = database.list_tasks()
        for task in tasks:
            date_created = task[2]
            date_due = task[3]
            checked_variable = task[4]

            self.add_checkbox(task_text=task[1], checked_variable=checked_variable, date_created = date_created, date_due=date_due)

    def add_checkbox(self, task_text=None, checked_variable=False, date_due = None,date_created=None):
        if task_text is None: #Check if this variable is passed, otherwise get from the textbox
            task_text = self.textbox.get(0.0,'end').strip()
            date_created = datetime.now().strftime("%m-%d-%y %I:%M %p")
            date_due = datetime.now().strftime("%m-%d-%y %I:%M %p")
            date_due="09-02-24 11:59 PM"

            database.create_task(task_text)

        if task_text: #check the string contains any characters
            tasksamt = len(self.checkboxes)
            frame = customtkinter.CTkCheckBox(self, text=task_text, command=lambda: self.mark_box(task_text,frame.get()))
            if checked_variable: frame.select()
            frame.grid(row=tasksamt+1,column=0,padx=10,pady=10, sticky='w')
            self.checkboxes.append(frame)
            self.textbox.delete("1.0", 'end')

                
            created_label = customtkinter.CTkLabel(self, text="Created Date: \n"+ date_created)
            created_label.grid(row=tasksamt+1,column = 1, padx=20, pady=5, sticky='e')
            self.labels.append(created_label)

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
        self.sidebar_frame = customtkinter.CTkFrame(self,width=140,corner_radius=0)
        self.sidebar_frame.grid(row=0,column=0,rowspan=4,sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4,weight=1) # allow space at the bottom

        self.sidebar_frame.grid_rowconfigure(0, weight=0)  # Top row (button)
        self.sidebar_frame.grid_rowconfigure(1, weight=0)  # Second row (button)
        self.sidebar_frame.grid_rowconfigure(2, weight=0)  # Remaining space (pushes buttons to the top)
        self.sidebar_frame.grid_rowconfigure(3, weight=1)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_frame_label = customtkinter.CTkLabel(self.sidebar_frame,text="Settings")
        self.sidebar_frame_label.grid(row=0, column=0, padx=10, pady=(20,10))
         # add textbox tosidebar
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame)
        self.textbox.grid(row=3, column=0, padx=10,pady=10,sticky="nsew")

        #task list scrollframe
        self.my_frame = ScrollFrame(master=self,label_text="Task List", textbox = self.textbox)
        self.my_frame.grid(row=0,column=1,padx=10,pady=10, sticky='nsew')

        #add buttons to sidebar

        self.add_task_button = customtkinter.CTkButton(self.sidebar_frame, text="Add Task",command=self.my_frame.add_checkbox)
        self.add_task_button.grid(row=1, column=0, padx=10, pady=10)

        self.remove_task_button = customtkinter.CTkButton(self.sidebar_frame, text="Remove Task",command=self.my_frame.remove_checkbox)
        self.remove_task_button.grid(row=2, column=0, padx=10, pady=10)

       

app = App()
app.mainloop()