from models.team import Team

class TeamController:
    @staticmethod
    def create_team(name):
        team = Team(name=name)
        team.save()

    @staticmethod
    def delete_team(team_id):
        team = Team.get_by_id(team_id)
        if team:
            team.delete()

    @staticmethod
    def get_all_teams():
        return Team.get_all()

    @staticmethod
    def get_team_by_id(team_id):
        return Team.get_by_id(team_id)
