import sqlite3

def setup_database():
    # Connect to the database (this will create the database if it does not exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS task_collaborators")
    cursor.execute("DROP TABLE IF EXISTS team_collaborators")
    cursor.execute("DROP TABLE IF EXISTS tasks")
    cursor.execute("DROP TABLE IF EXISTS teams")
    cursor.execute("DROP TABLE IF EXISTS collaborators")
    cursor.execute("DROP TABLE IF EXISTS projects")

    # Create the projects table
    cursor.execute("""
    CREATE TABLE projects (
        project_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )
    """)

    # Create the tasks table
    cursor.execute("""
    CREATE TABLE tasks (
        task_id INTEGER PRIMARY KEY,
        project_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )
    """)

    # Create the collaborators table
    cursor.execute("""
    CREATE TABLE collaborators (
        collaborator_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Create the teams table
    cursor.execute("""
    CREATE TABLE teams (
        team_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        project_id INTEGER,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )
    """)

    # Create the team_collaborators table
    cursor.execute("""
    CREATE TABLE team_collaborators (
        team_id INTEGER,
        collaborator_id INTEGER,
        PRIMARY KEY (team_id, collaborator_id),
        FOREIGN KEY (team_id) REFERENCES teams(team_id),
        FOREIGN KEY (collaborator_id) REFERENCES collaborators(collaborator_id)
    )
    """)

    # Create the task_collaborators table
    cursor.execute("""
    CREATE TABLE task_collaborators (
        task_id INTEGER,
        collaborator_id INTEGER,
        PRIMARY KEY (task_id, collaborator_id),
        FOREIGN KEY (task_id) REFERENCES tasks(task_id),
        FOREIGN KEY (collaborator_id) REFERENCES collaborators(collaborator_id)
    )
    """)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Execute the setup function
setup_database()
