import sys
import commlib
import host
import client

try:
    if sys.argv[1] == "-c":
        client.tetris(sys.argv[2])
    elif sys.argv[1] == "-h":
        host.tetris()
    elif sys.argv[1] == "-w":
        print commlib.ipwords
    else:
        print "Usage: python tetris.py -c <room name> OR python tetris.py -h OR python tetris.py -w"
except:
    print "Usage: python tetris.py -c <room name> OR python tetris.py -h OR python tetris.py -w"
