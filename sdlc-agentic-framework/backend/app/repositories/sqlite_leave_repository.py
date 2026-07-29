"""Small SQLite repository proving local persistence without extra dependencies."""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

class SQLiteLeaveRepository:
    def __init__(self, database: Path | str):
        self.database = str(database)
        self._initialise()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialise(self) -> None:
        with self._connect() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS employees(id TEXT PRIMARY KEY, manager_id TEXT NOT NULL, balance INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS leave_requests(id TEXT PRIMARY KEY, employee_id TEXT NOT NULL, manager_id TEXT NOT NULL,
              start_date TEXT NOT NULL, end_date TEXT NOT NULL, days INTEGER NOT NULL, reason TEXT NOT NULL,
              status TEXT NOT NULL, created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS leave_audit(id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT NOT NULL,
              action TEXT NOT NULL, actor_id TEXT NOT NULL, occurred_at TEXT NOT NULL);
            """)
            db.executemany("INSERT OR IGNORE INTO employees VALUES(?,?,?)", [("E001","M001",12),("E002","M001",2),("E003","M002",8),("E004","M002",0)])

    def employee(self, employee_id: str) -> dict[str, Any] | None:
        with self._connect() as db:
            row = db.execute("SELECT * FROM employees WHERE id=?", (employee_id,)).fetchone()
            return dict(row) if row else None

    def overlapping(self, employee_id: str, start: str, end: str) -> bool:
        with self._connect() as db:
            row = db.execute("SELECT 1 FROM leave_requests WHERE employee_id=? AND status IN ('PENDING','APPROVED') AND start_date<=? AND end_date>=?", (employee_id,end,start)).fetchone()
            return row is not None

    def create(self, record: dict[str, Any]) -> dict[str, Any]:
        with self._connect() as db:
            db.execute("INSERT INTO leave_requests VALUES(:id,:employee_id,:manager_id,:start_date,:end_date,:days,:reason,:status,:created_at)", record)
            db.execute("INSERT INTO leave_audit(request_id,action,actor_id,occurred_at) VALUES(?,?,?,?)", (record["id"],"SUBMITTED",record["employee_id"],record["created_at"]))
        return record

    def get(self, request_id: str) -> dict[str, Any] | None:
        with self._connect() as db:
            row=db.execute("SELECT * FROM leave_requests WHERE id=?",(request_id,)).fetchone()
            return dict(row) if row else None

    def decide(self, request_id: str, status: str, manager_id: str) -> dict[str, Any]:
        now=datetime.utcnow().isoformat()
        with self._connect() as db:
            db.execute("UPDATE leave_requests SET status=? WHERE id=?",(status,request_id))
            db.execute("INSERT INTO leave_audit(request_id,action,actor_id,occurred_at) VALUES(?,?,?,?)",(request_id,status,manager_id,now))
            return dict(db.execute("SELECT * FROM leave_requests WHERE id=?",(request_id,)).fetchone())
