from app import app

@app.route('/user/signup')
def signup():
    return "this is a sign up page"