from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank.")
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank.")

    def post(self):
        data=UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":"this username is already taken"}
        
        user=UserModel(**data)
        user.save_to_db()

        return {"message":"user created succesfully"},201

class User(Resource):
    @classmethod
    def get(cls,user_id):
        user=UserModel.find_by_id(user_id)
        if not user:
            return {"message":"User not found"},404
        return user.json()  

    @classmethod
    def delete(cls,user_id):
        user=UserModel.find_by_id(user_id)
        if not user:
                return {"message":"User not found"},404
        user.delete_from_db()
        return {"message":"user deleted"} ,200        