import subprocess, argparse, json, pathlib

PROJECT = pathlib.Path(__file__).resolve().parents[0]

with open('CONFIG.json') as f:
    CONFIG = json.load(f)


cmd = lambda x: subprocess.run(x, check=True, shell=True)



def setup_origin( path=f"""{ CONFIG['organization'] }/{ PROJECT.name }""" ):
    try:
        cmd(f'git remote add origin git@github.com:{ path }.git')
    except Exception as e:
        pass

def setup_update( path=f"""{ CONFIG['organization'] }/{ PROJECT.name }""" ):
        cmd(f'git remote set-url origin git@github.com:{ path }.git')

def update( message=None ):
    if not message: message = "update the repository"
    try:
        cmd("git add .")
        cmd(f"""git commit -m '{ message }'""")
        cmd("git push -u origin master")
    except Exception as e:
        pass

def pull_updates():
    try:
        cmd("git pull origin master")
    except Exception as e:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--get', action='store_true' , help='Get Updates from Master/Repo')
    parser.add_argument('-u', '--update', nargs="?"         , help='Update Git & Github')
    parser.add_argument('-s', '--setup', action='store_true', help='Setup Github path org/repo')
    parser.add_argument('-su', '--setup_update', action='store_true', help='Setup-Update Github path org/repo')
    args = parser.parse_args()

    if args.setup           : setup_origin()
    elif args.setup_update  : setup_update()
    elif args.update        : update( args.update[0] )
    elif args.get           : pull_updates()
    else                    : update()

if __name__ == '__main__':
    main()
