# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.3.0 - 4/12/2025
### Fixed
- there is no longer an error popup when using 'save as'
- object and array now shows up in the type chooser again
- long messages in popups no longer hide the button(s)
- objects and arrays are no longer turned into strings
### Changed
- Popups now better handle the modal state
- filepicker now respects language

## v1.2.0 beta - 4/6/2025
### Changed
- icon is now read from a file instead of base64 encoded text
- program no longer terminates when it encounters an error processing the lang file
### Added
- language preferences
## v1.1.0 beta - 4/5/2025
### Changed
- data storage directories are now set for FreeBSD
- relicensed under MIT
- license module now reads the 'LICENSE' file rather than using hard-coded text
### Added
- automatic detection for system theme
- language support
### Removed
- tooltips

## v1.0.1 - 3/31/2025
### Fixed
- remove and edit buttons now work properly

## v1.0.0 - 3/30/2025
### Added
- right-click context menu
- Automatic resize functionality for main listbox
- MacOS compatability
- ability to open files with the app

### Fixed
- interaction with main window no longer allowed while popup shows

### Changed
- main window now has a default size when in windowed mode

## v0.4.0 RC 2 - 1/25/2025
### Added
- licensing for the tooltip module
- functionality to the theme setting

### Fixed
- Fixed a bug causing 'add new item' window to not fully render on some screens

### Changed
- Moved embedded image data to a seperate file
- Reorganized file structure

## v0.4.0 RC - 1/22/2025
### Added
- Preferences
- Theme settings
- Persistent data

### Changed
- Replaced the built-in ctk.Button class with a custom subclass

## v0.3.0 beta - 1/17/2025
### Added
- Settings placeholder

### Removed
- Several buttons that were cluttering space

### Changed
- UI theme new looks more modern

## v0.2.0 beta
### Added
- A menubar with file, edit, and about categories
- More advanced editing mode for simple values

## v0.1.0 alpha - 12/20/2024
### Added
- Initial release
