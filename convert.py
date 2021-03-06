import os
import sys
import subprocess
import time
import shutil


def is_dimension(x):
    return x.endswith("_nether") or x.endswith("_the_end")


jarnames = sorted(filter(lambda x: '.jar' in x, os.listdir('jars')))
print("By running Spigot jars with this script, you accept the Minecraft EULA!")
print("Backup your worlds!  Once done, place them in the worlds directory and run this script.")
if input(f"Worlds will be upgraded in the order: {jarnames}  Continue? [Y|n]").lower() == 'n':
    print("Cancelling.  The files are sorted on file name, and only allow .jars from the jars directory.")
    sys.exit()
worldnames = sorted(filter(lambda x: os.path.isdir(os.path.join("worlds", x)) and not is_dimension(x),
                           os.listdir('worlds')))
if input(f"Worlds to be upgraded: {worldnames}  Continue? [Y|n]").lower() == 'n':
    print("Cancelling.  Worlds are any directory in the worlds directory.  _nether _the_end need a matching world"
          "(but wont' be in this list).")
    sys.exit()

start = time.time()
keep_going = True
for worldname in worldnames:
    for jarname in jarnames:
        shutil.copyfile(f"jars/{jarname}", f"worlds/{jarname}")
        with open("worlds/server.properties", "a") as fp:
            fp.write(f"level-name={worldname}")
        try:
            print(f"Upgrading {worldname} with {jarname}")
            keep_going = False
            process = subprocess.Popen(['java', '-Xmx1G', '-Xms1G', '-Dcom.mojang.eula.agree=true', '-jar', jarname,
                                        'nogui', '--forceUpgrade'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       cwd='worlds')

            line = 'Garbage'
            while process.poll() is None and line:
                line = process.stdout.readline().decode(sys.stdout.encoding)
                print(line, end="")
                if 'You need to agree to the EULA' in line:
                    print("Read the above message.  You'll find eula.txt in the worlds directory.")
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
print("Removing extra files for next run...")
for path in os.listdir('worlds'):
    rel_path = os.path.join("worlds", path)
    if os.path.isdir(rel_path):
        if path not in worldnames and not is_dimension(path):
            shutil.rmtree(rel_path)
    else:
        os.remove(rel_path)
