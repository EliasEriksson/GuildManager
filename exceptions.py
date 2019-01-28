class Base(BaseException):
    def __init__(self, message=None):
        self.message = message


class UserAlreadyExcists(Base):
    pass


class ServerAlreadyExcists(Base):
    pass


class MissingUser(Base):
    pass


class MissingServer(Base):
    pass


class MissingUsersServer(Base):
    pass


class RequestNotSuccessfull(Base):
    pass


class DoubleCommand(Base):
    pass


class Timeout(Base):
    pass


class DatabaseStructureError(Base):
    pass


class UsersServersLinkAlreadyExcists(Base):
    pass
