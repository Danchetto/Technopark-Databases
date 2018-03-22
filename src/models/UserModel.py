import json

class UserModel:

    def fill_info(self,nickname, about, email, fullname):
        self.nickname = nickname
        self.about = about
        self.email = email
        self.fullname = fullname

    def return_full_info(self):
        response = {'about': self.about,
                    'email': self.email,
                    'fullname': self.fullname,
                    'nickname': self.nickname}
        return json.dumps(response)
