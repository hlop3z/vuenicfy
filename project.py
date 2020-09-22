import subprocess, argparse, json, pathlib, shutil, os

PATH = os.getcwd()
cmd  = lambda x: subprocess.run(x, check=True, shell=True)

def new_project(name):
    app_name = name.lower().replace('-','_').strip()
    cmd(f'git clone https://github.com/hlop3z/skeletoy')

    EXAMPLE_FILE = f"""
import sys

sys.path.append('../{ app_name }')


import { app_name }

# Modules
print( { app_name }.__plugins__ )

# Class
{ app_name }.__demo__.Plugin().hello()

# Def
{ app_name }.__demo__.hello()
    """.strip()

    try:
        shutil.rmtree("skeletoy/.git")
        shutil.rmtree("skeletoy/tests")
        shutil.rmtree("skeletoy/examples")
        shutil.rmtree("skeletoy/dist")
        shutil.rmtree("skeletoy/skeletoy.egg-info")
        os.remove("skeletoy/project.py")
    except Exception as e:
        pass


    os.mkdir('skeletoy/examples')
    os.mkdir('skeletoy/tests')

    with open("skeletoy/examples/example.py", "w") as f:
        f.write( EXAMPLE_FILE )
        f.close()

    shutil.move("skeletoy/skeletoy", f"skeletoy/{ app_name }")
    shutil.move("skeletoy", app_name)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project', nargs=1, help='''Clone Github "hlop3z/skeletoy" for a new project''')
    args = parser.parse_args()

    if args.project: new_project( args.project[0] )
    else: pass



if __name__ == '__main__':
    main()
