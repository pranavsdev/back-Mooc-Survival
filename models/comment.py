from datetime import datetime
from db import db
from models.user import StudentModel, InstructorModel
from models.course import CourseModel


class CommentModel(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship(
        'CourseModel',
        backref=db.backref('comments', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship(
        'StudentModel',
        backref=db.backref('comments', cascade='all, delete-orphan',
                           lazy='dynamic')
    )
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    instructor = db.relationship(
        'InstructorModel',
        backref=db.backref('comments', cascade='all, delete-orphan',
                           lazy='dynamic')
    )

    def __init__(self, title, content, course_id,
                 student_id=None, instructor_id=None):
        self.title = title
        self.content = content
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.course = CourseModel.find_by_id(course_id)
        if StudentModel.find_by_id(student_id):
            self.student = StudentModel.find_by_id(student_id)
        if InstructorModel.find_by_id(instructor_id):
            self.instructor = InstructorModel.find_by_id(instructor_id)

    def json(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.date.strftime("%d/%m/%y - %H:%M:%S"),
            "course": {
                "id": self.course.id,
                "title": self.course.title
            },
            "author": {
                "id": self.author.id,
                "username": self.author.username
            }
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        if kwargs['content']:
            self.content = kwargs['content']
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, comment_id):
        return cls.query.filter_by(id=comment_id).first()
