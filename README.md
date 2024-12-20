# JSONly

Jsonly is a lightweight, user-friendly GUI JSON editor designed to make working with JSON files simple and efficient. Built with a focus on usability, Jsonly provides an intuitive interface for viewing, editing, and managing JSON data without overwhelming you with unnecessary features.

## Features
- Tree-View Editing: Easily navigate and edit the structure of your JSON data.
- Plain Text Viewer: View and copy the raw JSON content with a single click.
- Save and load queues from files

Jsonly is perfect for developers, data analysts, or anyone needing a reliable tool to manage JSON files. Whether you're debugging APIs, managing configurations, or just exploring JSON, JSONly has you covered.

## Installing Dependencies (for running from source):
If you plan to run JSONly from the source code, you will need to install the following dependencies:

1. **tkfilebrowser** (only on Linux):
   ```bash
   pip install tkfilebrowser
2. **Python** 3.8 or above
   - For Linux (note: most Linux distributions come with Python preinstalled):
     - For **Debian-based distributions** (e.g., Ubuntu):
       ```bash
       sudo apt install python3
      - For **Red Hat-based distributions** (e.g., Fedora, CentOS):
         ```bash
         sudo dnf install python3
     - For **Arch Linux**:
         ```bash
         sudo pacman -S python
     - For other Linux distributions, you can search for Python in your package manager. Alternatively, you can check your distribution’s documentation for installation instructions specific to Python.
   - For Windows
     - Installing from **Winget**:
         ```bash
         winget install Python.Python3.12
     - Windows installer:
         https://www.python.org/downloads/windows/
   - Other download options:
         https://python.org/downloads

## Platform Compatibility
JSONly has been tested on Linux and Windows. It has not been tested on macOS, so compatibility on macOS is not guaranteed.

## Usage
Run the executable for a hassle-free experience.
If running from source, use the following command:
```bash
python JSONly.pyw
```
## License
JSONly is released under the GPL License. See the [LICENSE](https://github.com/DudenessBoy/JSONly/blob/main/LICENSE) file for more details.
