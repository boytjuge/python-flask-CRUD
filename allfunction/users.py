from flask import Flask , request, jsonify

tempdata = [{'uid':1,'email':'main@mail.com','pass':'1234'}]


class Users:
    def getAllUser():
        return jsonify({'data':tempdata})

    def getUserById(id):
        if tempdata[id]['uid'] == id:
            return tempdata[id]

    def delUserById(id):
        return tempdata[{}]

    def updateUserById(id):
        return tempdata[{}]

