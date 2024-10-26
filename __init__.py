import sys
import os

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (project root)
project_root = os.path.dirname(current_dir)

# Add the project root to the Python module search path
sys.path.append(project_root)
