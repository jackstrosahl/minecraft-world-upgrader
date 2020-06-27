import os
import sys
import subprocess
import time

jarnames = sorted(filter(lambda x: '.jar' in x, os.listdir('jars')))
print("By running Spigot jars with this script, you accept the Minecraft EULA!")
print("Backup your worlds!  Once done, place them in the jars directory and run this script.")
if input(f"World will be upgraded in the order: {jarnames}  Continue? [Y|n]").lower() == 'n':
    print("Cancelling.  The files are sorted on file name, and only allow .jars from the jars directory.")
    sys.exit()

start = time.time()
keep_going = True
for jarname in jarnames:

    try:
        print(f"Upgrading with {jarname}")
        keep_going = False
        process = subprocess.Popen(['java', '-Xmx1G', '-Xms1G', '-Dcom.mojang.eula.agree=true', '-jar', jarname,'nogui',
                                    '--forceUpgrade'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd='jars')
        line = 'Garbage'
        while process.poll() is None and line:
            line = process.stdout.readline().decode(sys.stdout.encoding)
            print(line, end="")
            if 'You need to agree to the EULA' in line:
                print("Read the above message.  You'll find eula.txt in the jars directory.")
                break
            if 'Done' in line:
                print('Moving on...')
                process.communicate(input='Stop'.encode(sys.stdin.encoding))
                keep_going = True

        if not keep_going:
            print(f"Failed on {jarname}, see above output.")
            break
    finally:
        process.kill()

print(f"Finished upgrading through {jarnames} in {time.time()-start} seconds.")