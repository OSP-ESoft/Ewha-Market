from flask import Flask, render_template, request, flash, session
from database import DBhandler
import sys
import hashlib
application = Flask(__name__)
application.config["SECRET_KEY"] = "ABCD"
DB = DBhandler()

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/loginpage")
def loginpage():
    return render_template("loginpage.html")

@application.route("/mypage")
def mypage():
    return render_template("mypage.html")

@application.route("/login", methods=['POST'])
def login():
    flash("로그인")
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return render_template("index.html")
    else:
        flash("잘못된 값입니다.")
        return render_template("login.html")
    

@application.route("/logout")
def logout():
    flash("로그아웃")
    session.clear()
    return render_template("index.html")

@application.route("/registerpage")
def registerpage():
    return render_template("registerpage.html")

@application.route("/register", methods=['POST'])
def register():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if DB.insert_user(data,pw_hash):
        flash("회원가입 완료!")
        return render_template("loginpage.html")
    else:
        flash("중복되는 아이디입니다.")
        return render_template("registerpage.html")

@application.route("/list")
def view_list():
    page = request.args.get("page", 1, type=int)

    per_page = 10
    per_row = 5
    row_count = int(per_page/per_row)

    #보여줄 페이지의 첫/마지막 상품 인덱스
    start_idx = per_page*(page-1)
    end_idx = per_page*(page)

    data = DB.get_items() #read table

    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])

    total_count = len(data)
    rows = []  # 상품을 row 단위로 나누어 저장할 리스트

    for i in range(row_count):
        if (i == row_count - 1) and (total_count % per_row != 0):  # 마지막 줄
            rows.append(dict(list(data.items())[i * per_row:])) 
        else:
            rows.append(dict(list(data.items())[i * per_row:(i + 1) * per_row]))
    
    return render_template(
        "list.html",
        # datas = data.items(),
        rows = rows,
        limit = per_page,
        page = page,
        page_count = int((item_counts/per_page)+1),
        total = item_counts)

#상세페이지 라우팅
@application.route('/dynamicurl/<varible_name>/')
def DynamicUrl(varible_name):
    return str(varible_name)

@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("detail.html", name=name, data=data)

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/detail_review")
def view_detail_review():
    return render_template("detail_review.html")

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
    DB.insert_item(data['name'], data, image_file.filename)
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
    return render_template("result.html", data=data, img_path="static/images/{}".format(image_file.filename))

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