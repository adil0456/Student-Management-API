from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI(title="Student Management")

class Student(BaseModel):
    ID: str
    name: str
    major: str
    
def read():
    with open("students.json", "r", encoding="utf-8") as file:
        students = json.load(file)
    return students

def save(students):
    with open("students.json", "w", encoding="utf-8") as file:
        json.dump(students, file, indent=2)

@app.get("/")
def home():
    return "Welcome to student management dashboard!"

@app.get("/students")
def getStudents():
    return read()

@app.post("/add")
def addStudent(student: Student):
    students = read()
    student = student.model_dump()
    for std in students:
        if std["ID"] == student["ID"]:
            return {"message": "This Student Already Exists!"}
    students.append(student)
    save(students)
    return {"message": "Student added", "data": student}

@app.put("/update")
def updateInfo(student: Student):
    students = read()
    student = student.model_dump()
    for std in students:
        if std["ID"] == student["ID"]:
            std["name"] = student["name"]
            std["major"] = student["major"]
            save(students)
            return {"message": "Student Updated!"}
    return {"message": "Student Not Found!"}

@app.delete("/delete/{ID}")
def deleteStudent(ID: str):
    students = read()
    for student in students:
        if student["ID"] == ID:
            students.remove(student)
            save(students)
            return {"message": "Student Removed!"}
    return {"message": "Student Not Found!"}

            
            
    