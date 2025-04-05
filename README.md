# JSONly

JSONly is a lightweight, user-friendly GUI JSON editor designed to make working with JSON files simple and efficient. Built with a focus on usability, JSONly provides an intuitive interface for viewing, editing, and managing JSON data without overwhelming you with unnecessary features.

## Features
- Plain Text Viewer: View and copy the raw JSON content with a single click.
- Open any JSON file for easy editing

JSONly is perfect for developers, data analysts, or anyone needing a reliable tool to manage JSON files. Whether you're debugging APIs, managing configurations, or just exploring JSON, JSONly has you covered.

## Installing Dependencies (for running from source):
If you plan to run JSONly from the source code, you will need to install the following dependencies:

1. **Python requirements** (requirements.txt)
   ```bash
   pip install -r requirements.txt
2. **Xsel** (Linux only)
   - For **Debian-based distributions** (e.g., Ubuntu):
       ```bash
       sudo apt install xsel
      - For **Red Hat-based distributions** (e.g., Fedora, CentOS):
         ```bash
         sudo dnf install xsel
     - For **Arch-based distributions** (e.g. Manjaro, EndeavorOS):
         ```bash
         sudo pacman -S xsel
     - For other Linux distributions, you can search for xsel in your package manager.
3. **Python** 3.10 or above
   - For Linux (note: most Linux distributions come with Python preinstalled):
     - For **Debian-based distributions** (e.g., Ubuntu):
       ```bash
       sudo apt install python3
      - For **Red Hat-based distributions** (e.g., Fedora, CentOS):
         ```bash
         sudo dnf install python3
     - For **Arch-based distributions** (e.g. Manjaro, EndeavorOS):
         ```bash
         sudo pacman -S python
     - For other Linux distributions, you can search for Python in your package manager. Alternatively, you can check your distribution’s documentation for installation instructions specific to Python.
   - For Windows
     - Installing from **Winget**:
         ```bash
         winget install Python.Python3.13
     - Windows installer:
         https://www.python.org/downloads/windows/  
   - For MacOS
     - Installing from **Homebrew**
        ```bash
        brew install python@3.13
     - MacOS PKG installer:
         https://www.python.org/downloads/macos/
   - Other download options:
         https://python.org/downloads  

## Platform Compatibility
JSONly has been tested on Linux, MacOS, and Windows on x86_64 processors. ARM compatibility is not guaranteed, but should work.

Mobile compatibility (Android and iOS) is planned but not yet implemented.

## Usage
Run the release file for a hassle-free experience.
If running from source, use the following command:
```bash
python main.pyw
```
## License
This project is licensed under the MIT License starting from version 1.1.0-beta. See the [LICENSE](https://github.com/DudenessBoy/JSONly/blob/main/LICENSE) file for more details.

Versions 1.0.1 and earlier were released under the GNU General Public License v3.0 (GPL-3.0).
You can find the GPL-licensed source code by checking out the appropriate tags/releases in this repository.

## Additional links
Project website: https://DudenessBoy.github.io/JSONly  
SourceForge page: https://jsonly.sourceforge.net  
Discord server: https://discord.gg/gVFkaZpUhp  
Subreddit: https://reddit.com/r/JSONly  

## Contributing
If you encounter an issue or have a feature request, please submit it on the [GitHub Issues page](https://github.com/DudenessBoy/JSONly/issues). Developers with coding experience are encouraged to fork the repository and contribute by submitting a pull request. For those interested in becoming an active contributor to the project, please [reach out](https://dudenessboy.github.io/contact.html) to the author directly.
