import subprocess
host='jetbrains.com'
ping_output = subprocess.check_output(['ping','-c 5', host])

print(ping_output)