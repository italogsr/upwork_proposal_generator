#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Check if DATABASE_USER and DATABASE_PASSWORD are set
if [ -z "$DATABASE_USER" ] || [ -z "$DATABASE_PASSWORD" ]; then
  echo "Error: DATABASE_USER and DATABASE_PASSWORD must be set in .env file or environment"
  echo "Example:"
  echo "DATABASE_USER=your_database_user"
  echo "DATABASE_PASSWORD=your_database_password"
  exit 1
fi

# Drop and recreate database
sudo -u postgres psql -c "DROP DATABASE IF EXISTS upwork_proposal_generator;"
sudo -u postgres psql -c "CREATE DATABASE upwork_proposal_generator;"

# Drop and recreate user with new permissions
sudo -u postgres psql -c "DROP USER IF EXISTS $DATABASE_USER;"
sudo -u postgres psql -c "CREATE USER $DATABASE_USER WITH PASSWORD '$DATABASE_PASSWORD';"

# Grant privileges
sudo -u postgres psql -c "ALTER USER $DATABASE_USER WITH SUPERUSER;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE upwork_proposal_generator TO $DATABASE_USER;"
sudo -u postgres psql -d upwork_proposal_generator -c "GRANT ALL ON SCHEMA public TO $DATABASE_USER;"
sudo -u postgres psql -d upwork_proposal_generator -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DATABASE_USER;"

echo "Database setup complete. Database 'upwork_proposal_generator' created with user '$DATABASE_USER'."
echo "You can now run 'python db_schema.py' to create the tables."