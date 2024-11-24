from flask import Flask, render_template, request, flash, session, redirect
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
        return render_template("loginpage.html")
    

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
    print(data)

    total_count = len(data)
    rows = []  # 상품을 row 단위로 나누어 저장할 리스트

    for i in range(row_count):
        if (i == row_count - 1) and (total_count % per_row != 0):  # 마지막 줄
            rows.append(dict(list(data.items())[i * per_row:])) 
        else:
            rows.append(dict(list(data.items())[i * per_row:(i + 1) * per_row]))

    print(rows, type(rows))
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
def view_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("detail.html", name=name, data=data)

@application.route("/group")
def view_group():
    page = request.args.get("page", 1, type=int)

    per_page = 10

    #보여줄 페이지의 첫/마지막 상품 인덱스
    start_idx = per_page*(page-1)
    end_idx = per_page*(page)

    data = DB.get_groups() #read table
    d = []
    
    if data:
        group_counts = len(data)
        data = dict(list(data.items())[start_idx:end_idx])
        print(data, type(data))
        total_count = len(data)
        for i in range(1):
            d.append(dict(list(data.items())[i:]))

    
        return render_template(
            "group.html",
            datas = d,
            limit = per_page,
            page = page,
            page_count = int((group_counts/per_page)+1),
            total = group_counts)
    else:
        return render_template(
            "group.html",
            # datas = data.items(),
            rows = 0,
            limit = 0,
            page = page,
            page_count = 1,
            total = 0)
    
@application.route("/view_group_detail/<title>/")
def view_group_detail(title):
    print("###title:",title)
    data = DB.get_group_bytitle(str(title))
    print("####data:",data)
    return render_template("detail_group.html", title=title, data=data)

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/detail_review")
def view_detail_review():
    return render_template("detail_review.html")

@application.route("/reg_items")
def reg_item():
    id_ = session.get('id', None)
    if not id_:
        flash("로그인하십시오.")
        return redirect("/loginpage")
    else:
        return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_review():
    id_ = session.get('id', None)
    if not id_:
        flash("로그인하십시오.")
        return redirect("/loginpage")
    else:
        return render_template("reg_reviews.html")

@application.route("/reg_groups")
def reg_group():
    id_ = session.get('id', None)
    if not id_:
        flash("로그인하십시오.")
        return redirect("/loginpage")
    else:
        return render_template("reg_groups.html")

@application.route("/submit_item", methods=['POST'])
def reg_item_submit():
    id_ = session.get('id', None)
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))

    data = request.form
    DB.insert_item(data['name'], data, id_, image_file.filename) #name = request.args.get("name")
    name = data['name']
    
    return view_detail(name)

@application.route("/submit_group", methods=['POST'])
def reg_group_submit():
    id_ = session.get('id', None)
    data = request.form
    DB.insert_group(data['title'], data, id_)

    title = data['title']

    return view_group_detail(title)

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