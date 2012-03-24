import commlib
import gamestates

def alive(players):
    result = []
    for i in len(players):
        if not (players[i].lost):
            result.append(i)
    return result

def endgame(winner_index, names):
    print "The winner is " + names[winner_index]

def tetris():
    channel = Commlink()
    #get players to join game and assign names to players
    players = channel.poll()
    while len(alive(players)) > 1:
        for user in channel.connectedusers:
            channel.send(user, players)
        players = channel.poll()
    endgame(alive(players)[0])
