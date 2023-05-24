def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "image": item["image"],
        "email": item["email"],
        "password": item["password"],
        "status": item["status"],
        "role": item["role"],
        "code":item["code"],
        "code_created_at":item["code_created_at"],
        "accessed_at": item["accessed_at"],
        "created_at": item["created_at"],
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]
