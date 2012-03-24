import commlib
import gamestates

def Gameover():
    return False

def tetris():
    channel = Commlink()
    while !Gameover():
        for user in channel.connectedusers:
            channel.send(user, channel.poll())
