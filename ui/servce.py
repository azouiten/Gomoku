import sys
import random
import subprocess
import time

if __name__ == "__main__":
    if int(sys.argv[1]) == 1:
        p = subprocess.Popen(['python3', 'servce.py', '2'], 
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

        i = 0
        recieve = False
        while True:
            if recieve:
                print('p1 is recieving...', file=sys.stderr)
                
                buf = []
                for line in p.stdout:
                    buf.append(line)
                print('p1 is recieving...', file=sys.stderr)
                recieve = False
            else:
                p.stdin.write(str.encode('Mok nta\n'))
                print('p1 sent.', file=sys.stderr)
                recieve = True
            i += 1
        
    else:
        
        i = 0
        recieve = True
        while True:
            if recieve:
                print('p2 is recieving...', file=sys.stderr)
                buf = []
                for line in sys.stdin:
                    buf.append(line)
                print(f'p2 recieved. {buf}', file=sys.stderr)
                recieve = False
            else:
                print('Mok')
                recieve = True
            i += 1
