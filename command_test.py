import os
import subprocess
import sys
import asyncio

# os
os.chdir('D:/user/Desktop/server')

global console
console = subprocess.Popen('java -jar server.jar nogui', shell=True, stdout=subprocess.PIPE)
print('opening server')

while True:
    total_output = ''
    output = console.stdout.readline()
    if output:
        total_output += output.decode()[10:
        print(total_output)