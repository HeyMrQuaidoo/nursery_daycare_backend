import re
from uuid import UUID
from typing import Union
from pymysql import IntegrityError as PYIntegrityError
from sqlite3 import IntegrityError as SQLiteIntegrityError
from asyncpg.exceptions import (
    IntegrityConstraintViolationError,
    ForeignKeyViolationError,
    UniqueViolationError as AsyncpgUniqueViolationError,
)

from app.core.response import DAOResponse


class CustomException(Exception):
    status_code: int = 400
    msg: str

    def __init__(self, msg=""):
        # msg = self._parse_error_message(error_message=str(msg))
        super().__init__(msg)

    def _parse_error_message(self, error_message):
        # initialize a dictionary to store the parsed data
        error_details = {}

        # regex patterns to extract specific parts of the error message
        unique_constraint_pattern = r'unique constraint "(?P<constraint_name>.*?)"'
        duplicate_key_pattern = (
            r"Key \((?P<column_name>.*?)\)=\((?P<value>.*?)\) already exists"
        )
        table_pattern = r"INSERT INTO (?P<table_name>\w+)"
        parameters_pattern = r"\[parameters: (?P<parameters>.*?)\]"

        # extract unique constraint name
        constraint_match = re.search(unique_constraint_pattern, error_message)
        if constraint_match:
            error_details["constraint_name"] = constraint_match.group("constraint_name")

        # extract the duplicate key column and value
        duplicate_key_match = re.search(duplicate_key_pattern, error_message)
        if duplicate_key_match:
            error_details["column_name"] = duplicate_key_match.group("column_name")
            error_details["value"] = duplicate_key_match.group("value")

        # extract the table name
        table_match = re.search(table_pattern, error_message)
        if table_match:
            error_details["table_name"] = table_match.group("table_name")

        # extract the parameters passed
        parameters_match = re.search(parameters_pattern, error_message)
        if parameters_match:
            error_details["parameters"] = parameters_match.group("parameters")

        human_readable_message = (
            f"Error: A error occurred when trying to insert data into the '{error_details.get('table_name')}' table."
            f"The value '{error_details.get('value')}' in the column '{error_details.get('column_name')}' "
            f"violates the constraint '{error_details.get('constraint_name')}'."
        )

        return human_readable_message

    def to_dao_response(self) -> DAOResponse:
        return DAOResponse(success=False, error=self.msg)


class DatabaseConnectionException(CustomException):
    status_code = 500  # Internal Server Error

    def __init__(self, pymysql_msg):
        self.msg = "Failed Connecting to database, please check credentials and/or connectivity"
        self.msg += "\n" + str(pymysql_msg)
        super().__init__(self.msg)


class DatabaseCredentialException(CustomException):
    status_code = 400  # Bad Request

    def __init__(self, key_, msg=""):
        self.msg = msg if msg else f"{key_} is required"
        super().__init__(self.msg)


class RecordNotFoundException(CustomException):
    status_code = 404  # Not Found

    def __init__(self, model: str = "", id: Union[int | str | UUID] = None, msg=None):
        self.msg = msg if msg else f"{model} with ID {id} not found"
        super().__init__(self.msg)


class UniqueViolationError(CustomException, AsyncpgUniqueViolationError):
    def __init__(self, original_exception: Exception):
        self.original_exception = original_exception
        self.message = self._parse_error_message(error_message=self.original_exception)
        super().__init__(self.message)

    def _parse_exception(self) -> str:
        exception_str = str(self.original_exception)
        if "duplicate key value violates unique constraint" in exception_str:
            return f"Integrity Error: Duplicate entry detected. {self._extract_detail(exception_str)}"
        return f"Error creating data: {exception_str}"

    def _extract_detail(self, exception_str: str) -> str:
        detail_marker = "DETAIL:  "
        detail_start = exception_str.find(detail_marker)
        if detail_start != -1:
            detail_end = exception_str.find("\n", detail_start)
            return exception_str[detail_start:detail_end].strip()
        return "No further details available."

    def __str__(self):
        return self.message


class IntegrityError(
    PYIntegrityError,
    SQLiteIntegrityError,
    IntegrityConstraintViolationError,
    CustomException,
):
    status_code = 400  # Bad Request

    def __init__(self, msg="Integrity error during SQL operation."):
        self.msg = msg
        super().__init__(self.msg)


class ForeignKeyError(CustomException, ForeignKeyViolationError):
    status_code = 400  # Bad Request

    def __init__(self, msg="Foreign key violation"):
        self.msg = msg
        super().__init__(self.msg)
