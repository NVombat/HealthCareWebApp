from core.errorfactory import AppointmentErrors, UserErrors


class InvalidUserCredentialsError(UserErrors):
    ...


class UserAlreadyExistsError(UserErrors):
    ...


class UserDoesNotExistError(UserErrors):
    ...


class AppointmentAlreadyExistsError(AppointmentErrors):
    ...


class AppointmentDoesNotExistError(AppointmentErrors):
    ...


class DoctorUnavailableError(AppointmentErrors):
    ...
