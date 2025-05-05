from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from course import CourseClass
from student import StudentClass
from result import ResultClass
class SRMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1800x800+0+0")
        self.root.config(bg = "white")

        self.logo_dash= ImageTk.PhotoImage(file= "images/logo_p.png")
        
        #title
        title = Label(self.root, text = "Student Result Management System", padx= 10, compound=LEFT, image=self.logo_dash, font = ("goudy old style", 20, "bold"), bg= "#033054", fg= "white").place(x=0, y=0, relwidth=1, height=50)

        M_Frame= LabelFrame(self.root, text= "Menu", font=("times new roman", 15), bg= "white")
        number_of_buttons = 3
        btn_width = 200
        spacing = 10
        frame_width = number_of_buttons * btn_width + (number_of_buttons - 1) * spacing
        M_Frame.place(x=10, y=70, width=frame_width, height=80)


        #widgets
        btn_width = 200
        spacing = 10
        x_start = 10

        btn_course= Button(M_Frame, text= "Course", font=("goudy old style", 20, "bold"), bg= "#033054", fg= "white", cursor= "hand2", command=self.add_course).place(x=x_start, y=5, width=btn_width, height=40)
        x_start += btn_width + spacing

        btn_students= Button(M_Frame, text= "Students", font=("goudy old style", 20, "bold"), bg= "#033054", fg= "white", cursor= "hand2", command=self.add_student).place(x=x_start, y=5, width=btn_width, height=40)
        x_start += btn_width + spacing

        btn_result= Button(M_Frame, text= "Result", font=("goudy old style", 20, "bold"), bg= "#033054", fg= "white", cursor= "hand2", command=self.add_result).place(x=x_start, y=5, width=btn_width, height=40)
        x_start += btn_width + spacing

        self.bg_image= Image.open("images/student.logo.png")
        self.bg_image= self.bg_image.resize((950, 800))
        self.bg_image= ImageTk.PhotoImage(self.bg_image)

        self.bg_ima= Image.open("images/bg.png")
        self.bg_ima= self.bg_ima.resize((950, 800))
        self.bg_ima= ImageTk.PhotoImage(self.bg_ima)

        self.lbl_bg= Label(self.root, image= self.bg_image).place(x=700, y=180, width=950, height=500)
        self.lbl_bg_ima= Label(self.root, image= self.bg_ima).place(x=10, y=180, width=770, height=450)
        overview= Label(self.root, text= '''The system would store student information and Result in a database, allowing users to:
Insert student data and result
Multiple Courses for Students to Pick
Retrieve student results for a specific student or all students
Delete student data''', font= ("goudy old style", 13), bg= "white", fg="#033054", bd=5, relief=SOLID,).place(x=830, y=640)


        self.b_lbl_course= Label(self.root, text= "Total Courses\n [ 0 ]", font=("goudy old style", 20),fg="white", bd=10, relief= RIDGE, bg= "dark red", cursor="hand2")
        self.b_lbl_course.place(x=10, y=650, width= 250, height= 100)

        self.b_lbl_student= Label(self.root, text= "Total Students\n [ 0 ]", font=("goudy old style", 20),fg="white", bd=10, relief= RIDGE, bg= "dark red", cursor="hand2")
        self.b_lbl_student.place(x=270, y=650, width= 250, height= 100)

        self.b_lbl_result= Label(self.root, text= "Total Results\n [ 0 ]", font=("goudy old style", 20),fg="white", bd=10, relief= RIDGE, bg= "dark red", cursor="hand2")
        self.b_lbl_result.place(x=530, y=650, width= 250, height= 100)
        
        #footer
        footer = Label(self.root, text = "SRMS - Student Result Management System\n Contact 8879416401 or abdulhadee814@gmail.com for any technical issues", font = ("goudy old style", 10, "bold"), bg= "black", fg= "white").pack(side=BOTTOM, fill= X)
        self.update_details()
    
    def update_details(self):
        con=sqlite3.connect(database="database_srms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from course")
            cr = cur.fetchall()
            self.b_lbl_course.config(text=f"Total Courses\n[ {len(cr)} ]")
           
            cur.execute("select * from student")
            cr = cur.fetchall()
            self.b_lbl_student.config(text=f"Total Students\n[ {len(cr)} ]")

            cur.execute("select * from result")
            cr = cur.fetchall()
            self.b_lbl_result.config(text=f"Total Result\n[ {len(cr)} ]")
            
            
            self.b_lbl_course.after(200, self.update_details)
               
        except Exception as ex:
             messagebox.showerror("Error", f"Error due to {str(ex)}")
    

        
    
    
    def add_course(self):
        self.new_win=Toplevel(self.root) 
        self.obj=CourseClass(self.new_win)

    def add_student(self):
        self.new_win=Toplevel(self.root) 
        self.obj=StudentClass(self.new_win)

    def add_result(self):
        self.new_win=Toplevel(self.root) 
        self.obj=ResultClass(self.new_win)  
               
if __name__ ==  "__main__":
    root = Tk()
    obj = SRMS(root)
    root.mainloop()


        