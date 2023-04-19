
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(50), nullable=False)
    group_id = Column(Integer, ForeignKey(Group.id, ondelete="CASCADE"))
    groups = relationship('Group', backref='students')

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(50), nullable=False)


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teacher.id, ondelete="CASCADE"))
    teachers = relationship('Teacher', backref='subjects')

class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=True)
    date_of = Column(Date, nullable=True)
    subject_id = Column(Integer, ForeignKey(Subject.id, ondelete="CASCADE"))
    student_id = Column(Integer, ForeignKey(Student.id, ondelete="CASCADE"))
    students = relationship('Student', backref='grade')
    subjects = relationship('Subject', backref='grade')








