import pyrebase
import json 

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def insert_item(self, name, data, img_path):
        item_info ={
            "seller": "me",
            "category": data.get('category', "unknown"), #카테고리 부분.. 13주차에 수정 예정
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