#!/usr/bin/env python3
"""Filtered logger"""
import logging
import mysql.connector
from os import environ
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')

def filter_datum(fileds: List[str], redaction: str,
        message: str, separator: str) -> str:
    """Filter datum"""
    for field in fields:
        message = re.sub(
                f"{field}=.*?{separator}", 
                f"{field}={redaction}{separator}",
                message
                )
    return message

def get_logger() -> logging.Logger:
    """Get logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get DB"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    return mysql.connector.MySQLConnection(
            user=username, password=password, host=host, database=db_name
            )


def main():
    """Main"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [k[0] for k in cursor.description]

    logger = get_logger()
    for one in cursor:
        one_row = "".join(f"{f}={str(r)} " for r, f in zip(one, field_names))
        logger.info(one_row.strip())

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """Redacting Formater"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == "__main__":
    main()
