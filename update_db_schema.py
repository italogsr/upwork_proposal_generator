import psycopg2
from database_config import DB_CONFIG

def update_schema():
    """Update the database schema to match the application's expectations."""
    commands = [
        # Drop existing tables (in reverse order of dependencies)
        """
        DROP TABLE IF EXISTS proposals;
        """,
        """
        DROP TABLE IF EXISTS job_descriptions;
        """,
        """
        DROP TABLE IF EXISTS profiles;
        """,
        """
        DROP TABLE IF EXISTS users;
        """,
        
        # Create tables with correct schema
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS profiles (
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            post_title VARCHAR(255) NOT NULL,
            post_description TEXT NOT NULL,
            post_skills_founded TEXT[],
            skills_asked_expliced TEXT[],
            level_asked VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS proposals (
            id SERIAL PRIMARY KEY,
            profile_id INTEGER REFERENCES profiles(id),
            job_description_id INTEGER REFERENCES job_descriptions(id),
            headline TEXT,
            body TEXT,
            full_text TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE
        )
        """
    ]
    
    conn = None
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute each command
        for command in commands:
            cur.execute(command)
            
        # Commit the changes
        conn.commit()
        
        # Close the cursor
        cur.close()
        
        print("Database schema updated successfully!")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating schema: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    update_schema()
