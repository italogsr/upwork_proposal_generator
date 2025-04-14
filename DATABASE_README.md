# Database Setup for Upwork Proposal Generator

This document provides detailed information about the database setup for the Upwork Proposal Generator application.

## Database Configuration

The application uses PostgreSQL as its database system. The database configuration is defined in the `database_config.py` file:

```python
# Database connection parameters
DB_CONFIG = {
    'dbname': 'upwork_proposal_generator',
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'host': os.getenv('DATABASE_HOST', 'localhost'),
    'port': os.getenv('DATABASE_PORT', '5432')
}

# Connection string format for SQLAlchemy
DB_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
```

## Database Schema

The application uses the following tables:

### Users Table

Stores user account information for authentication.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Profiles Table

Stores freelancer profiles with skills, experience, and other information.

```sql
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    skills TEXT[],
    experience INTEGER DEFAULT 0,
    price INTEGER DEFAULT 0,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Job Descriptions Table

Stores job descriptions from Upwork with extracted skills and requirements.

```sql
CREATE TABLE job_descriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    post_title VARCHAR(255) NOT NULL,
    post_description TEXT NOT NULL,
    post_skills_founded TEXT[],
    skills_asked_expliced TEXT[],
    level_asked VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Proposals Table

Stores generated proposals linking profiles to job descriptions.

```sql
CREATE TABLE proposals (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER REFERENCES profiles(id),
    job_description_id INTEGER REFERENCES job_descriptions(id),
    headline TEXT,
    body TEXT,
    full_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## Database Setup Options

### Option 1: Local Setup

1. Install PostgreSQL:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib

   # Start PostgreSQL service if not already running
   sudo systemctl start postgresql
   ```

2. Create the database and user:
   ```bash
   # Create the database and user (run as postgres user)
   sudo -u postgres psql -c "CREATE DATABASE upwork_proposal_generator;"
   sudo -u postgres psql -c "CREATE USER your_database_user WITH PASSWORD 'your_database_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE upwork_proposal_generator TO your_database_user;"
   sudo -u postgres psql -c "GRANT ALL ON SCHEMA public TO your_database_user;"
   ```

3. Create the database tables:
   ```bash
   # Run the database schema creation script
   python db_schema.py
   ```

4. Test the database connection:
   ```bash
   # Run the test connection script
   python test_db_connection.py
   ```

### Option 2: Docker Setup

When using Docker, the database is automatically set up as part of the container initialization:

1. The PostgreSQL database runs in its own container (`db`)
2. The database schema is initialized using the `docker/db/init.sql` script
3. The database data is stored in a Docker volume for persistence

## Database Utilities

The project includes several utilities for working with the database:

### `db_schema.py`

Creates the database tables using raw SQL commands with psycopg2.

```bash
python db_schema.py
```

### `create_tables.py`

Creates the database tables using SQLAlchemy ORM models.

```bash
python create_tables.py
```

### `test_db_connection.py`

Tests the connection to the database and displays the PostgreSQL version.

```bash
python test_db_connection.py
```

### `check_db_schema.py`

Displays the current database schema, including tables and columns.

```bash
python check_db_schema.py
```

### `update_db_schema.py`

Updates the database schema by dropping and recreating all tables (warning: this will delete all data).

```bash
python update_db_schema.py
```

## Environment Variables

The database configuration is controlled by the following environment variables:

```
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost  # Use 'db' for Docker setup
DATABASE_PORT=5432
```

These variables should be set in the `.env` file for local setup or will be automatically configured in the Docker environment.

## SQLAlchemy ORM Models

The application uses SQLAlchemy ORM for database operations. The models are defined in `src/db/models.py`:

### User Model

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")
    job_descriptions = relationship("JobDescription", back_populates="user", cascade="all, delete-orphan")
```

### Profile Model

```python
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    skills = Column(ARRAY(String), default=[])
    experience = Column(Integer, default=0)
    price = Column(Integer, default=0)
    description = Column(Text)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profiles")
    proposals = relationship("Proposal", back_populates="profile", cascade="all, delete-orphan")
```

### JobDescription Model

```python
class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_title = Column(String, index=True)
    post_description = Column(Text)
    post_skills_founded = Column(ARRAY(String), default=[])
    skills_asked_expliced = Column(ARRAY(String), default=[])
    level_asked = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    proposals = relationship("Proposal", back_populates="job_description", cascade="all, delete-orphan")
```

### Proposal Model

```python
class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"))
    headline = Column(Text)
    body = Column(Text)
    full_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    profile = relationship("Profile", back_populates="proposals")
    job_description = relationship("JobDescription", back_populates="proposals")
```

## Database Operations

Database operations are handled by the CRUD functions defined in `src/db/crud.py`. These functions provide a clean interface for creating, reading, updating, and deleting records in the database.

## Troubleshooting

### Connection Issues

If you encounter connection issues, check:

1. PostgreSQL service is running
2. Database and user exist with correct permissions
3. Environment variables are set correctly
4. For Docker setup, ensure the database container is running

### Reset Database

To reset the database and start fresh:

```bash
# For local setup
sudo -u postgres psql -c "DROP DATABASE IF EXISTS upwork_proposal_generator;"
sudo -u postgres psql -c "CREATE DATABASE upwork_proposal_generator;"
sudo -u postgres psql -c "CREATE USER your_database_user WITH PASSWORD 'your_database_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE upwork_proposal_generator TO your_database_user;"
sudo -u postgres psql -c "GRANT ALL ON SCHEMA public TO your_database_user;"
python db_schema.py

# For Docker setup
docker-compose down -v  # This will remove the volume with all data
docker-compose up -d    # This will recreate the database
```
