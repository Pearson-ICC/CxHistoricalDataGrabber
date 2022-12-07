import sqlite3
from typing import Optional, Generator
from db.cxRecord import CxRecord


class Database:
    def __init__(self):
        self.db_name = "records.db"
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        self.create_table()
        self.conn.commit()

    def create_table(self):
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS records
            (interactionId TEXT NOT NULL UNIQUE, startTimestamp TEXT NOT NULL, interactionTime INTEGER NOT NULL, queue TEXT NOT NULL, channelType TEXT NOT NULL)"""
        )

    def insertFromGenerator(self, generator: Generator[CxRecord, None, None]):
        i = 1
        for record in generator:
            self.c.execute(
                "INSERT OR REPLACE INTO records VALUES (?, ?, ?, ?, ?)",
                (
                    record.interactionId,
                    record.startTimestamp,
                    record.interactionTime,
                    record.queue,
                    record.channelType,
                ),
            )
            # print(f"#{i} - {record.interactionId}")
            i += 1
            if i % 100000 == 0:
                self.conn.commit()  # commit every 100000 records so we don't lose everything if the script is stopped etc
                print(f"Committed {i} records")
        self.conn.commit()
        print(f"Committed {i} records total.")

    def insert(
        self,
        interactionId: str,
        startTimestamp: str,
        interactionTime: int,
        queue: str,
        channelType: str,
    ):
        self.c.execute(
            "INSERT OR REPLACE INTO records VALUES (?, ?, ?, ?, ?)",
            (interactionId, startTimestamp, interactionTime, queue, channelType),
        )
        self.conn.commit()

    def getAll(self):
        self.c.execute("SELECT * FROM records")
        return self.c.fetchall()

    def getWhere(
        self,
        queueId: Optional[str] = None,
        channelType: Optional[str] = None,
        betweenStart: Optional[str] = None,
        betweenEnd: Optional[str] = None,
    ) -> list[CxRecord]:
        query = "SELECT * FROM records "
        if queueId or channelType or betweenStart or betweenEnd:
            query += "WHERE "
        if queueId:
            query += f"queue='{queueId}'"
        if channelType:
            query += f"channelType='{channelType}'"
        if betweenStart and betweenEnd:
            query += f"startTimestamp BETWEEN '{betweenStart}' AND '{betweenEnd}'"

        self.c.execute(query)
        return self.c.fetchall()

    def close(self):
        self.conn.close()
