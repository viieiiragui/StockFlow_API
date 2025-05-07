"""
Database initialization module.

Sets up the SQLAlchemy database instance for use in Flask applications.
"""

from flask_sqlalchemy import SQLAlchemy

# Instantiate the SQLAlchemy object
db = SQLAlchemy()
