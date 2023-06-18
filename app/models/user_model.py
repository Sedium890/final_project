from app.config.mysqlconnection import connectToMySQL
from app import app
from flask import flash, session
from werkzeug.utils import secure_filename
import os
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


class User:
    DB = 'contractnetwork'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.company_name = data['company_name']
        self.phone_number = data['phone_number']
        self.profile_picture = data['profile_picture']
        self.is_contractor = data['is_contractor']
        self.is_subcontractor = data['is_subcontractor']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.all_sightings = []


    @classmethod
    def register(cls, data, file):
        if not cls.validate_user(data):
            return False

        is_contractor = int('is_contractor' in data)  # 1 if checked, 0 if unchecked
        is_subcontractor = int('is_subcontractor' in data)  # 1 if checked, 0 if unchecked
        hashed_password = bcrypt.generate_password_hash(data['password'])

        query = """
        INSERT INTO users (first_name, last_name, email, password, company_name, phone_number, profile_picture, is_contractor, is_subcontractor)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(company_name)s, %(phone_number)s, %(profile_picture)s, %(is_contractor)s, %(is_subcontractor)s)
        ;"""

        if file and User.allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data['profile_picture'] = filename

        user_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': hashed_password,
            'company_name': data['company_name'],
            'phone_number': data['phone_number'],
            'profile_picture': data['profile_picture'],
            'is_contractor': is_contractor,
            'is_subcontractor': is_subcontractor
        }

        user_id = connectToMySQL(cls.DB).query_db(query, user_data)
        session['first_name'] = data['first_name']
        session['user_id'] = user_id
        return user_id

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in User.ALLOWED_EXTENSIONS


    @classmethod
    def get_user_by_email(cls, email):
        data = {'email': email}
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            result = cls(result[0])
            return result


    @classmethod
    def get_user_by_id(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            result = cls(result[0])
            return result


    @classmethod
    def get_all_users(cls):
        query = """
        SELECT *
        FROM users;
        """
        results = connectToMySQL(cls.DB).query_db(query)

        if results:
            user_listing = []
            for record in results:
                one_user = cls(record)
                user_listing.append(one_user)
            return user_listing
        else:
            return None


    @classmethod
    def login_user(cls, data):
        this_user = cls.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['first_name'] = this_user.first_name
                session['user_id'] = this_user.id
        return this_user
    
    @classmethod
    def update_profile(cls, data, file):
        if file and User.allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data['profile_picture'] = filename

        query = """
        UPDATE users
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s,
            company_name = %(company_name)s, phone_number = %(phone_number)s, profile_picture = %(profile_picture)s
        WHERE id = %(id)s;
        """

        connectToMySQL(cls.DB).query_db(query, data)







    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASS_REGEX = re.compile(r"^(?=.*[A-Z])(?=.*\d).{8,}$")
        is_valid = True

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address")
            is_valid = False
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters.')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters.')
            is_valid = False
        if len(data['email']) < 2:
            flash('EMAIL must be at least 2 characters.')
            is_valid = False
        if len(data['company_name']) < 5:
            flash('Company Name must be at least 5 characters.')
            is_valid = False
        if len(data['phone_number']) < 12:
            flash("phone number is invalid")
            is_valid = False
        if 'password' in data and not PASS_REGEX.match(data['password']):
            flash("Password must be at least 8 characters long, and must contain an uppercase letter and one number.")
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash('That email is already in use')
            is_valid = False
        if 'password' in data and data['password'] != data['confirm_password']:
            flash('Your passwords do not match')
            is_valid = False

        return is_valid




