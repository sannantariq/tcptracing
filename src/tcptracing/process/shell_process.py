import shlex
import subprocess

def start_process(cmd, stdin=None, stdout=None, shell=False):
    if not shell:
        args = shlex.split(cmd)
    else:
        args = cmd
    p = subprocess.Popen(args=args, stdin=stdin, stdout=stdout, shell=shell)
    return p

if __name__ == "__main__":
    # cmd = "echo 'HelloWorld' | tee -a sample.txt"
    cmd = "/Users/stariq/Documents/Research/lossVdelay/tcptracing/src/bash_scripts/simple.sh"
    p = start_process(cmd, stdout=subprocess.DEVNULL, shell=True)
    output, _ = p.communicate()
    print(output)