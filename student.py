from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x500+80+170")
        self.root.config(bg = "white")
        self.root.focus_force()

       #title
        title = Label(self.root, text = "Manage Student Details", font = ("goudy old style", 20, "bold"), bg= "#033054", fg= "white").place(x=10, y=15, width=1180, height=35)

        #variables
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_email=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_contact=StringVar()
        self.var_admission=StringVar()
        self.var_course=StringVar()
        self.var_search=StringVar()

        #widgets
        lbl_rollNO=Label(self.root, text=" Roll No:", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        lbl_name=Label(self.root, text="Name:", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=100)
        lbl_email=Label(self.root, text="Email:", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=140)
        lbl_gender=Label(self.root, text="Gender:", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=180)
        lbl_addressr=Label(self.root, text="Address:", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=260)
        
        lbl_dob=Label(self.root, text="DOB:", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=60)
        lbl_contact=Label(self.root, text="Contact:", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=100)
        lbl_admission=Label(self.root, text="Admission:", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=140)
        lbl_course=Label(self.root, text="Course:", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=180)
       
       
        self.courselist=["Select Course"]
        #functions to call
        self.fetch_course()
        
        
        #Entry Fields
        self.txt_rollNO=Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_rollNO.place(x=130, y=60, width=200)
        txt_name=Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=130, y=100, width=200)
        txt_email=Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=130, y=140, width=200)
        self.txt_gender=ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female"), state='readonly', justify=CENTER, font=("goudy old style", 15, "bold"))
        self.txt_gender.place(x=130, y=180, width=200)
        self.txt_gender.current(0)

        txt_dob=Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=480, y=60, width=200)
        txt_contact=Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=480, y=100, width=200)
        txt_admission=Entry(self.root, textvariable=self.var_admission, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=480, y=140, width=200)
        self.txt_course=ttk.Combobox(self.root, textvariable=self.var_course, values=(self.courselist), state='readonly', justify=CENTER, font=("goudy old style", 15, "bold"))
        self.txt_course.place(x=480, y=180, width=200)
        self.txt_course.current(0)

        self.txt_address=Text(self.root, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_address.place(x=130, y=260, width=500, height=100)

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
        lbl_search_rollNO=Label(self.root, text="Roll No: ", font=("goudy old style", 15, "bold"), bg="white").place(x=720, y=60)
        txt_search_rollNO=Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=870, y=60, width=180)
        btn_search=Button(self.root, text= "Search", font=("goudy old style", 15, "bold"), bg= "#03a9f4", fg= "white", cursor= "hand2", command=self.search).place(x=1070, y=60, width=110, height=28)

        #Content
        self.S_Frame=Frame(self.root, bd=2, relief=RIDGE)
        self.S_Frame.place(x=720, y=100, width=470, height=340)

        scrolly=Scrollbar(self.S_Frame, orient=VERTICAL)
        scrollx=Scrollbar(self.S_Frame, orient=HORIZONTAL)

        
        
        self.StudentTable = ttk.Treeview(self.S_Frame, columns=("roll_no", "name", "email", "gender", "dob", "contact", "admission", "course", "address"), xscrollcommand=scrollx, yscrollcommand=scrolly)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill= Y)
        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)

        self.StudentTable.heading("roll_no", text="Roll No")
        self.StudentTable.heading("name", text="Name")
        self.StudentTable.heading("email", text="Email")
        self.StudentTable.heading("gender", text="Gender")
        self.StudentTable.heading("dob", text="D.O.B")
        self.StudentTable.heading("contact", text="Contact")
        self.StudentTable.heading("admission", text="Admission")
        self.StudentTable.heading("course", text="Course")
        self.StudentTable.heading("address", text="Address")

        self.StudentTable["show"] = "headings"

        self.StudentTable.column("roll_no", width=100)
        self.StudentTable.column("name", width=100)
        self.StudentTable.column("email", width=150)
        self.StudentTable.column("gender", width=80)
        self.StudentTable.column("dob", width=100)
        self.StudentTable.column("contact", width=100)
        self.StudentTable.column("admission", width=100)
        self.StudentTable.column("course", width=100)
        self.StudentTable.column("address", width=150)
       
        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()



        
        


    #functions==================

    def delete(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            if self.var_roll.get()=="":
                messagebox.showerror("Error", "Course Name is Required", parent=self.root)
            else:
                cur.execute("select * from student where roll_no=?", (self.var_roll.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Select Course from List", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete the course", parent=self.root)
                    if op==True:
                        cur.execute("delete from student where roll_no=?", (self.var_roll.get(),))
                        con.commit()
                        messagebox.showinfo("Succes", "Course Deleted Succesfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.show()
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.txt_address.delete("1.0", END)
        self.var_gender.set("")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_course.set("")
        self.var_admission.set("")
        self.txt_rollNO.config(state=NORMAL)



    def get_data(self, ev):
        self.txt_rollNO.config(state="readonly")
        r=self.StudentTable.focus()
        content=self.StudentTable.item(r)
        row=content["values"]
        self.var_roll.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_dob.set(row[4])
        self.var_contact.set(row[5])
        self.var_admission.set(row[6])
        self.var_course.set(row[7])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert(END, row[8])


    def add(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            if self.var_roll.get()=="":
                messagebox.showerror("Error", "Roll Number is Required", parent=self.root)
            else:
                cur.execute("select * from student where roll_no=?", (self.var_roll.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "Roll Number is already available", parent=self.root)
                else:
                    cur.execute("insert into student(roll_no, name, email, gender, dob, contact, admission, course, address) values(?,?,?,?,?,?,?,?,?)", (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_contact.get(),
                        self.var_admission.get(),
                        self.var_course.get(),
                        self.txt_address.get("1.0", END)                    
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Added Succesfully!", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


    
    def update(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            if self.var_roll.get()=="":
                messagebox.showerror("Error", "Roll Number is Required", parent=self.root)
            else:
                cur.execute("select * from student where roll_no=?", (self.var_roll.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Select Student from List", parent=self.root)
                else:
                    cur.execute("update student set name=?, email=?, gender=?, dob=?, contact=?, admission=?, course=?, address=? where roll_no=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_contact.get(),
                        self.var_admission.get(),
                        self.var_course.get(),
                        self.txt_address.get("1.0", END),
                        self.var_roll.get()
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
            cur.execute("select * from student")
            rows=cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert("", END, values=row)
               
        except Exception as ex:
             messagebox.showerror("Error", f"Error due to {str(ex)}")
             

    def fetch_course(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            cur.execute("select name from course")
            rows=cur.fetchall()
            
            if len(rows) > 0:
                self.courselist = ["Select Course"] + [row[0] for row in rows]


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    


    def search(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            cur.execute(f"select * from student where roll_no=?", (self.var_roll.get(),))
            rows=cur.fetchone()
            if rows!=None:
                self.StudentTable.delete(*self.StudentTable.get_children())
                for row in rows:
                    self.StudentTable.insert("", END, values=row)
            else:
                messagebox.showerror("Error","No Record Found", parent=self.root)
        except Exception as ex:
             messagebox.showerror("Error", f"Error due to {str(ex)}")




if __name__ ==  "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()