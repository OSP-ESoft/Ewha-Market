from flask import Flask, render_template, request, flash
import sys
application = Flask(__name__)
application.config["SECRET_KEY"] = "ABCD"

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/loginpage")
def loginpage():
    return render_template("loginpage.html")

@application.route("/mypage")
def mypage():
    return render_template("mypage.html")

@application.route("/login")
def login():
    flash("로그인")
    return render_template("index.html")

@application.route("/logout")
def logout():
    flash("로그아웃")
    return render_template("index.html")

@application.route("/registerpage")
def registerpage():
    return render_template("registerpage.html")

@application.route("/register")
def register():
    flash("회원가입")
    return render_template("index.html")

@application.route("/list")
def view_list():
    return render_template("list.html")

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")




@application.route("/submit_item", methods=['POST'])
def reg_item_submit():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))

    data = request.form
    '''
    name = request.args.get("name")
    seller = request.args.get("seller")
    addr = request.args.get("addr")
    email = request.args.get("email")
    category = request.args.get("category")
    card = request.args.get("card")
    status = request.args.get("status")
    phone = request.args.get("phone")
    '''

    print(data)
    return render_template("result.html", data=data,  img_path="static/images/{}".format(image_file.filename))

'''
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data=request.form


    return render_template("submit_item_result.html", data=data,  img_path="static/images/{}".format(image_file.filename))
'''

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)