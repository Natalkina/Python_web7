from sqlalchemy import func, desc, select, and_

from src.models import Group, Student, Teacher, Subject, Rating
from src.db import session

"""
Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
select r.student_id, s.fullname, sum(r.value)
from students as s
join rating as r
on s.id = r.student_id
group by r.student_id, s."name"
order by sum(r.value) desc
limit 5
"""


def select_1():

    result = session.query(Student.fullname, func.round(func.avg(Rating.grade), 2).label('avg_grade')) \
        .select_from(Rating).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result


"""
 --Знайти студента із найвищим середнім балом з певного предмета
select r.student_id, s.fullname, round(avg(r.grade), 2) as avg_rating
from students as s
join rating as r  on s.id = r.student_id
join subject as su  on su.id = r.subject_id
where r.subject_id = 2 
group by s.id
order by avg_rating desc
limit 1
"""

def select_2():
    subquery = select(func.max(Rating.grade)).filter(Rating.subject_id == 2).scalar_subquery()

    result = session.query(Rating.student_id, Student.fullname, Rating.grade, Rating.subject_id). \
        join(Student). \
        filter(Rating.subject_id == 1). \
        filter(Rating.grade == subquery). \
        order_by(Rating.student_id).all

    return result


"""
-- Знайти середній бал у групах з певного предмета

select g."name", round(avg(r.grade),2) as avg_rating, r.subject_id 
from students as s
join rating as r  on s.id = r.student_id
join "groups" as g on g.id = s.group_id
where r.subject_id = 2
group by g.id, r.subject_id 
order by g.id, r.subject_id 
"""

def select_3():
    result = session.query(
        Group.name,
        Subject.id,
        func.round(func.avg(Rating.grade), 2).label('avg_rating')) \
        .select_from(Rating).join(Student).join(Group).join(Subject) \
        .filter(Rating.subject_id == 1) \
        .group_by(Group.id, Subject.id).order_by(Group.id, Subject.id).all()
    return result
"""
-- Знайти середній бал на потоці (по всій таблиці оцінок).
select avg(r.value)
from rating r
"""

def select_4():
    result = session.query(
        func.round(func.avg(Rating.grade), 2).label('avg_rating')) \
        .select_from(Rating).all()
    return result

"""
--Знайти які курси читає певний викладач.
select s.fullname , t.fullname
from subjects s
inner join teachers t on s.teacher_id =t.id
where t.id = 3
"""
def select_5():

    result = session.query(
        Subject.name,
        Teacher.fullname) \
        .select_from(Subject).join(Teacher) \
        .filter(Teacher.id == 3).all()
    return result

"""
-- Знайти список студентів у певній групі.
select s.fullname as student_name, g."name"
from students s
inner join "groups" g  on g.id = s.group_id
where g.id = 2
"""

def select_6():
    result = session.query(
        Group.name,
        Student.fullname.label('student_name')) \
        .select_from(Student).join(Group) \
        .filter(Group.id == 2).all()
    return result

"""
-- Знайти оцінки студентів у окремій групі з певного предмета
select g."name",  s.fullname, s2."name", r.grade
from students s
inner join "groups" g  on g.id = s.group_id
inner join rating r on r.student_id = s.id
inner join subjects s2 on s2.id = r.subject_id
where g.id = 2 and r.subject_id = 1
order by r.grade desc
"""

def select_7():
    result = session.query(
        Group.name.label('group'),
        Subject.name.label('subject'),
        Student.fullname.label('student'),
        Rating.grade) \
        .select_from(Rating).join(Student).join(Subject).join(Group) \
        .filter(and_(Group.id == 2, Subject.id == 1)) \
        .order_by(desc(Rating.grade)).all()
    return result

"""
-- Знайти середній бал, який ставить певний викладач зі своїх предметів.
select t.fullname as teacher, round(avg(r.grade),2) as avg_rating, s.name as subject
from  teachers t
inner join subjects s on s.teacher_id = t.id
inner join rating r on r.subject_id  = s.id
where t.id = 1
group by t.fullname, s.name
order by avg_rating  desc
"""

def select_8():
    result = session.query(
        Teacher.fullname.label('teacher'),
        Subject.name.label('subject'),
        func.round(func.avg(Rating.grade), 2).label('avg_rating')) \
        .select_from(Teacher).join(Subject).join(Rating) \
        .filter(Teacher.id == 1) \
        .group_by(Teacher.fullname, Subject.name)\
        .order_by(desc('avg_rating')).all()
    return result

"""
--Знайти список курсів, які відвідує певний студент.
select distinct  s.fullname, s2.name
from  students s
inner join rating r on r.student_id  = s.id
inner join subjects s2 on s2.id = r.subject_id
where s.id = 4
order by s.fullname
"""

def select_9():
    result = session.query(
        Student.fullname.label('student'),
        Subject.name.label('Subject')) \
        .select_from(Rating).join(Subject).join(Student) \
        .filter(Student.id == 1)\
        .order_by(Student.id).all()
    return result
"""
- Список курсів, які певному студенту читає певний викладач
select distinct  s.fullname, s2."name", t.fullname
from  students s
inner join rating r on r.student_id  = s.id
inner join subjects s2 on s2.id = r.subject_id
inner join teachers t on t.id = s2.teacher_id
where t.id = 1 and s.id  = 2
order by s.fullname
"""

def select_10():

    result = session.query(
        Student.fullname.label('student'),
        Subject.name.label('subject'),
        Teacher.fullname.label('teacher')) \
        .select_from(Rating).join(Student).join(Subject).join(Teacher) \
        .filter(and_(Student.id == 2, Teacher.id == 1)) \
        .order_by(Student.id).all()
    return result

"""
-- Середній бал, який певний викладач ставить певному студентові.
select  s.fullname, t.fullname, round(avg(r.grade),2)
from  students s
inner join rating r on r.student_id  = s.id
inner join subjects s2 on s2.id = r.subject_id
inner join teachers t on t.id = s2.teacher_id
where t.id = 1 and s.id  = 2
group by  t.fullname, s.fullname
"""
def select_11():
    result = session.query(
        Student.fullname.label('student'),
        Teacher.fullname.label('teacher'),
        func.round(func.avg(Rating.grade), 2).label('avg_rating')) \
        .select_from(Rating).join(Student).join(Subject).join(Teacher) \
        .filter(and_(Teacher.id == 1, Student.id == 2)) \
        .group_by(Student.fullname, Subject.name).all()
    return result


"""
-- Оцінки студентів у певній групі з певного предмета на останньому занятті.
select s.group_id,  s.fullname ,  s2."name", r.grade, r.date_of
from  students s
inner join rating r on r.student_id  = s.id
inner join subjects s2 on s2.id = r.subject_id
where s.group_id = 1 and r.subject_id = 1 and
r.date_of = (select max(r2.date_of) from rating r2 where s.group_id = 1 and r2.subject_id = 1)
"""

def select_12():
    subquery = select(func.max(Rating.date_of)).join(Student).filter(and_(
        Rating.subject_id == 1, Student.group_id == 1
    )).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Rating.grade, Rating.date_of) \
        .select_from(Rating) \
        .join(Student) \
        .filter(and_(Rating.subject_id == 1, Student.group_id == 1, Rating.date_of == subquery)).all()
    return result


if __name__ == '__main__':
    print(select_1())

