Radish Pie - USB ISO Flasher
Radish Pie is a simple and powerful Python-based graphical utility for Windows, designed to easily format USB drives and flash ISO images onto them. It handles administrator privilege elevation automatically, making the process straightforward for users.

Features
Format & Write ISO: Cleanly formats your USB drive and then burns an ISO image onto it, making it bootable.

Format Drive: A dedicated function to format any selected USB drive, especially useful for recovering drives that have become "RAW" or unreadable.

Automatic Administrator Elevation: The application automatically requests administrator privileges upon launch, ensuring smooth operation for disk-related tasks.

Clean Deployment: Ensures a tidy project directory by automatically hiding the main application file (radishpie.py) and the dd.exe utility after setup.

User-Friendly Interface: Built with Tkinter for a simple and intuitive user experience.

Prerequisites
Windows Operating System: This tool is designed specifically for Windows.

Python 3: A working installation of Python 3 (3.6 or newer recommended). Ensure Python is added to your system's PATH during installation for the smoothest experience.

Installation
To set up Radish Pie, simply follow these steps:

Download the Project:
Clone or download the entire Radish Pie project from its GitHub repository to a local folder on your computer.

Run the Setup Script:
Right-click setup.py and select 'Run as administrator' to run it.

The setup.py script will:

Check for and request administrator privileges (a UAC prompt will appear, please click "Yes").

Install necessary Python packages (requests, wmi) if they are not already installed.

Download the dd.exe utility (a crucial tool for low-level disk operations).

Create the main application file radishpie.py.

Create a convenient batch file run_radishpie.bat.

Hide radishpie.py and dd.exe to keep your project folder tidy.

The setup process will pause at the end, prompting you to press Enter before closing the console window.

How to Use Radish Pie
Once the setup is complete, you can start using Radish Pie:

Launch the Application:
In your project folder, double-click the run_radishpie.bat file.

This batch file is configured to automatically request administrator privileges. A UAC prompt will appear; you must click "Yes" for the application to function correctly.

Select Your USB Drive:
From the 'USB Drives' dropdown, carefully select the target USB drive. CRITICAL: Double-check your selection! Operations are irreversible and will permanently erase all data on the chosen drive.

Choose Partition Style and File System:
Select your desired "Partition Style" (MBR or GPT) and "File System" (FAT32 or NTFS).

Note: If your ISO file is larger than 4GB, FAT32 will not be available, and you must select NTFS.

Select Your ISO File:
Click the "Browse" button next to "ISO File" and select the .iso image you wish to flash.

Perform an Action:

Format & Write ISO: Click this button to clean the drive, format it, and then burn the selected ISO image. This is the primary function for creating bootable USB drives.

Format Drive: Click this button if you only want to format the selected USB drive (e.g., to recover a drive that became "RAW" or unreadable after a failed flash attempt). This will clean the drive and format it to your chosen file system.

Troubleshooting
If you encounter any issues while using Radish Pie, refer to the common problems and solutions below:

"DISKPART FAILED!" or "Permission Denied" Error:

Antivirus/Security Software: Your antivirus or firewall might be blocking diskpart.exe or dd.exe as they perform low-level disk operations. Temporarily disable your security software or add exceptions for radishpie.py, dd.exe, and python.exe.

Drive in Use: Ensure no other programs (like File Explorer) are accessing the USB drive. Safely remove the drive from Windows and re-insert it, or restart your computer.

Damaged Drive/Port: Try a different USB drive or a different USB port on your computer.

"Python not found" Error when running run_radishpie.bat:

This means Python is not correctly installed or not added to your system's PATH. Reinstall Python, ensuring the "Add Python to PATH" option is checked during installation.

UAC Prompt Not Appearing (or application fails without it):

Ensure you are running run_radishpie.bat (or setup.py initially) by right-clicking and selecting "Run as administrator." The script includes logic to request elevation, but sometimes manual intervention is needed.

USB Drive Shows as "RAW" or "Unusable" in Disk Management:

This can happen if a previous formatting or flashing operation was interrupted. Use the "Format Drive" button in Radish Pie to recover the drive. This function will perform a full clean and format, making it usable again.

Important Notes
Data Loss Warning: Operations performed by Radish Pie (both "Format & Write ISO" and "Format Drive") will PERMANENTLY ERASE ALL DATA on the selected USB drive. Always double-check that you have selected the correct drive.

Use with Caution: This tool performs low-level disk operations. Use it responsibly and understand the risks involved.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Support
For any issues or questions, please open an issue on the GitHub repository.
