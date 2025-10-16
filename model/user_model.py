#from app import app
import mysql.connector
from flask import make_response
import os
import json
from marshmallow import Schema,fields,ValidationError
from dotenv import load_dotenv
load_dotenv()

class UserSchema(Schema):
    id=fields.Int(required=False)
    name=fields.Str(required=True,error_messages={"required": "Name is required"})
    email = fields.Email(required=True, error_messages={"required": "Email is required", "invalid": "Invalid email format"})
    phone = fields.Str(required=True, error_messages={"required": "Phone is required"})
    role = fields.Str(required=True, error_messages={"required": "Role is required"})
    password = fields.Str(required=True, error_messages={"required": "Password is required"})

#@app.route("/user/model/user_model_signUp")
class Model():
    def __init__(self): #within constructor mysql connection code as soon as object got created it will call the constructor
        try:
            #self.connection=mysql.connector.connect(host="localhost",user="root",password="admin",database="flask_tutorial")
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME")
            )
            self.connection.autocommit=True
            self.cur=self.connection.cursor(dictionary=True)
            print("connection succesfull")
        except:
            print('error')
    
    def userSignupModel(self):
        return "This is a user sign up model"


    def user_getAll_model(self):
        self.cur.execute("select * from user")
        result=self.cur.fetchall()
        print(result)
        if len(result)>0:
            #query execution code
            return make_response({'payload':result},200)
            #return json.dumps(result)
        else:
            return make_response({'messege':'no rows found'},204)
    
    def user_addUser_model(self,data):
        try:
            validated_data=UserSchema().load(data)
            query="INSERT INTO user(name, email, phone, role, password) VALUES (%s,%s,%s,%s,%s)"
            values = (
                validated_data['name'],
                validated_data['email'],
                validated_data['phone'],
                validated_data['role'],
                validated_data['password']
            )
            #print('data is',data['name'])
            self.cur.execute(query,values)
            return {"message": "User added successfully"}
        except ValidationError as err:
            return {"errors": err.messages}

    
    def user_updateUser_model(self,data):
        print('data is',data['name'])
        self.cur.execute(
    "UPDATE user SET name=%s, email=%s, phone=%s, role=%s, password=%s WHERE id=%s",
    (data['name'], data['email'], data['phone'], data['role'], data['password'], data['id'])
)
        if self.cur.rowcount>0:

            return make_response({'messege': "user updated successfully"},202)
        
        else:
            return make_response({'message': "Nothing to update"},204)
        
    def user_deleteUser_model(self,id):
        self.cur.execute(f"DELETE from user where id={id}")
        if self.cur.rowcount>0:

            return make_response({'message':"user deleted successfully"},200)
        
        else:
            return make_response({'message': "Nothing to delete"},204)
        

    def user_patchUser_model(self,data,id):
        qry="UPDATE user SET"
        print(data)
        for ele,val in data.items():
            qry+=f" {ele}='{val}',"
        print(qry)
        qry=qry[:-1]+' '+f"where id={id}"
        self.cur.execute(qry)
        if self.cur.rowcount>0:

            return make_response({'messege': "user updated successfully"},202)
        
        else:
            return make_response({'message': "Nothing to update"},204)
        
    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (page - 1) * limit  # correct offset

        qry = f"SELECT * FROM user LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()

        if result:
            return make_response(
                {"message": "Users fetched successfully", "data": result}, 200
            )
        else:
            return make_response({"message": "No users found"}, 204)
        
    def __del__(self):
        """Clean up MySQL resources when Model object is deleted."""
        try:
            if hasattr(self, "connection") and self.connection.is_connected():
                self.cur.close()
                self.connection.close()
                print("MySQL connection closed")
        except Exception as e:
            print(f"Error closing connection: {e}")
        
        
    