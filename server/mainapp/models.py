from dotenv import load_dotenv
import binascii
import hashlib
import pymongo
import os

from core.settings import DATABASE
from .errors import (
    AppointmentAlreadyExistsError,
    AppointmentDoesNotExistError,
    DoctorUnavailableError,
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
        self.db = client[DATABASE['db']][os.getenv("USER_DATA_COLLECTION")]

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

    def get_name(self, email) -> str:
        """Fetches Name from db for specific user

        Args:
            email: Email ID of User

        Returns:
            str
        """
        if value := self.db.find_one({"Email": email}):
            name = value["Name"]
            return name

        else:
            raise UserDoesNotExistError("User Does Not Exist")


class AppointmentData:
    def __init__(self) -> None:
        """
        Connect to MongoDB
        """
        client = pymongo.MongoClient(DATABASE['mongo_uri'])
        self.db = client[DATABASE['db']][os.getenv(
            "APPOINTMENT_DATA_COLLECTION")]

    def insert_appointment(self, name: str, desc: str, date: str, doc: str):
        """Insert appointment into collection

        Args:
            name: User Name
            desc: Problem descriptio
            date: Date of Appointment
            doc: Doctor

        Returns:
                void: inserts appointment data into db
        """
        if self.db.find_one({"Name": name, "Date": date}):
            raise AppointmentAlreadyExistsError(
                f"An appointment for {name} already exists on {date}")

        elif self.db.find_one({"Date": date, "Doctor": doc}):
            raise DoctorUnavailableError(
                f"Doctor {doc} is unavailable on {date}")

        else:
            rec = {"Name": name, "Description": desc,
                   "Date": date, "Doctor": doc}
            self.db.insert_one(rec)

    def delete_appointment(self, name: str, date: str, doc: str):
        if self.db.find_one({"Name": name, "Date": date, "Doctor": doc}):
            self.db.delete_one(
                {
                    "Name": name,
                    "Date": date,
                    "Doctor": doc,
                },
            )
        else:
            raise AppointmentDoesNotExistError(
                "Appointment Does Not Exist For The Current User or Doctor"
            )
