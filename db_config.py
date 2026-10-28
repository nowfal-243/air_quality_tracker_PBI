"""Shared MySQL settings + connection helper used by the pipeline.

Settings are read from environment variables first, then from the .env file
next to this script. Only MYSQL_PASSWORD is required.

    MYSQL_PASSWORD  (required)
    MYSQL_USER      (default: root)
    MYSQL_HOST      (default: 127.0.0.1)
    MYSQL_PORT      (default: 3306)
    MYSQL_DATABASE  (default: air_quality)
"""
import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _read_env_file():
    values = {}
    path = os.path.join(BASE_DIR, ".env")
    if not os.path.exists(path):
        return values
    # utf-8-sig drops the BOM that Windows Notepad / PowerShell can add
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            values[key.strip()] = val.strip().strip('"').strip("'")
    return values


def get_setting(name, default=None):
    return os.getenv(name) or _read_env_file().get(name) or default


def _url(with_database=True):
    password = get_setting("MYSQL_PASSWORD")
    if not password:
        raise SystemExit(
            "MYSQL_PASSWORD is not set.\n"
            "Fix: create a .env file next to run_pipeline.py containing\n"
            "     MYSQL_PASSWORD=your_password\n"
            "or set the MYSQL_PASSWORD environment variable."
        )
    return URL.create(
        "mysql+pymysql",
        username=get_setting("MYSQL_USER", "root"),
        password=password,
        host=get_setting("MYSQL_HOST", "127.0.0.1"),
        port=int(get_setting("MYSQL_PORT", "3306")),
        database=get_setting("MYSQL_DATABASE", "air_quality") if with_database else None,
    )


def get_engine():
    """Return an engine for the pipeline database, creating the database if needed.

    Exits with a plain-English message if MySQL cannot be reached.
    """
    db = get_setting("MYSQL_DATABASE", "air_quality")
    try:
        server = create_engine(_url(with_database=False))
        with server.begin() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db}`"))
        engine = create_engine(_url())
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except OperationalError as e:
        code = e.orig.args[0] if getattr(e, "orig", None) and e.orig.args else None
        hints = {
            2003: "MySQL is not running or not listening on that host/port. Start the MySQL service.",
            1045: "Wrong MySQL user/password. Check MYSQL_PASSWORD in .env.",
            2059: "MySQL auth plugin problem. Install the 'cryptography' package (pip install cryptography).",
        }
        raise SystemExit(f"Cannot connect to MySQL: {hints.get(code, 'see error below')}\n{e.orig}")
