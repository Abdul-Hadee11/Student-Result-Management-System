from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("900x500+100+100")
        self.root.config(bg="white")

        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()

        title = Label(self.root, text="Manage Student Results", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, relwidth=1)

        lbl_select = Label(self.root, text="Select Roll No.", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=100)
        self.roll_list = []
        self.fetch_roll()
        self.combo_roll = ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list, font=("goudy old style", 13), state='readonly', justify=CENTER)
        self.combo_roll.place(x=200, y=100, width=200)
        self.combo_roll.bind("<<ComboboxSelected>>", self.fetch_student)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=150)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow", state='readonly').place(x=200, y=150, width=300)

        lbl_course = Label(self.root, text="Course", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=200)
        txt_course = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15), bg="lightyellow", state='readonly').place(x=200, y=200, width=300)

        lbl_marks = Label(self.root, text="Marks Obtained", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=250)
        txt_marks = Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 15), bg="lightyellow").place(x=230, y=250, width=300)

        btn_add = Button(self.root, text="Add", font=("goudy old style", 15), bg="#2196f3", fg="white", command=self.add).place(x=200, y=300, width=100)
        btn_update = Button(self.root, text="Update", font=("goudy old style", 15), bg="#4caf50", fg="white", command=self.update).place(x=310, y=300, width=100)
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15), bg="#f44336", fg="white", command=self.delete).place(x=420, y=300, width=100)

        

        self.R_Frame=Frame(self.root, bd=2, relief=RIDGE)
        self.R_Frame.place(x=10, y=350, width=880, height=140)
        scrolly=Scrollbar(self.R_Frame, orient=VERTICAL)
        
        self.result_table= ttk.Treeview(self.R_Frame, columns=("select_stud", "name", "course", "marks"), yscrollcommand=scrolly)
        scrolly.pack(side=RIGHT, fill= Y)
        scrolly.config(command=self.result_table.yview)
        
        self.result_table.heading("select_stud", text="Roll_no")
        self.result_table.heading("name", text="Name")
        self.result_table.heading("course", text="Course")
        self.result_table.heading("marks", text="Marks Obtained")
        
        self.result_table["show"]="headings"
        
        self.result_table.column("select_stud", width=100)
        self.result_table.column("name", width=100)
        self.result_table.column("course", width=100)
        self.result_table.column("marks", width=100)
        
        self.result_table.pack(fill=BOTH, expand=1)
        self.result_table.bind("<ButtonRelease-1>",self.get_data)
        self.show()

    def fetch_roll(self):
        con = sqlite3.connect("database_srms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll_no FROM student")
            rows = cur.fetchall()
            self.roll_list = [row[0] for row in rows]
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        con.close()

    def fetch_student(self, ev):
        con = sqlite3.connect("database_srms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name, course FROM student WHERE roll_no=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        con.close()

    def add(self):
        if self.var_roll.get() == "" or self.var_marks.get() == "":
            messagebox.showerror("Error", "All fields are required")
            return
        con = sqlite3.connect("database_srms.db")
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO result (select_stud, name, course, marks) VALUES (?, ?, ?, ?)", (
                self.var_roll.get(),
                self.var_name.get(),
                self.var_course.get(),
                self.var_marks.get()
            ))
            con.commit()
            messagebox.showinfo("Success", "Result added successfully")
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        con.close()

    def update(self):
        con = sqlite3.connect("database_srms.db")
        cur = con.cursor()
        try:
            cur.execute("UPDATE result SET name=?, course=?, marks=? WHERE select_stud=?", (
                self.var_name.get(),
                self.var_course.get(),
                self.var_marks.get(),
                self.var_roll.get()
            ))
            con.commit()
            messagebox.showinfo("Success", "Result updated successfully")
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        con.close()

    def delete(self):
        con = sqlite3.connect("database_srms.db")
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM result WHERE select_stud=?", (self.var_roll.get(),))
            con.commit()
            messagebox.showinfo("Deleted", "Result deleted successfully")
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        con.close()

    def show(self):
        con = sqlite3.connect("database_srms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM result")
            rows = cur.fetchall()
            self.result_table.delete(*self.result_table.get_children())
            for row in rows:
                self.result_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        con.close()

    def get_data(self, ev):
        selected = self.result_table.focus()
        content = self.result_table.item(selected)
        row = content['values']
        if row:
            self.var_roll.set(row[0])
            self.var_name.set(row[1])
            self.var_course.set(row[2])
            self.var_marks.set(row[3])



if __name__ ==  "__main__":
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()

    