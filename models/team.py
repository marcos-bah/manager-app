import sqlite3

from models.collaborator import Collaborator


class Team:
    def __init__(self, team_id=None, name="", project_id=None, collaborators=None):
        self.team_id = team_id
        self.name = name
        self.project_id = project_id
        self.collaborators = collaborators if collaborators else []
        self.tablename = "teams"

    def save(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.team_id:
            cursor.execute("UPDATE teams SET name = ?, project_id = ? WHERE team_id = ?", 
                           (self.name, self.project_id, self.team_id))
        else:
            cursor.execute("INSERT INTO teams (name, project_id) VALUES (?, ?)", 
                           (self.name, self.project_id))
            self.team_id = cursor.lastrowid

        # Save or update collaborators
        for collaborator in self.collaborators:
            cursor.execute("INSERT OR IGNORE INTO team_collaborators (team_id, collaborator_id) VALUES (?, ?)", 
                           (self.team_id, collaborator.collaborator_id))
        
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teams WHERE team_id = ?", 
                       (self.team_id,))
        cursor.execute("DELETE FROM team_collaborators WHERE team_id = ?", 
                       (self.team_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teams")
        rows = cursor.fetchall()
        print(rows)
        teams = []
        for row in rows:
            team = Team(*row)
            team.collaborators = Team.get_collaborators_for_team(team.team_id)
            teams.append(team)
        conn.close()
        return teams

    @staticmethod
    def get_by_id(team_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teams WHERE team_id = ?", 
                       (team_id,))
        row = cursor.fetchone()
        if row:
            team = Team(*row)
            team.collaborators = Team.get_collaborators_for_team(team.team_id)
            conn.close()
            return team
        conn.close()
        return None

    @staticmethod
    def get_collaborators_for_team(team_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT c.* FROM collaborators c JOIN team_collaborators tc ON c.collaborator_id = tc.collaborator_id WHERE tc.team_id = ?", 
                       (team_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Collaborator(*row) for row in rows]
