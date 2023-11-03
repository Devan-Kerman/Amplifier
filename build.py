import os
import subprocess
import sys

def run_command(command):
	process = subprocess.Popen(command, shell=True)
	process.wait()
	return process.returncode


# Create a virtual environment
if len(sys.argv) < 2:
	wsl_path = f"/root/.virtualenvs/{os.path.basename(os.getcwd())}"
	if os.path.exists(wsl_path):
		print("Linux environment detected!")
		venv_path = wsl_path
	else:
		venv_path = "venv"
else:
	venv_path = sys.argv[1]

if not os.path.exists(venv_path):
	print("Creating virtual environment...")
	return_code = run_command(f"{sys.executable} -m venv {venv_path}")
	if return_code != 0:
		print("Failed to create virtual environment.")
		sys.exit(1)
	else:
		print("Virtual environment created successfully.")
print("Virtual environment already exists.")

# Activate the virtual environment
print("Activating virtual environment...")
activate_script = "activate.bat" if sys.platform == "win32" else "activate"
activate_path = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", activate_script)
activate_command = f"{activate_path}"

if sys.platform != "win32":
	activate_command = f". {activate_command}"

# Install requirements
print("Installing requirements...")
print("Upgrading pip...")
install_command = f"{activate_command} && python -m pip install --upgrade pip"
return_code = run_command(install_command)
if return_code != 0:
	print("Failed to install requirements.")
	sys.exit(1)

print("Installing wheel...")
install_command = f"{activate_command} pip install wheel"
return_code = run_command(install_command)
if return_code != 0:
	print("Failed to install requirements.")
	sys.exit(1)

print("Installing Pytorch...")
install_command = f"{activate_command} && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121"
return_code = run_command(install_command)
if return_code != 0:
	print("Failed to install requirements.")
	sys.exit(1)

print("Installing Additional Libraries...")
with open("req.txt", "w") as f:
	# f.write("clu\n")
	f.write("matplotlib\n")
	# f.write("flax\n")
	f.write("apache_beam\n")
	# f.write("joblib\n")
	f.write("tokenizers\n")
	f.write("openai\n")
	f.write("rich\n")
	f.write('python-dotenv\n')
	f.write("transformers\n")
	f.write("mwparserfromhell\n")

install_command = f"{activate_command} && pip install -r req.txt"
return_code = run_command(install_command)
os.remove("req.txt")
if return_code != 0:
	print("Failed to install requirements.")
	sys.exit(1)

print("Requirements installed successfully.")
print("Project setup complete.")

print("Installing Datasets...")
install_command = f"{activate_command} && pip install datasets"
return_code = run_command(install_command)
if return_code != 0:
	print("Failed to install requirements.")
	sys.exit(1)