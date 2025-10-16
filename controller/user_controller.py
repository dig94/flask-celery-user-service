#from app import app
from flask import Blueprint,request,jsonify
from tasks.user_tasks import send_welcome_email
#from model.user_model_check import user_model
from model.user_model import Model

user_bp = Blueprint("user", __name__)
obj=Model()

@user_bp.route("/user/signup")
def user_signup_controller():
    return obj.userSignupModel()

@user_bp.route("/user/getAll")
def user_getAll_controller():
    return obj.user_getAll_model()
    #return obj.user_signup_model()

@user_bp.route("/user/addone",methods=["POST"])
def user_addone_controller():
    data=request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    result = obj.user_addUser_model(data)
    email = data.get("email")
    task_id = None
    if email:
        task = send_welcome_email.delay(email)  # async
        task_id = task.id

    # 3. Return response immediately
    return jsonify({
        "message": "User added successfully",
        "db_result": result,
        "email_task_id": task_id
    }), 201

@user_bp.route("/user/update",methods=["PUT"])
def user_update_controller():
    return obj.user_updateUser_model(request.form)

@user_bp.route("/user/delete/<id>",methods=["DELETE"])
def user_delete_controller(id):
    return obj.user_deleteUser_model(id)

@user_bp.route("/user/patch/<id>",methods=["PATCH"])
def user_patch_controller(id):
    return obj.user_patchUser_model(request.form,id)


@user_bp.route("/user/page/limit/<limit>/page/<page>",methods=["GET"])
def user_pagination_controller(limit,page):
    return obj.user_pagination_model(limit,page)