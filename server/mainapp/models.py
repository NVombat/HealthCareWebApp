from dotenv import load_dotenv
import hashlib
import binascii
import pymongo
import os

from core.settings import DATABASE
from .errors import (
    InvalidUserCredentialsError,
    UserAlreadyExistsError,
    UserDoesNotExistError,
)

load_dotenv()


class UserData:
    def __init__(self) -> None:
        """
        Connect to MongoDB
        """
        client = pymongo.MongoClient(DATABASE['mongo_uri'])
        self.db = client[DATABASE['db']][os.getenv("DATA_COLLECTION")]

    def insert_user(self, name: str, email: str, password: str) -> None:
        """Insert user into collection

        Args:
            name: User Name
            email: User Email ID
            pwd: User Account Password

        Returns:
                void: inserts user data into db
        """
        if self.db.find_one({"Email": email}):
            raise UserAlreadyExistsError("User Already Exists")
        else:
            pwd = self.hash_password(password)
            rec = {"Name": name, "Email": email, "Password": pwd}
            self.db.insert_one(rec)

    def hash_password(self, pwd: str) -> str:
        """Hashes password using salted password hashing (SHA512 & PBKDF_HMAC2)

        Args:
            pwd: Password to be hashed

        Returns:
            str: Hashed password
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        print("SALT1: ", salt)
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha512", pwd.encode("utf-8"), salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        final_hashed_pwd = (salt + pwd_hash).decode("ascii")
        return final_hashed_pwd

    def check_hash(self, email: str, pwd: str) -> bool:
        """Verifies hashed password with stored hash & verifies user before login

        Args:
            email: Email ID of User
            pwd: Password to be checked

        Returns:
            bool
        """
        if value := self.db.find_one({"Email": email}):
            dbpwd = value["Password"]
            # print("DBPWD: ", dbpwd)

            # PASSWORD HASH AND SALT STORED IN DATABASE
            salt = dbpwd[:64]
            # print("SALT2: ", salt)
            dbpwd = dbpwd[64:]
            # print("Stored password hash: ", dbpwd)

            # PASSWORD HASH FOR PASSWORD THAT USER HAS CURRENTLY ENTERED
            pwd_hash = hashlib.pbkdf2_hmac(
                "sha512", pwd.encode("utf-8"), salt.encode("ascii"), 100000
            )
            pwd_hash = binascii.hexlify(pwd_hash).decode("ascii")
            # print("pwd_hash: ", pwd_hash)

            if pwd_hash == dbpwd:
                # print("Hash Match")
                return True
            else:
                # print("Hash does NOT match")
                # return False
                raise InvalidUserCredentialsError("Invalid Login Credentials")

        else:
            print("User NOT in DB")
            # return False
            raise UserDoesNotExistError("User Does Not Exist")
