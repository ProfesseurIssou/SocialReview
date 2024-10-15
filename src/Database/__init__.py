"""
    Différent types de données utilisés dans le projet
"""
from sqlite3worker import Sqlite3Worker
from dataclasses import dataclass
from datetime import datetime, date
from typing import Union

import os

@dataclass
class Base_Platform:
    id: int
    name: str
    base_url: str
@dataclass
class Base_Report_Tag:
    id: int
    tag_name: str
@dataclass
class Base_Account:
    id: int
    platform_id: int
    account_id: str
    account_url: str
@dataclass
class Base_Report:
    id: int
    account_id: int
    report_date: date
    report_tag_id: int
    report_text: str




class Database:
    database_file: str
    db: Sqlite3Worker

    def __init__(self) -> None:
        """
            - Open the database, create the tables if not exists
        """
        self.database_file = "database.db"

        if not os.path.exists(self.database_file):
            self.__Generate_Database()
        self.db = Sqlite3Worker(self.database_file)
        return
            

    def __Generate_Database(self) -> None:
        """
            - Generate the database
            - If the database already exists, remove it
        """
        if os.path.exists(self.database_file):
            os.remove(self.database_file)

        db: Sqlite3Worker = Sqlite3Worker(self.database_file)

        # Create the tables
        db.execute("CREATE TABLE IF NOT EXISTS platform (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, base_url TEXT NOT NULL);")
        db.execute("CREATE TABLE IF NOT EXISTS report_tag (id INTEGER PRIMARY KEY AUTOINCREMENT, tag_name TEXT NOT NULL UNIQUE);")
        db.execute("CREATE TABLE IF NOT EXISTS report_account (id INTEGER PRIMARY KEY AUTOINCREMENT, platform_id INTEGER REFERENCES platform (id) ON DELETE CASCADE, account_id TEXT NOT NULL, account_url TEXT NOT NULL);")
        db.execute("CREATE TABLE IF NOT EXISTS report (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER REFERENCES account (id) ON DELETE CASCADE, report_date TEXT NOT NULL, report_tag_id INTEGER REFERENCES tag (id) ON DELETE CASCADE, report_text TEXT NOT NULL);")

        # Insert the default platforms
        db.execute("INSERT INTO platform (name, base_url) VALUES ('twitter', 'https://twitter.com/');")
        db.execute("INSERT INTO platform (name, base_url) VALUES ('facebook', 'https://facebook.com/');")
        db.execute("INSERT INTO platform (name, base_url) VALUES ('discord', 'https://discord.com/');")
        db.execute("INSERT INTO platform (name, base_url) VALUES ('instagram', 'https://instagram.com/');")

        # Insert the default report tags
        db.execute("INSERT INTO report_tag (tag_name) VALUES ('Autre');")
        db.execute("INSERT INTO report_tag (tag_name) VALUES ('Harcèlement');")
        db.execute("INSERT INTO report_tag (tag_name) VALUES ('Discrimination');")
        db.execute("INSERT INTO report_tag (tag_name) VALUES ('Arnaque');")

        db.close()
        return

    ### PLATFORM ###
    def Platform_GetAll(self) -> list[Base_Platform]:
        """
            Get all the platforms
            Return:
                list[Base_Platform]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, name, base_url FROM platform;")
        return [Base_Platform(id=result[0], name=result[1], base_url=result[2]) for result in results]
    def Platform_GetBy_ID(self, id: int) -> Union[Base_Platform, None]:
        """
            Get the platform by id
            Params:
                id: int
            Return:
                Base_Platform or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, name, base_url FROM platform WHERE id = ?;", [id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Platform(id=result[0], name=result[1], base_url=result[2])
    def Platform_GetBy_Name(self, name: str) -> Union[Base_Platform, None]:
        """
            Get the platform by name
            Params:
                name: str
            Return:
                Base_Platform or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, name, base_url FROM platform WHERE name = ?;", [name])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Platform(id=result[0], name=result[1], base_url=result[2])
    ################

    ### REPORT_TAG ###
    def ReportTag_GetAll(self) -> list[Base_Report_Tag]:
        """
            Get all the report tags
            Return:
                list[Base_Report_Tag]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, tag_name FROM report_tag;")
        return [Base_Report_Tag(id=result[0], tag_name=result[1]) for result in results]
    def ReportTag_GetBy_ID(self, id: int) -> Union[Base_Report_Tag, None]:
        """
            Get the report tag by id
            Params:
                id: int
            Return:
                Base_Report_Tag or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, tag_name FROM report_tag WHERE id = ?;", [id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Report_Tag(id=result[0], tag_name=result[1])
    def ReportTag_GetBy_Name(self, tag_name: str) -> Union[Base_Report_Tag, None]:
        """
            Get the report tag by name
            Params:
                tag_name: str
            Return:
                Base_Report_Tag or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, tag_name FROM report_tag WHERE tag_name = ?;", [tag_name])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Report_Tag(id=result[0], tag_name=result[1])
    
    def ReportTag_Insert(self, tag_name: str) -> None:
        """
            Insert the report tag
            Params:
                tag_name: str
        """
        self.db.execute("INSERT INTO report_tag (tag_name) VALUES (?);", [tag_name])
        return
    ####################

    ### REPORT_ACCOUNT ###
    def Account_GetAll(self) -> list[Base_Account]:
        """
            Get all the report accounts
            Return:
                list[Base_Report_Account]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, platform_id, account_id, account_url FROM report_account;")
        return [Base_Account(id=result[0], platform_id=result[1], account_id=result[2], account_url=result[3]) for result in results]
    def Account_GetBy_ID(self, id: int) -> Union[Base_Account, None]:
        """
            Get the report account by id
            Params:
                id: int
            Return:
                Base_Report_Account or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, platform_id, account_id, account_url FROM report_account WHERE id = ?;", [id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Account(id=result[0], platform_id=result[1], account_id=result[2], account_url=result[3])
    def Account_GetBy_AccountID(self, account_id: str) -> Union[Base_Account, None]:
        """
            Get the report account by account id
            Params:
                account_id: str
            Return:
                Base_Report_Account or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, platform_id, account_id, account_url FROM report_account WHERE account_id = ?;", [account_id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Account(id=result[0], platform_id=result[1], account_id=result[2], account_url=result[3])
    
    def Account_Insert(self, platform_id: int, account_id: str, account_url: str) -> None:
        """
            Insert the report account
            Params:
                platform_id: int
                account_id: str
                account_url: str
        """
        self.db.execute("INSERT INTO report_account (platform_id, account_id, account_url) VALUES (?, ?, ?);", [platform_id, account_id, account_url])
        return
    #####################

    ### REPORT ###
    def Report_GetAll(self) -> list[Base_Report]:
        """
            Get all the reports
            Return:
                list[Base_Report]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, account_id, report_date, report_tag_id, report_text FROM report;")
        return [Base_Report(id=result[0], account_id=result[1], report_date=datetime.strptime(result[2], "%Y-%m-%d").date(), report_tag_id=result[3], report_text=result[4]) for result in results]
    def Report_GetBy_ID(self, id: int) -> Union[Base_Report, None]:
        """
            Get the report by id
            Params:
                id: int
            Return:
                Base_Report or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, account_id, report_date, report_tag_id, report_text FROM report WHERE id = ?;", [id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Report(id=result[0], account_id=result[1], report_date=datetime.strptime(result[2], "%Y-%m-%d").date(), report_tag_id=result[3], report_text=result[4])
    def Report_GetBy_AccountID(self, account_id: int) -> list[Base_Report]:
        """
            Get the report by account id
            Params:
                account_id: int
            Return:
                list[Base_Report]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, account_id, report_date, report_tag_id, report_text FROM report WHERE account_id = ?;", [account_id])
        return [Base_Report(id=result[0], account_id=result[1], report_date=datetime.strptime(result[2], "%Y-%m-%d").date(), report_tag_id=result[3], report_text=result[4]) for result in results]
    def Report_GetBy_TagID(self, tag_id: int) -> list[Base_Report]:
        """
            Get the report by tag id
            Params:
                tag_id: int
            Return:
                list[Base_Report]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, account_id, report_date, report_tag_id, report_text FROM report WHERE report_tag_id = ?;", [tag_id])
        return [Base_Report(id=result[0], account_id=result[1], report_date=datetime.strptime(result[2], "%Y-%m-%d").date(), report_tag_id=result[3], report_text=result[4]) for result in results]
    
    def Report_Insert(self, account_id: int, report_date: date, report_tag_id: int, report_text: str) -> None:
        """
            Insert the report
            Params:
                account_id: int
                report_date: date
                report_tag_id: int
                report_text: str
        """
        self.db.execute("INSERT INTO report (account_id, report_date, report_tag_id, report_text) VALUES (?, ?, ?, ?);", [account_id, report_date.strftime("%Y-%m-%d"), report_tag_id, report_text])
        return
    #################
