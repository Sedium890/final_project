from app.config.mysqlconnection import connectToMySQL
from app.models import user_model
from flask import flash, session




class Sighting:
    DB = 'contractnetwork'
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.bid_amount = data['bid_amount'] 
        self.additional_notes = data['additional_notes']
        self.submission_date = data['submission_date']
        self.bid_status = data['bid_status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.created_by = None
        self.bids_proposals_list = []




# ---------------------------------CREATE----------------------------------




    @classmethod
    def save_sighting(cls, data):
        if not cls.validate_sighting(data):
            return False
        else:
            query="""
                INSERT INTO bids_proposals
                (bid_amount, bid_status, submission_date, additional_notes, user_id)
                VALUES
                (%(bid_amount)s, %(bid_status)s, %(submission_date)s, %(additional_notes)s, %(user_id)s);
            """
        return connectToMySQL(cls.DB).query_db(query,data)
    

















# ----------------------------------READ--------------------------------------









    @classmethod
    def get_one_sighting_with_user(cls,data):
        query = """
            SELECT bids_proposals.*, users.company_name
            FROM bids_proposals
            JOIN users
            ON bids_proposals.user_id = users.id
            WHERE bids_proposals.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        print(results)
        return results[0]
    
    @classmethod
    def get_all_sightings(cls):
        query = """
            SELECT *
            FROM bids_proposals
            JOIN users
            WHERE bids_proposals.user_id = users.id;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        print(results)
        all_bids_proposals = []
        for row in results:

            bids_proposals_data={
                'id': row['id'],
                'user_id': row['user_id'],
                'bid_amount': row['bid_amount'],
                'additional_notes': row['additional_notes'],
                'submission_date': row['submission_date'],
                'bid_status': row['bid_status'],
                'created_at': row['created_at'], 
                'updated_at': row['updated_at']
            }
            one_bid_proposal = cls(bids_proposals_data)
            
            user_data={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'company_name': row['company_name'],
                'phone_number': row['phone_number'],
                'profile_picture': row['profile_picture'],
                'is_contractor': row['is_contractor'],
                'is_subcontractor': row['is_subcontractor'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_bid_proposal.created_by = user_model.User(user_data)
            all_bids_proposals.append(one_bid_proposal)
        return all_bids_proposals










# -----------------------------------------UPDATE-------------------------------------






    @classmethod
    def update_sighting(cls,data):
        if not cls.validate_sighting(data):
            return False
        query = """
        UPDATE bids_proposals
        SET 
        bid_amount=%(bid_amount)s, additional_notes=%(additional_notes)s, submission_date=%(submission_date)s, bid_status=%(bid_status)s
        WHERE bids_proposals.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        print(results)
        return results
    













# ------------------------------------------DELETE----------------------------------------------


    @classmethod
    def delete_sighting(cls, data):
        query = """
        DELETE FROM bids_proposals
        WHERE id=%(id)s AND user_id=%(user_id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results







# -------------------------------------STATIC METHODS------------------------------------







    @staticmethod
    def validate_sighting(data):
        is_valid = True
        if len(data['bid_status']) < 2:
            flash('Bid Status must be at least 2 characters.')
            is_valid = False
        if len(data['additional_notes']) < 2:
            flash('Please submit notes')
            is_valid = False
        if len(data['submission_date']) < 2:
            flash('Please enter a date.')
            is_valid = False
        if len(data['bid_amount']) < 1:
            flash('please enter an amount')
            is_valid = False
        return is_valid