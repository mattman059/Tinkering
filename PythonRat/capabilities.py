import subprocess

def run(command):
    """
    Parameters
    ----------
    command : str
        The command to execute via subprocess pipe


    Returns
    -------
    str
        stdout/stderr result of the executed command
    """

    
    output = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    return output.stdout.read().decode() + output.stderr.read().decode()
