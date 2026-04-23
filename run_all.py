import subprocess
import os

# paths (adjust if needed)
backend_path = r"C:\Users\Srujan vamshi\OneDrive\Documents\certificates\pro\kubera ai\backend\app"
frontend_path = r"C:\Users\Srujan vamshi\OneDrive\Documents\certificates\pro\kubera ai\frontend\kubera-ui"

print("Starting Backend...")
backend = subprocess.Popen(
    ["uvicorn", "app:app", "--reload"],
    cwd=backend_path,
    shell=True
)

print("Starting Frontend...")
frontend = subprocess.Popen(
    ["npm", "run", "dev"],
    cwd=frontend_path,
    shell=True
)

try:
    backend.wait()
    frontend.wait()
except KeyboardInterrupt:
    print("\nStopping servers...")
    backend.terminate()
    frontend.terminate()