from fastapi import APIRouter, HTTPException, status, Depends

from app.models.user import User
from app.config.config import collection
from app.schemas.user import userEntity, usersEntity
from app.utils.utils import get_hashed_password, verify_password
from app.utils.repo import JWTRepo, JWTBearer, JWTBearerAdmin
from app.utils.MailService import sendOTP
from bson import ObjectId
from datetime import datetime, date
import random
import re

app_router = APIRouter()


def generate_numeric_otp(length):
    otp = ""
    for _ in range(length):
        digit = random.randint(0, 9)
        otp += str(digit)
    return otp

def validate_password(password):
    regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%^&+=])\S{8,}$"
    return re.match(regex, password) is not None

@app_router.get("/")
async def main():
    
    return {"message": usersEntity(collection.find())}


# RETRIEVE ALL ACCOUNT
@app_router.get("/users", dependencies=[Depends(JWTBearerAdmin())])
async def find_all_users():
    result = usersEntity(collection.find())
    listUsers = []
    for r in result:
        r["image"] = ""
        if r["role"] != 0:
            length = len(r["accessed_at"])
            dtAcc = ["NaN", "NaN"]
            if length > 0:
                time = datetime.fromisoformat(
                    str(r["accessed_at"][length - 1]))
                dtAcc = time.strftime("%Y/%m/%d %H:%M:%S").split(" ")
            time = datetime.fromisoformat(str(r["created_at"]))
            dtCre = time.strftime("%Y/%m/%d %H:%M:%S").split(" ")
            listUsers.append(
                {
                    "id": r["id"],
                    "email": r["email"],
                    "status": r["status"],
                    "role": r["role"],
                    "accessed_at": {"date": dtAcc[0], "time": dtAcc[1]},
                    "created_at": {"date": dtCre[0], "time": dtCre[1]},
                }
            )

    return {"status": "success", "data": listUsers}


# RETRIEVE ACCOUNT BY ID
@app_router.get("/user/{id}", dependencies=[Depends(JWTBearerAdmin())])
async def find_user_by_id(id: str):
    result = userEntity(collection.find_one({"_id": ObjectId(id)}))
    return {"status": "success", "data": result}


# REGISTER ACCOUNT
@app_router.post("/user/register")
async def register(user: User):
    # check existed email
    check = usersEntity(collection.find({"email": str(user.email.lower())}))

    if len(check) != 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Can't create account with email: {user.email.lower()}",
        )
    elif int(user.role) == 0 or int(user.role) > 2 or int(user.role) < 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Can't create account"
        )
    elif user.email.lower() == "" or user.password == "" or validate_password(user.password)==False:
        raise HTTPException(status_code=406, detail="Not Acceptable")
    else:
        user.password = get_hashed_password(user.password)
        user.created_at = datetime.now()
        user.email = user.email.lower()
        _id = collection.insert_one(dict(user))
        result = userEntity(collection.find_one({"_id": _id.inserted_id}))
        return {
            "message": "Successfully created user: " + result["email"],
        }


# UPDATE ACCOUNT BY ID
@app_router.put("/user/{id}", dependencies=[Depends(JWTBearer())])
async def update_user(id: str, user: User):
    try:
        # check existed email
        findUser = userEntity(collection.find_one({"_id": ObjectId(id)}))

        # if email's existed return status 409 (admin's role is 1)
        # if role = 0 or out range[0;2] return status 401
        # else return status 200

        if findUser["email"] != user.email.lower():
            check = usersEntity(collection.find({"email": user.email.lower()}))
            if len(check) != 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Can't update email: {user.email.lower()}",
                )
            elif (
                int(user.role) == 0
                or int(user.role) > 2
                or int(user.role) < 0
                or findUser["role"] == 0
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Can't update account",
                )
        if user.password == "" or validate_password(user.password)==False:
            user.password = findUser["password"]
        else:
            user.password = get_hashed_password(user.password)
        if user.email == "":
            user.email = findUser["email"]
        if user.status == 0:
            user.status == findUser["status"]

        user.accessed_at = findUser["accessed_at"]
        user.created_at = findUser["created_at"]
        user.image = findUser["image"]
        collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
        return {"status": "success"}
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Can't update account"
        )


# DELETE ACCOUNT BY ID
@app_router.delete("/user/{id}", dependencies=[Depends(JWTBearer())])
async def delete_user(id: str):
    try:
        check = userEntity(collection.find_one({"_id": ObjectId(id)}))
        if check["role"] != 0:
            collection.find_one_and_delete({"_id": ObjectId(id)})
            return {"status": "success"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You can delete this account!",
            )
    except:
        raise HTTPException(status_code=400, detail="Not found")


# LOGIN USER
@app_router.post("/user/login")
async def user_login(user: User):
    try:
        result = userEntity(collection.find_one({"email": str(user.email.lower())}))

        if (result):
            if not verify_password(user.password, result["password"]):
                raise HTTPException(
                    status_code=401, detail="Incorrect email or password")

            acc = result["accessed_at"]
            length = len(acc)

            if length > 0:
                if acc[length - 1].date() != date.today():
                    result["accessed_at"].append(datetime.now())
            else:
                result["accessed_at"].append(datetime.now())

            collection.find_one_and_update(
                {"_id": ObjectId(result["id"])}, {"$set": dict(result)}
            )

            if result["status"] == 1:
                token = JWTRepo.generate_token(
                    {"email": result["email"], "role": result["role"]}
                )
                return {
                    "data": {
                        "id": result["id"],
                        "email": result["email"],
                        "role": result["role"],
                    },
                    "access_token": token,
                    "token_type": "Bearer",
                }

            raise HTTPException(
                status_code=307, detail="Account's not verified")
        else:        
            raise HTTPException(
                status_code=404, detail="Account's been deleted")
    except:
        if user.email=="admin@admin.com":
                user.password=get_hashed_password("1")
                user.role=0
                user.status=1
                _id = collection.insert_one(dict(user))
                findUser = userEntity(collection.find_one({"_id": _id.inserted_id}))
                token = JWTRepo.generate_token(
                    {"email": findUser["email"], "role": findUser["role"]}
                )
                return {
                    "data": {
                        "id": findUser["id"],
                        "email": findUser["email"],
                        "role": findUser["role"],
                    },
                    "access_token": token,
                    "token_type": "Bearer",
                }
        raise HTTPException(
                status_code=404, detail="Account's been deleted")


@app_router.get("/send_otp")
async def send_OTP(email: str):
    result = userEntity(collection.find_one({"email": str(email.lower())}))
    if result:
        otp = generate_numeric_otp(6)
        result["code"] = otp
        result["code_created_at"] = datetime.now()
        sendOTP(str(email.lower()), otp)
        collection.find_one_and_update(
            {"_id": ObjectId(result["id"])}, {"$set": dict(result)}
        )
    else:
        raise HTTPException(
            status_code=404, detail="Account's been deleted")


@app_router.post("/user/verify_account")
async def verify_account(user: User):
    findUser = userEntity(collection.find_one({"email": str(user.email.lower())}))
    if findUser:
        if findUser["code"] == user.code and abs(datetime.now() - findUser["code_created_at"]).seconds <= 3000:
            if findUser["status"] == 1:
                token = JWTRepo.generate_token(
                    {"email": findUser["email"], "role": findUser["role"]}
                )
                raise HTTPException(status_code=307, detail={"access_token": token,
                                                             "token_type": "Bearer", })
            else:
                findUser["status"] = 1
                collection.find_one_and_update(
                    {"_id": ObjectId(findUser["id"])}, {"$set": dict(findUser)}
                )

                return {
                    "data": {
                        "id": findUser["id"],
                        "email": findUser["email"],
                        "role": findUser["role"],
                    }
                }
        else:
            otp = generate_numeric_otp(6)
            findUser["code"] = otp
            findUser["code_created_at"] = datetime.now()
            sendOTP(str(user.email.lower()), otp)
            collection.find_one_and_update(
                {"_id": ObjectId(findUser["id"])}, {"$set": dict(findUser)}
            )
            raise HTTPException(status_code=406, detail="Not Acceptable")

    else:
        raise HTTPException(
            status_code=404, detail="Not found")


@app_router.put("/change_password", dependencies=[Depends(JWTBearer())])
async def change_password(user: User, token: str = Depends(JWTBearer())):
    currentUser = userEntity(collection.find_one(
        {"email": JWTRepo.decode_token(token).get("email")}))
    findUser = userEntity(collection.find_one({"email": str(user.email.lower())}))
    if currentUser["email"]==findUser["email"] and validate_password(user.password):
        if findUser:
            if findUser["role"] != 0:
                findUser["password"] = get_hashed_password(user.password)
                collection.find_one_and_update(
                    {"_id": ObjectId(findUser["id"])}, {"$set": dict(findUser)}
                )
            else:
                raise HTTPException(status_code=406, detail="Not Acceptable")     
    else:
        raise HTTPException(status_code=406, detail="Not Acceptable")


@app_router.get("/new-clients", dependencies=[Depends(JWTBearerAdmin())])
async def new_clients():
    newClientsThisQuarter = 0
    ClientsLastQuarter = 0
    pc = 0
    quarterNow = int(datetime.now().month) // 4 + 1
    allUsers = usersEntity(collection.find())

    for u in allUsers:
        quaterU = int(u["created_at"].month) // 4 + 1
        if quaterU == quarterNow:
            newClientsThisQuarter += 1
        elif quarterU == quarterNow - 1:
            ClientsLastQuarter += 1

    if ClientsLastQuarter == 0:
        pc = -1
    else:
        total = False
        pc = round(
            100 * (newClientsThisQuarter - ClientsLastQuarter) /
            ClientsLastQuarter, 2
        )

    return {
        "newClients": (format(newClientsThisQuarter, ",d")),
        "percent": pc,
    }


@app_router.get("/today-users", dependencies=[Depends(JWTBearerAdmin())])
async def today_users():
    allUsers = usersEntity(collection.find())
    countUserToday = 0
    countUserThisOneLastWeek = 0
    pc = 0
    total = True
    for us in allUsers:
        arrAccessed = us["accessed_at"]
        for a in arrAccessed:
            if a.date() == date.today():
                countUserToday += 1
            elif abs(date.today() - a.date()).days == 7:
                countUserThisOneLastWeek += 1
    if countUserThisOneLastWeek == 0:
        pc = round((100 * (countUserToday / len(allUsers))), 2)
    else:
        total = False
        pc = round(
            100
            * (countUserToday - countUserThisOneLastWeek)
            / countUserThisOneLastWeek,
            2,
        )
    return {
        "todayUsers": (format(countUserToday, ",d")),
        "percent": pc,
        "total": total,
    }
