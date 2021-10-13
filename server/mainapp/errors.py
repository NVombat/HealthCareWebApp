from core.errorfactory import UserErrors


class InvalidUserCredentialsError(UserErrors):
    ...


class UserAlreadyExistsError(UserErrors):
    ...


class UserDoesNotExistError(UserErrors):
    ...
