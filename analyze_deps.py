import subprocess
import sys

def run_pip_command(command):
    """Run a pip command and return the output."""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def main():
    """Analyze package dependencies."""
    print("Checking for dependency conflicts...")
    
    # Try to install packages with verbose output to see conflicts
    result = run_pip_command([
        sys.executable, "-m", "pip", "install", 
        "--dry-run", "-r", "requirements.txt", 
        "--verbose"
    ])
    
    print(result)
    
    # Check for specific problematic packages
    print("\nChecking numpy compatibility...")
    result = run_pip_command([
        sys.executable, "-m", "pip", "install",
        "--dry-run", "numpy==1.24.3",
        "--verbose"
    ])
    print(result)

if __name__ == "__main__":
    main() 
