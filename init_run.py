import subprocess
import os

subprocess.run(["python", "init_db.py"])

os.execvp("flask", ["flask", "run", "--host", "0.0.0.0"])
