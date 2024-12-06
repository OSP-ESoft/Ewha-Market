import pyrebase
import json 
from datetime import datetime 

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()


    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "pw": pw,
            "email": data['email'],
            "phone": data['phone']
        }

        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        print("users###",users.val())

        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()

                if value['id'] == id_string:
                    return False
            return True
    
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False
    
    #mypage
    def get_user_by_data(self,user_id):
        datas = self.db.child("user").get()
        for res in datas.each():
            user_data = res.val()
            if user_data.get("id") == user_id:
                return user_data
        return None
        
    #review 
    def get_reviews(self, sort_by="recent"):
        reviews = self.db.child("review").get().val()
        if sort_by == "recent":
            sorted_reviews = dict(sorted(reviews.items(), key=lambda x: x[1].get("date", ""), reverse=True))
        elif sort_by == "high":
            # 별점 높은 순 정렬
            sorted_reviews = dict(sorted(reviews.items(), key=lambda x: int(x[1].get("rating", 0)), reverse=True))
        elif sort_by == "low":
            # 별점 낮은 순 정렬
            sorted_reviews = dict(sorted(reviews.items(), key=lambda x: int(x[1].get("rating", 0))))
        else:
            # 기본 정렬: 변경 없음
            sorted_reviews = reviews
        return sorted_reviews
    
    def insert_review(self, title, data, img_path,user_id):
        review_info = {
            "writer": user_id,
            "product": data["product"],
            "title": data["title"],
            "content": data["content"],
            "payment": data["payment"],
            "rating": data["rating"],
            "img_path": img_path,
            "date": datetime.now().strftime("%Y-%m-%d"),  # 현재 날짜를 문자열로 포맷
        }

        self.db.child("review").child(title).set(review_info)
        return True    
    def get_review_bytitle(self, title):
        reviews = self.db.child("review").get()
        for res in reviews.each():
            if res.key() == title:
                return res.val() 
        return None  

    # item
    def get_items(self):
        items = self.db.child("item").get().val()
        # print(f"Retrieved items: {items}") #데이터 확인
        return items
    
    def insert_item(self, title, data, user_id, img_path):
        item_info ={
            "seller": user_id,
            "price" : data["price"],
            "addr": data['addr'],
            "phone": data['phone'],
            "card": data['card'],
            "payment" : data["payment"],
            "condition": data['condition'],
            "description" : data["description"],
            "category" : data['category'],
            "img_path": img_path
        }
        self.db.child("item").child(title).set(item_info)
        print(data,img_path)
        return True
        
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("##########", name)
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value

    def get_items_bycategory(self, cate):
        items = self.db.child("item").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()
            # if value['category'] == cate:
            if 'category' in value and value['category'] == cate: #value가 category를 가지고 있는지 검토
                target_value.append(value)
                target_key.append(key_value)
        # print("######target_value",target_value)
        print(f"Filtered items for category {cate}: {target_value}") #디버깅용
        new_dict={}
        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    
    #buy-popup
    def get_seller_by_item_name(self, item_name):
        item = self.db.child("item").child(item_name).get()

    # item 데이터를 출력하여 어떤 값이 반환되는지 확인
        print(f"### item.val(): {item.val()}")

        if item.val():
            return item.val().get("seller")
        return None


    
    

    
    # def get_sellerInfo_by_id(self, seller_id): 
    #     # Firebase에서 판매자 ID에 해당하는 사용자 정보 가져오기
    #     seller_info = self.db.child("user").child(seller_id).get()

    #     # 판매자 정보가 존재할 경우 email과 phone 반환
    #     if seller_info.val():
    #         seller_data = seller_info.val()
    #         return {
    #             "email": seller_data.get("email"),
    #             "phone": seller_data.get("phone")
    #         }
    #     else:
    #         return None  # 해당 판매자가 없을 경우 None 반환

    def get_sellerInfo_by_id(self, seller_id):
    # Firebase에서 모든 사용자 정보를 가져오기
        all_users = self.db.child("user").get()

    # 모든 사용자 정보에서 id가 seller_id와 일치하는 사용자를 찾음
        for user_key, user_data in all_users.val().items():
            if user_data.get("id") == seller_id:  # id가 seller_id와 일치하는지 확인
                return {
                    "email": user_data.get("email"),
                    "phone": user_data.get("phone")
                }
    
        return None  # 해당 판매자 ID를 가진 사용자가 없을 경우 None 반환

    # group
    def get_groups(self):
        groups = self.db.child("group").get().val()
        return groups
    
    def insert_group(self, title, data, user_id):
        group_info ={
            "writer": user_id,
            "phone": data['phone'],
            "category": data['category'],
            "description" : data["description"],
            "status" : "모집중"
        }
        self.db.child("group").child(title).set(group_info)
        return True

    def get_group_bytitle(self, title):
        items = self.db.child("group").get()
        target_value=""
        print("##########", title)
        for res in items.each():
            key_value = res.key()
            
            if key_value == title:
                target_value = res.val()
        return target_value
        
    def get_groups_bycategory(self, category):
        items = self.db.child("group").get()
        target_value=[]
        target_key=[]

        for res in items.each():
            value = res.val()
            key_value = res.key()
            # if value['category'] == cate:
            if 'category' in value and value['category'] == category: #value가 category를 가지고 있는지 검토
                target_value.append(value)
                target_key.append(key_value)
        # print("######target_value",target_value)

        print(f"Filtered items for category {category}: {target_value}") #디버깅용

        new_dict={}
        for k,v in zip(target_key,target_value):
            new_dict[k]=v

        data = sorted(new_dict.items(), key=lambda x:x[1]["status"], reverse=True)
        return dict(data)
    
    #좋아요
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value

        for res in hearts.each():
            key_value = res.key()

            if key_value == name:
                target_value=res.val()
        return target_value

    def update_heart(self, user_id, isHeart, item):
        heart_info ={
        "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True   
