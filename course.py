from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x500+80+170")
        self.root.config(bg = "white")
        self.root.focus_force()

       #title
        title = Label(self.root, text = "Manage Course Details", font = ("goudy old style", 20, "bold"), bg= "#033054", fg= "white").place(x=10, y=15, width=1180, height=35)

        #variables
        self.var_course=StringVar()
        self.var_duration=StringVar()
        self.var_charges=StringVar()
        self.var_search=StringVar()

        #widgets
        lbl_courseName=Label(self.root, text="Course Name:", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        lbl_duration=Label(self.root, text="Duration:", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=100)
        lbl_charges=Label(self.root, text="Charges:", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=140)
        lbl_description=Label(self.root, text="Description:", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=180)

        #Entry Fields
        self.txt_courseName=Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_courseName.place(x=150, y=60, width=200)
        txt_duration=Entry(self.root, textvariable=self.var_duration, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=100, width=200)
        txt_courseName_charges=Entry(self.root, textvariable=self.var_charges, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=140, width=200)
        self.txt_description=Text(self.root, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_description.place(x=150, y=180, width=500, height=150)

        #Butons
        self.btn_save= Button(self.root, text="Save", font=("goudy old style",15,"bold"), fg="white", bd=5, relief= RIDGE, bg= "dark red", cursor="hand2", command=self.add)
        self.btn_save.place(x=150, y=400, width=110, height=40)
        
        self.btn_update= Button(self.root, text="Update", font=("goudy old style",15,"bold"), fg="white", bd=5, relief= RIDGE, bg= "dark red", cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=400, width=110, height=40)

        self.btn_delete= Button(self.root, text="Delete", font=("goudy old style",15,"bold"), fg="white", bd=5, relief= RIDGE, bg= "dark red", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=390, y=400, width=110, height=40)

        self.btn_clear= Button(self.root, text="Clear", font=("goudy old style",15,"bold"), fg="white", bd=5, relief= RIDGE, bg= "dark red", cursor="hand2", command= self.clear)
        self.btn_clear.place(x=510, y=400, width=110, height=40)

        #Search Panel
        lbl_search_courseName=Label(self.root, text="Course Name: ", font=("goudy old style", 15, "bold"), bg="white").place(x=720, y=60)
        txt_search_courseName=Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=870, y=60, width=180)
        btn_search=Button(self.root, text= "Search", font=("goudy old style", 15, "bold"), bg= "#03a9f4", fg= "white", cursor= "hand2", command=self.search).place(x=1070, y=60, width=110, height=28)

        #Content
        self.C_Frame=Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrolly=Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx=Scrollbar(self.C_Frame, orient=HORIZONTAL)
        
        self.CourseTable= ttk.Treeview(self.C_Frame, columns=("C_ID", "NAME", "DURATION", "CHARGES", "DESCRIPTION"), xscrollcommand=scrollx, yscrollcommand=scrolly)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill= Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)
        
        self.CourseTable.heading("C_ID", text="Course ID")
        self.CourseTable.heading("NAME", text="Name")
        self.CourseTable.heading("DURATION", text="Duration")
        self.CourseTable.heading("CHARGES", text="Charges")
        self.CourseTable.heading("DESCRIPTION", text="Description")
        self.CourseTable["show"]="headings"
        self.CourseTable.column("C_ID", width=100)
        self.CourseTable.column("NAME", width=100)
        self.CourseTable.column("DURATION", width=100)
        self.CourseTable.column("CHARGES", width=100)
        self.CourseTable.column("DESCRIPTION", width=150)
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()


    #functions==================

    def delete(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error", "Course Name is Required", parent=self.root)
            else:
                cur.execute("select * from course where NAME=?", (self.var_course.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Select Course from List", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete the course", parent=self.root)
                    if op==True:
                        cur.execute("delete from course where NAME=?", (self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Succes", "Course Deleted Succesfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.txt_description.delete("1.0", END)
        self.var_search.set("")
        self.txt_courseName.config(state=NORMAL)



    def get_data(self, ev):
        self.txt_courseName.config(state="readonly")
        r=self.CourseTable.focus()
        content=self.CourseTable.item(r)
        row=content["values"]
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete("1.0", END)
        self.txt_description.insert(END, row[4])



    def add(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error", "Course Name is Required", parent=self.root)
            else:
                cur.execute("select * from course where NAME=?", (self.var_course.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "Course Name is already available", parent=self.root)
                else:
                    cur.execute("insert into course (NAME, DURATION, CHARGES, DESCRIPTION) values(?,?,?,?)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END)                    
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Added Succesfully!", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


    
    def update(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error", "Course Name is Required", parent=self.root)
            else:
                cur.execute("select * from course where NAME=?", (self.var_course.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Select Course from List", parent=self.root)
                else:
                    cur.execute("update course set DURATION=?, CHARGES=?, DESCRIPTION=? where NAME=?", (
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END),
                        self.var_course.get()                   
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Updated Succesfully!", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")




    def show(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from course")
            rows=cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert("", END, values=row)
               
        except Exception as ex:
             messagebox.showerror("Error", f"Error due to {str(ex)}")


    def search(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            cur.execute(f"select * from course where NAME LIKE '%{self.var_search.get()}%'")
            rows=cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert("", END, values=row)
               
        except Exception as ex:
             messagebox.showerror("Error", f"Error due to {str(ex)}")



             

if __name__ ==  "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()