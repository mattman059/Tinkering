import subprocess

def run(command):
    output = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    return output.stdout.read().decode() + output.stderr.read().decode()
