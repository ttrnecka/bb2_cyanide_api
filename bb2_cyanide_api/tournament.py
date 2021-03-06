"""Match helpers"""
from .match import Match
from collections import Counter

class Tournament:
    def __init__(self, *args:Match):
      self.matches = args

    def leaderboard(self):
      coaches = {}
      for match in self.matches:
        if match.is_concede():
          continue
        for coach in [match.coach1(), match.coach2()]:
          if not coach['coachname'] in coaches:
            coaches[coach['coachname']] = Counter({'name': coach['coachname']})
        winner = match.winner()
        coach1_name = match.coach1()['coachname']
        coach2_name = match.coach2()['coachname']
        coaches[coach1_name]['matches'] += 1
        coaches[coach2_name]['matches'] += 1
        for stat in ["inflictedtouchdowns", "inflictedtackles", "inflictedcasualties",
                     'inflictedinjuries', 'inflictedko', 'inflicteddead', 'inflictedmetersrunning',
                     'inflictedpasses', 'inflictedcatches', 'inflictedinterceptions',
                     'sustainedexpulsions', 'sustainedcasualties', 'sustainedko',
                     'sustainedinjuries', 'sustaineddead', 'inflictedmeterspassing']:
          coaches[coach1_name][stat] += match.team1()[stat]
          coaches[coach2_name][stat] += match.team2()[stat]

        coaches[coach1_name]['opponentinflictedinjuries'] += match.team2()['inflictedinjuries']
        coaches[coach2_name]['opponentinflictedinjuries'] += match.team1()['inflictedinjuries']

        coaches[coach1_name]['opponentinflictedko'] += match.team2()['inflictedko']
        coaches[coach2_name]['opponentinflictedko'] += match.team1()['inflictedko']

        coaches[coach1_name]['opponentinflictedcasualties'] += match.team2()['inflictedcasualties']
        coaches[coach2_name]['opponentinflictedcasualties'] += match.team1()['inflictedcasualties']

        coaches[coach1_name]['opponentinflicteddead'] += match.team2()['inflicteddead']
        coaches[coach2_name]['opponentinflicteddead'] += match.team1()['inflicteddead']

        coaches[coach1_name]['sustainedtouchdowns'] += match.team2()['inflictedtouchdowns']
        coaches[coach2_name]['sustainedtouchdowns'] += match.team1()['inflictedtouchdowns']

        coaches[coach1_name]['inflictedpushouts'] += sum(
            [player['stats']['inflictedpushouts'] for player in match.team1()['roster']]
        )
        coaches[coach2_name]['inflictedpushouts'] += sum(
            [player['stats']['inflictedpushouts'] for player in match.team2()['roster']]
        )
        coaches[coach1_name]['sustainedtackles'] += sum(
            [player['stats']['sustainedtackles'] for player in match.team1()['roster']]
        )
        coaches[coach2_name]['sustainedtackles'] += sum(
            [player['stats']['sustainedtackles'] for player in match.team2()['roster']]
        )

        if winner:
          if winner == match.coach1():
            coaches[coach1_name]['wins'] += 1
            coaches[coach1_name]['points'] += 3
            coaches[coach2_name]['losses'] += 1
          else:
            coaches[coach2_name]['wins'] += 1
            coaches[coach2_name]['points'] += 3
            coaches[coach1_name]['losses'] += 1
        else:
          coaches[coach1_name]['draws'] += 1
          coaches[coach1_name]['points'] += 1
          coaches[coach2_name]['draws'] += 1
          coaches[coach2_name]['points'] += 1

      return [v for k, v in sorted(coaches.items(), key=lambda item: item[1]['points'], reverse=True)]
