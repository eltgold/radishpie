import os
import sys
import subprocess
import ctypes # Required to interact with Windows OS functions (UAC)
import tempfile # For creating and managing temporary directories
import shutil # For file moving operations
import tkinter as tk
from tkinter import ttk, messagebox
import threading

# --- Helper Functions for Administrator Privileges ---

def is_admin():
    """
    Checks if the script is running with administrator privileges on Windows.
    Returns True if it is an administrator, False otherwise.
    """
    try:
        # Tries to call the IsUserAnAdmin() function from shell32.dll
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        # In case of an error (e.g., OS is not Windows),
        # assumes it's not an administrator and prints the error.
        print(f"Error checking administrator privileges: {e}")
        return False

def run_as_admin():
    """
    Attempts to restart the Python script with administrator privileges on Windows.
    Displays the User Account Control (UAC) prompt.
    """
    python_executable = sys.executable # Full path to the Python executable
    script_path = os.path.abspath(sys.argv[0]) # Full path to the current script

    print("Script detected not running as administrator.")
    print("Attempting to restart with administrator privileges. Please confirm in the UAC prompt.")

    try:
        # Uses ShellExecuteW to re-execute the script with the 'runas' verb
        ctypes.windll.shell32.ShellExecuteW(
            None,          # hWnd: Parent window handle (None for default)
            "runas",       # lpOperation: The operation verb (runas = run as administrator)
            python_executable, # lpFile: The file to be executed (python.exe)
            f'"{script_path}"', # lpParameters: Arguments for the executable (script path in quotes)
            None,          # lpDirectory: Working directory (None for current)
            1              # nShowCmd: How the window should be shown (1 = SW_SHOWNORMAL)
        )
        # If execution is successful, the current (non-admin) process can be terminated.
        sys.exit(0)
    except Exception as e:
        print(f"Error attempting to restart as administrator: {e}")
        print("Could not obtain administrator privileges. Please run the script manually as administrator.")
        sys.exit(1) # Exit with error code if elevation fails

# --- Installation and Download Functions ---

def install_package(pkg):
    """
    Installs a Python package using pip.
    Ensures that the pip associated with the current interpreter is used.
    """
    print(f"Installing '{pkg}' package...")
    try:
        # Uses subprocess.check_call to execute pip and check the return code
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        print(f"Package '{pkg}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing package '{pkg}': {e}")
        print("Please check your internet connection or permissions.")
        sys.exit(1) # Exit if an essential package installation fails

def check_and_install_packages():
    """
    Checks for the presence of 'requests' and 'wmi' packages and installs them if necessary.
    """
    print("Checking for necessary Python packages...")
    try:
        import requests
        print("'requests' is already installed.")
    except ImportError:
        install_package("requests")

    try:
        import wmi
        print("'wmi' is already installed.")
    except ImportError:
        # The 'wmi' package is Windows-specific and may have dependencies like 'pywin32'.
        # Pip usually handles this automatically.
        install_package("wmi")
    print("Package check completed.")


def download_dd():
    """
    Downloads the 'dd.exe' file from a URL, extracts it from a ZIP to a temporary directory,
    moves it to the current directory, then hides it.
    Returns True on success, False on failure.
    """
    import requests
    import zipfile

    DD_URL = "http://www.chrysocome.net/downloads/69633bffe459caa3779730c11c9247f8/dd-0.6beta3.zip"
    DD_ZIP_NAME = "dd.zip"
    DD_FILENAME = "dd.exe"
    FINAL_DD_PATH = os.path.join(".", DD_FILENAME) # Final path where dd.exe should be

    print(f"Downloading {DD_FILENAME} (will overwrite if exists)...")
    try:
        # Makes an HTTP request to download the ZIP file in stream mode
        r = requests.get(DD_URL, stream=True)
        r.raise_for_status() # Raises an exception for bad HTTP status codes (4xx or 5xx)

        # Creates a temporary directory that will be automatically cleaned up when exiting the 'with' block
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_zip_path = os.path.join(temp_dir, DD_ZIP_NAME)
            temp_dd_path = os.path.join(temp_dir, DD_FILENAME)

            # Saves the ZIP file to the temporary directory
            with open(temp_zip_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"File {DD_ZIP_NAME} downloaded to temporary directory. Extracting {DD_FILENAME}...")
            # Extracts dd.exe from the ZIP to the temporary directory
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                zip_ref.extract(DD_FILENAME, temp_dir)

            # Tries to remove the existing dd.exe in the final directory before moving
            if os.path.exists(FINAL_DD_PATH):
                try:
                    os.remove(FINAL_DD_PATH)
                    print(f"Removed existing file: {FINAL_DD_PATH}")
                except OSError as e:
                    print(f"Warning: Could not remove existing file {FINAL_DD_PATH}: {e}. Attempting to move anyway.")
                    # If it cannot be removed, the move operation might fail if the file is locked.

            # Moves dd.exe from the temporary directory to the final directory
            print(f"Moving {DD_FILENAME} to the current directory...")
            shutil.move(temp_dd_path, FINAL_DD_PATH)

        # Hides the dd.exe file using the Windows attrib command
        print(f"Hiding {DD_FILENAME}...")
        subprocess.run(['attrib', '+h', FINAL_DD_PATH], creationflags=subprocess.CREATE_NO_WINDOW, check=True)

        print(f"{DD_FILENAME} downloaded, extracted, and hidden successfully.")
        return True
    except Exception as e:
        # Catches any exception that occurs during the download/extraction/move process
        print(f"Failed to download {DD_FILENAME}: {e}")
        # Tries to clean up the temporary ZIP file if it was partially downloaded (if temp_dir didn't clean up)
        if 'temp_zip_path' in locals() and os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)
        return False

def write_radishpie():
    """
    Creates or overwrites the 'radishpie.py' file with the GUI code
    and hides it.
    """
    RADISHPIE_FILENAME = "radishpie.py"
    # The complete RadishPie application code in a multi-line string.
    # Using a unique delimiter (r'''_RADISHPIE_CODE_START_''') to prevent
    # "unterminated triple-quoted string literal" errors if the internal
    # code contains sequences that could be misinterpreted as string endings.
    radishpie_code = r'''_RADISHPIE_CODE_START_
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import wmi
import os
import re
import sys # Imported for sys.executable and sys.argv
import ctypes # Imported for is_admin and run_as_admin

# --- Helper Functions for Administrator Privileges (Copied from setup script) ---

def is_admin():
    """
    Checks if the script is running with administrator privileges on Windows.
    Returns True if it is an administrator, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """
    Attempts to restart the Python script with administrator privileges on Windows.
    Displays the User Account Control (UAC) prompt.
    """
    python_executable = sys.executable
    script_path = os.path.abspath(sys.argv[0])
    print("Radish Pie: Attempting to restart with administrator privileges...")
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            python_executable,
            f'"{script_path}"',
            None,
            1
        )
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("ADMIN ERROR", f"Could not obtain administrator privileges.\nPlease run 'radishpie.py' manually as administrator.\nError: {e}")
        sys.exit(1)

# --- Main RadishPie Application Class ---

class RadishPie(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Radish Pie 1.0")
        self.geometry("600x420")
        self.wmi = wmi.WMI()
        self.last_iso_dir = os.getcwd() # Keeps track of the last accessed ISO directory

        self.create_widgets()
        self.refresh_drives() # Populates the USB drives list on startup

    def create_widgets(self):
        """Creates and organizes the graphical interface widgets."""
        # Label and Combobox for USB drive selection
        ttk.Label(self, text="USB Drives:").pack(anchor="w", padx=10, pady=5)
        self.drive_list = ttk.Combobox(self, state="readonly")
        self.drive_list.pack(fill="x", padx=10)

        # Label and Combobox for partition style selection (MBR/GPT)
        ttk.Label(self, text="Partition Style:").pack(anchor="w", padx=10, pady=5)
        self.part_style = ttk.Combobox(self, values=["MBR", "GPT"], state="readonly")
        self.part_style.current(0) # Sets MBR as default
        self.part_style.pack(fill="x", padx=10)

        # Label and Combobox for file system selection (FAT32/NTFS)
        ttk.Label(self, text="File System:").pack(anchor="w", padx=10, pady=5)
        self.fs = ttk.Combobox(self, state="readonly")
        self.fs.pack(fill="x", padx=10)

        # Label, Entry, and Button for ISO file selection
        ttk.Label(self, text="ISO File:").pack(anchor="w", padx=10, pady=5)
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=10)
        self.iso_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.iso_path).pack(side="left", fill="x", expand=True)
        ttk.Button(frame, text="Browse", command=self.browse_iso).pack(side="left", padx=5)

        # Progress bar to display burning progress
        self.progress = ttk.Progressbar(self, orient="horizontal", length=580, mode="determinate")
        self.progress.pack(pady=15, padx=10)

        # Status label for user messages
        self.status_label = ttk.Label(self, text="Ready", anchor="center")
        self.status_label.pack(fill="x", padx=10)

        # Frame for action buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        self.start_btn = ttk.Button(btn_frame, text="Format & Write ISO", command=self.start_process)
        self.start_btn.pack(side="left", padx=5)
        # NEW BUTTON: Format Drive (for recovery)
        self.format_btn = ttk.Button(btn_frame, text="Format Drive", command=self.start_format_only_process)
        self.format_btn.pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Refresh Drives", command=self.refresh_drives).pack(side="left", padx=5)

    def iso_fat32_compatible(self, iso_path):
        """
        Checks if the ISO file size is compatible with the FAT32 file system (<= 4GB).
        """
        try:
            size = os.path.getsize(iso_path)
            print(f"Radish Pie (DEBUG): ISO size '{iso_path}': {size} bytes") # DEBUG: Displays ISO size
            return size <= 4 * 1024 * 1024 * 1024  # 4GB limit for FAT32
        except Exception as e: # Catches the exception to display the error
            print(f"Radish Pie (ERROR): Error getting ISO size '{iso_path}': {e}") # DEBUG: Displays the error
            return False # Returns False in case of an error getting the size

    def browse_iso(self):
        """
        Opens a dialog box for the user to select an ISO file.
        Updates file system options based on ISO size.
        """
        print("Radish Pie (DEBUG): browse_iso function called.") # DEBUG: Confirms function call
        file = filedialog.askopenfilename(initialdir=self.last_iso_dir, filetypes=[("ISO Files", "*.iso")])
        if file:
            print(f"Radish Pie (DEBUG): ISO selected: {file}") # DEBUG: Displays selected ISO path
            self.iso_path.set(file) # Sets the selected ISO path
            self.last_iso_dir = os.path.dirname(file) # Saves the directory for next time
            compatible = self.iso_fat32_compatible(file)
            print(f"Radish Pie (DEBUG): Compatible with FAT32: {compatible}") # DEBUG: Displays compatibility result
            if compatible:
                self.fs["values"] = ["FAT32", "NTFS"] # Offers FAT32 and NTFS
                self.fs.current(0)  # Sets FAT32 as default
                self.set_status("ISO size OK for FAT32. FAT32 and NTFS available.")
            else:
                self.fs["values"] = ["NTFS"] # Offers only NTFS
                self.fs.current(0)
                self.set_status("ISO too big for FAT32. Only NTFS available.")
            print(f"Radish Pie (DEBUG): FS options set to: {self.fs['values']}") # DEBUG: Shows set options
        else:
            print("Radish Pie (DEBUG): No ISO file selected.") # DEBUG: Informs if no file was selected

    def refresh_drives(self):
        """
        Updates the list of available removable USB drives on the system.
        """
        self.set_status("Refreshing drives...")
        self.update_idletasks() # Forces GUI update to show status message
        drives = []
        self.drives_info = {} # Dictionary to map display string to disk index

        try:
            # Iterates over all physical disks detected by WMI
            for disk in self.wmi.Win32_DiskDrive():
                # Checks if the disk is removable (USB)
                if disk.MediaType and "Removable" in disk.MediaType:
                    disk_index = disk.Index # Gets the disk index (e.g., 0, 1, 2)
                    # Calculates disk size in GB for display
                    size_gb = round(int(disk.Size) / (1024**3))
                    display_string = f"Disk {disk_index} - {disk.Model} ({size_gb} GB)"
                    drives.append(display_string)
                    self.drives_info[display_string] = disk_index # Stores the disk index
            print(f"Radish Pie (DEBUG): Drives found via WMI: {drives}") # DEBUG: Shows found drives
        except Exception as e:
            print(f"Radish Pie (ERROR): Error accessing WMI to list drives: {e}") # DEBUG: WMI error
            self.set_status("ERROR: Could not list drives. Run as administrator.")
            messagebox.showerror("ERROR", "Could not list USB drives. Please run the application as administrator.")


        self.drive_list["values"] = drives # Updates combobox options
        if drives:
            self.drive_list.current(0) # Selects the first drive by default
            self.set_status(f"Found {len(drives)} removable drive(s).")
        else:
            self.set_status("No removable drives detected.")
        self.progress["value"] = 0 # Resets progress bar

    def start_process(self):
        """
        Starts the ISO formatting and burning process.
        Performs validations and asks for user confirmation.
        """
        # Initial validations
        if not self.drive_list.get():
            messagebox.showerror("ERROR", "Please select a USB drive.")
            return
        if not os.path.isfile(self.iso_path.get()):
            messagebox.showerror("ERROR", "Please select a valid ISO file.")
            return

        # Crucial confirmation before erasing drive data
        confirm = messagebox.askyesno(
            "Confirm Action",
            (
                f"CRITICAL WARNING: All data on drive '{self.drive_list.get()}' will be PERMANENTLY ERASED and the drive will be formatted.\n\n"
                "DOUBLE-CHECK that you have selected the CORRECT drive, as this operation is IRREVERSIBLE.\n\n"
                "Are you sure you want to continue?"
            ),
        )
        if not confirm:
            self.set_status("Operation cancelled by user.")
            return

        self.progress["value"] = 0
        self.set_status("Starting process...")
        self.start_btn.config(state="disabled") # Disables button to prevent multiple executions
        self.format_btn.config(state="disabled") # Disables format button as well
        # Starts the process in a new thread to avoid freezing the graphical interface
        threading.Thread(target=self.process_task, daemon=True).start()

    def start_format_only_process(self):
        """
        Starts the process of formatting a selected USB drive (without burning an ISO).
        Useful for recovering drives in RAW state.
        """
        if not self.drive_list.get():
            messagebox.showerror("ERROR", "Please select a USB drive to format.")
            return

        # Crucial confirmation before formatting
        confirm = messagebox.askyesno(
            "Confirm Format",
            (
                f"CRITICAL WARNING: All data on drive '{self.drive_list.get()}' will be PERMANENTLY ERASED and the drive will be formatted.\n\n"
                "DOUBLE-CHECK that you have selected the CORRECT drive, as this operation is IRREVERSIBLE.\n\n"
                "This function is useful for recovering drives in RAW or unreadable state.\n\n"
                "Are you sure you want to format this drive?"
            ),
        )
        if not confirm:
            self.set_status("Formatting cancelled by user.")
            return

        self.progress["value"] = 0
        self.set_status("Starting drive formatting...")
        self.start_btn.config(state="disabled") # Disables ISO burning button
        self.format_btn.config(state="disabled") # Disables the format button itself
        threading.Thread(target=self.format_drive_task, daemon=True).start()

    def format_drive_task(self):
        """
        Contains the logic to format the selected USB drive using diskpart (with clean).
        Executed in a separate thread.
        """
        try:
            drive_str = self.drive_list.get()
            disk_index = self.drives_info[drive_str]
            part_style = self.part_style.get()
            fs = self.fs.get()

            part_style_lower = part_style.lower()
            fs_lower = fs.lower()

            self.set_status(f"Formatting drive {drive_str} to {fs}...")
            # Diskpart script to clean, partition, and format the disk
            # The 'clean' command is used here to ensure recovery of RAW drives
            diskpart_script_content = (
                f"select disk {disk_index}\n"
                "clean\n" # Use clean to ensure RAW drives are formatted
                f"convert {part_style_lower}\n"
                "create partition primary\n"
                f"format fs={fs_lower} quick\n"
                "assign\n"
                "exit\n"
            )
            diskpart_script_path = "diskpart_script.txt"
            with open(diskpart_script_path, "w") as f:
                f.write(diskpart_script_content)

            dp = subprocess.run(["diskpart", "/s", diskpart_script_path], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            os.remove(diskpart_script_path)
            if dp.returncode != 0:
                self.show_error(f"DISKPART FAILED! Check disk and permissions.\nError: {dp.stderr}")
                return

            self.set_status("Drive formatted successfully!")
            messagebox.showinfo("SUCCESS", "USB drive formatted successfully!")

        except Exception as e:
            self.show_error(f"An unexpected error occurred during formatting: {e}")
        finally:
            self.start_btn.config(state="normal")
            self.format_btn.config(state="normal")
            self.progress["value"] = 100 # Completes the progress bar for formatting

    def process_task(self):
        """
        Contains the main ISO formatting and burning logic.
        Executed in a separate thread.
        """
        try:
            drive_str = self.drive_list.get()
            disk_index = self.drives_info[drive_str] # Gets the selected disk index
            part_style = self.part_style.get()
            fs = self.fs.get()
            iso = self.iso_path.get()

            part_style_lower = part_style.lower()
            fs_lower = fs.lower()

            self.set_status("Executing diskpart to prepare the drive (cleaning and formatting)...")
            # Diskpart script to clean, partition, and format the disk
            # The 'clean' command is REINTRODUCED here to ensure a clean base for ISO burning.
            diskpart_script_content = (
                f"select disk {disk_index}\n"
                "clean\n" # REINTRODUCED: Cleans the disk completely before partitioning/formatting
                f"convert {part_style_lower}\n" # Converts to MBR/GPT
                "create partition primary\n"
                f"format fs={fs_lower} quick\n"
                "assign\n"
                "exit\n"
            )
            # Creates a temporary file for the diskpart script
            diskpart_script_path = "diskpart_script.txt"
            with open(diskpart_script_path, "w") as f:
                f.write(diskpart_script_content)

            # Executes diskpart.exe with the temporary script
            # 'capture_output=True' to get stdout and stderr, 'text=True' for string output
            # 'creationflags=subprocess.CREATE_NO_WINDOW' to prevent console window from flashing
            dp = subprocess.run(["diskpart", "/s", diskpart_script_path], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            os.remove(diskpart_script_path) # Removes the temporary script after execution
            if dp.returncode != 0:
                self.show_error(f"DISKPART FAILED during drive preparation! Check disk and permissions.\nError: {dp.stderr}\n\n"
                                "The USB drive might be in a RAW state. Try using the 'Format Drive' function to recover it.")
                return

            dd_path = "dd.exe" # dd.exe should be in the same directory as the script
            total_size = os.path.getsize(iso) # Total size of the ISO file for progress calculation

            self.set_status("Burning ISO with dd.exe... This may take some time.")
            # Executes dd.exe to burn the ISO to the physical disk
            # 'if={iso}' is the input file (ISO)
            # 'of=\\\\.\\PhysicalDrive{disk_index}' is the output file (the physical disk)
            # 'bs=4M' sets the block size for read/write to 4 Megabytes
            # 'status=progress' makes dd.exe print progress to stderr
            # 'stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True' to capture output
            # 'creationflags=subprocess.CREATE_NO_WINDOW' to prevent console window from flashing
            process = subprocess.Popen([dd_path, f"if={iso}", rf"of=\\\\.\\PhysicalDrive{disk_index}", "bs=4M", "status=progress"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Loop to read dd.exe progress from stderr
            while True:
                line = process.stderr.readline() # dd.exe sends progress updates to stderr
                if not line: # Exit loop when no more lines
                    break
                # Uses regex to find the number of bytes transferred in the progress line
                match = re.search(r"(\d+)\s+bytes transferred", line)
                if match:
                    transferred = int(match.group(1))
                    # Calculates percentage progress and updates the progress bar
                    percent = min(100, int(transferred * 100 / total_size))
                    self.progress["value"] = percent
                    self.update_idletasks() # Forces GUI update to show real-time progress

            process.wait() # Waits for the dd.exe process to complete
            if process.returncode != 0:
                self.show_error(f"dd.exe failed during burning.\nError: {process.stderr.read()}\n\n"
                                "The USB drive might be in a RAW state. Try using the 'Format Drive' function to recover it.")
                return

            self.set_status("ISO burned successfully!")
            messagebox.showinfo("SUCCESS", "ISO burned successfully to USB drive!")

        except Exception as e:
            # Catches any unexpected error and displays it to the user
            self.show_error(f"An unexpected error occurred: {e}\n\n"
                            "The USB drive might be in a RAW state. Try using the 'Format Drive' function to recover it.")
        finally:
            # Ensures buttons are re-enabled, even in case of error
            self.start_btn.config(state="normal")
            self.format_btn.config(state="normal")

    def set_status(self, msg):
        """
        Updates the status message in the graphical interface safely (on the main thread).
        """
        self.status_label.after(0, lambda: self.status_label.config(text=msg))

    def show_error(self, msg):
        """
        Displays an error message in the graphical interface and an error messagebox.
        Executed safely on the main thread.
        """
        self.status_label.after(0, lambda: [
            self.status_label.config(text="ERROR"),
            messagebox.showerror("ERROR", msg)
        ])

if __name__ == "__main__":
    # Checks and requests administrator privileges for the RadishPie application
    if not is_admin():
        run_as_admin()
    else:
        print("Radish Pie: Running with administrator privileges.")
        RadishPie().mainloop()
_RADISHPIE_CODE_END_'''

    # Opens the file for writing (overwrites if exists) with UTF-8 encoding
    with open(RADISHPIE_FILENAME, "w", encoding="utf-8") as f:
        # Remove the unique delimiters before writing to the file
        f.write(radishpie_code.replace(r'''_RADISHPIE_CODE_START_''', '').replace(r'''_RADISHPIE_CODE_END_''', ''))
    print(f"'{RADISHPIE_FILENAME}' created/overwritten successfully.")

    # --- NEW: Hides the radishpie.py file ---
    try:
        subprocess.run(['attrib', '+h', RADISHPIE_FILENAME], creationflags=subprocess.CREATE_NO_WINDOW, check=True)
        print(f"'{RADISHPIE_FILENAME}' hidden successfully.")
    except Exception as e:
        print(f"Warning: Could not hide '{RADISHPIE_FILENAME}': {e}")


    # --- NEW: Creates the .bat file to facilitate running as administrator ---
    BAT_FILENAME = "run_radishpie.bat"
    # .bat file content: uses PowerShell to start the Python script as administrator
    # The 'Start-Process -Verb RunAs' command triggers the UAC prompt
    # 'python.exe' is the Python interpreter, and '%~dp0radishpie.py' ensures the correct script path
    # '%~dp0' expands to the directory of the .bat file, ensuring python.exe finds the script.
    bat_content = f'''@echo off
setlocal
set SCRIPT_DIR=%~dp0
set PYTHON_EXECUTABLE=python.exe

:: Checks if Python is in PATH or tries a common path
where %PYTHON_EXECUTABLE% >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found in PATH. Attempting common path...
    set PYTHON_EXECUTABLE="%LOCALAPPDATA%\\Programs\\Python\\Python*\\python.exe"
    for /f "delims=" %%i in ('dir /b /s /ad "%LOCALAPPDATA%\\Programs\\Python\\Python*"') do (
        if exist "%%i\\python.exe" (
            set PYTHON_EXECUTABLE="%%i\\python.exe"
            goto :found_python
        )
    )
    echo ERROR: Python not found. Please install Python or add it to PATH.
    pause
    exit /b 1
)

:found_python
echo Starting Radish Pie with administrator privileges...
powershell -Command "Start-Process -FilePath %PYTHON_EXECUTABLE% -ArgumentList '\"%SCRIPT_DIR%radishpie.py\"' -Verb RunAs"
if %errorlevel% neq 0 (
    echo ERROR: Failed to start Radish Pie. Check permissions or if Python is installed correctly.
    pause
)
endlocal
'''
    # Writes the content to the .bat file
    with open(BAT_FILENAME, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print(f"'{BAT_FILENAME}' created successfully to facilitate running as administrator.")


# --- Main Setup Script Function ---

def main(pause=True):
    """
    Main function that orchestrates the setup process:
    1. Checks and requests administrator privileges.
    2. Installs necessary Python packages.
    3. Downloads and configures dd.exe.
    4. Creates the radishpie.py file.
    5. Creates the run_radishpie.bat file.
    """
    # Step 1: Check and request administrator privileges for the setup script
    if not is_admin():
        run_as_admin()
        # If run_as_admin() is successful, it will terminate the current process and start a new one.
        # If it fails, it will have already exited with sys.exit(1).
        return # Ensures the rest of the script is not executed in the non-admin instance

    print("Script is running with administrator privileges. Proceeding with setup...")

    # Step 2: Check and install Python packages
    check_and_install_packages()

    # Step 3: Download and configure dd.exe
    success = download_dd()
    if not success:
        print("Setup failed due to a problem downloading dd.exe.")
        print("Please check your internet connection, security software (antivirus), or permissions and try again.")
        # Adds a pause before exiting in case of failure
        if pause:
            input("Press Enter to exit...")
        sys.exit(1) # Exit with error if dd.exe download fails

    # Step 4: Create the radishpie.py file AND the run_radishpie.bat
    write_radishpie()
    print("\nSetup completed successfully!")
    print("To start the Radish Pie application, double-click the 'run_radishpie.bat' file.")
    print("It will automatically request administrator privileges.")
    print("Enjoy using Radish Pie!")

    # Adds a final pause so the console window doesn't close immediately
    if pause:
        input("Press Enter to exit...")

class SetupApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Radish Pie Setup")
        self.geometry("400x200")
        ttk.Label(self, text="Radish Pie Setup").pack(pady=10)
        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=20, pady=10)
        self.status = ttk.Label(self, text="Ready")
        self.status.pack(pady=5)
        ttk.Button(self, text="Run Setup", command=self.start_setup).pack(pady=10)

    def start_setup(self):
        self.progress.start()
        self.status.config(text="Running setup...")
        threading.Thread(target=self.run_setup, daemon=True).start()

    def run_setup(self):
        try:
            main(pause=False)
            self.after(0, self.on_success)
        except SystemExit as e:
            self.after(0, lambda: self.on_exit(e.code))
        except Exception as e:
            self.after(0, lambda: self.on_failure(str(e)))

    def on_success(self):
        self.progress.stop()
        self.status.config(text="Setup completed.")
        messagebox.showinfo("Setup", "Setup completed successfully!")

    def on_exit(self, code):
        self.progress.stop()
        if code == 0:
            self.status.config(text="Setup completed.")
            messagebox.showinfo("Setup", "Setup completed successfully!")
        else:
            self.status.config(text="Setup failed.")
            messagebox.showerror("Setup Failed", f"Setup exited with code {code}")

    def on_failure(self, msg):
        self.progress.stop()
        self.status.config(text="Setup failed.")
        messagebox.showerror("Setup Failed", msg)

if __name__ == "__main__":
    app = SetupApp()
    app.mainloop()

