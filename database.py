import pyrebase
import json 

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def insert_item(self, name, data, user_id, img_path):
        item_info ={
            "seller": user_id,
            "price" : data["price"],
            "addr": data['addr'],
            "phone": data['phone'],
            "card": data['card'],
            "payment" : data["payment"],
            "condition": data['condition'],
            "description" : data["description"],
            "img_path": img_path
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True
    
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
    
    # item 노드 아래 값들 가져오기
    def get_items(self):
        items = self.db.child("item").get().val()
        return items
    
    #상품 이름으로 item 테이블에서 정보 가져오기
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("##########", name)
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value

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