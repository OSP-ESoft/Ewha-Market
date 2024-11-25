from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from database import DBhandler
import sys
import hashlib
application = Flask(__name__)
application.config["SECRET_KEY"] = "ABCD"
DB = DBhandler()

@application.route("/")
def hello():
    # return render_template("index.html")
    return redirect(url_for('view_list'))

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
    try:
        reviews = DB.db.child("review").get().val()  # Firebase에서 데이터 가져오기
        reviews_list = []  # 가져온 데이터를 리스트로 변환
        if reviews:
            for key, value in reviews.items():
                reviews_list.append(value)

        # 리뷰 개수와 데이터를 HTML에 전달
        return render_template("review.html", reviews=reviews_list, count=len(reviews_list))
    except Exception as e:
        print(f"Error: {e}")
        flash("리뷰 데이터를 불러오는 중 오류가 발생했습니다.")
        return render_template("review.html", reviews=[], count=0)

@application.route("/detail_review")
def view_detail_review():
    return render_template("detail_review.html")

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

from datetime import datetime  # 날짜 처리를 위해 추가

@application.route("/reg_reviews_init/<name>/")
def reg_reviews_init(name):
    return render_template("reg_reviews.html", name=name)


@application.route("/reg_reviews", methods=["GET", "POST"])
def reg_reviews():
    if request.method == "POST":
        try:
            # POST 요청 처리 (데이터 저장)
            data = request.form.to_dict()
            image_file = request.files.get("file")

            # 기본 값 설정
            product = data.get("product", "")
            title = data.get("title", "")
            content = data.get("content", "")
            payment = data.get("payment", "")
            rating = data.get("rating", "0")

            # 필수 입력값 체크
            if not product or not title:
                flash("상품명과 제목은 필수 항목입니다.")
                return render_template("reg_reviews.html")

            # 이미지 파일 처리
            if image_file and image_file.filename != "":
                image_path = f"static/images/{image_file.filename}"
                image_file.save(image_path)
            else:
                # 기본 이미지 경로 설정
                image_path = "/static/images/default.jpg"

            # Firebase DB 저장
            review_data = {
                "product": product,
                "title": title,
                "content": content,
                "payment": payment,
                "rating": rating,
                "image": f"/{image_path}",  # 경로에 "/"를 추가하여 Flask static 경로와 일치시킴
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
            DB.db.child("review").push(review_data)

            flash("리뷰가 성공적으로 등록되었습니다!")
            return redirect(url_for("view_review"))
        except Exception as e:
            print(f"Error: {e}")
            flash("리뷰 등록 중 오류가 발생했습니다.")
            return render_template("reg_reviews.html")
    else:
        # GET 요청 처리 (리뷰 등록 페이지 렌더링)
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

@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'],name)
    return jsonify({'my_heart': my_heart})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    return jsonify({'msg': '좋아요 완료!'})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    return jsonify({'msg': '좋아요 해제 완료!'})

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
