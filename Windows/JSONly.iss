;   JSONly is a GUI program for interacting with and manipulating JSON files
;     Copyright (C) 2024  Luke Moyer
;     This program is free software: you can redistribute it and/or modify
;     it under the terms of the GNU General Public License as published by
;     the Free Software Foundation, either version 3 of the License, or
;     (at your option) any later version.

;     This program is distributed in the hope that it will be useful,
;     but WITHOUT ANY WARRANTY; without even the implied warranty of
;     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;     GNU General Public License for more details.

;     You should have received a copy of the GNU General Public License
;     along with this program.  If not, see <https://www.gnu.org/licenses/>.

; this is the Inno Setup script for the Windows installer

[Setup]
AppName=JSONly
SetupIconFile=icon.ico
AppVersion=1.0.0
DefaultDirName={autopf}\JSONly
AppPublisher=Luke Moyer
AppCopyright=Copyright (C) 2024 Luke Moyer
DefaultGroupName=JSONly
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
LicenseFile=..\LICENSE
ChangesAssociations=yes
 
[Code]
procedure InitializeWizard();
begin
  // Hide the "I accept the agreement" and "I do not accept the agreement" radio buttons
  WizardForm.LicenseAcceptedRadio.Checked := True;
  WizardForm.LicenseAcceptedRadio.Visible := False;
  WizardForm.LicenseNotAcceptedRadio.Visible := False;
  
  // Enable the "Next" button on the license page
  WizardForm.NextButton.Enabled := True;
end;

[Messages]
; Customize license page text
WizardLicense=Open-source license
LicenseLabel=This software is licensed under the GNU General Public License (GPL). Please review the terms below.
LicenseLabel3=Important Notice: This is not an End User License Agreement (EULA). You do not need to agree to these terms to install or use this software. You are free to modify and distribute this program, as long as you comply with the terms of this license.

[Files]
Source: "dist\JSONly.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}\doc\"; Flags: ignoreversion
Source: "..\PSFL.txt"; DestDir: "{app}\doc\"; Flags: ignoreversion
Source: "doc\*"; DestDir: "{app}\doc\"; Flags: ignoreversion createallsubdirs recursesubdirs

[Icons]
Name: "{group}\JSONly"; Filename: "{app}\JSONly.exe"; WorkingDir: "{app}"; IconFilename: "{app}\JSONly.exe"
Name: "{commondesktop}\JSONly"; Filename: "{app}\JSONly.exe"; WorkingDir: "{app}"; IconFilename: "{app}\JSONly.exe"; Comment: "A GUI JSON editor"

[Run]
Filename: "{app}\JSONly.exe"; WorkingDir: "{app}"; Description: "Launch JSONly"; Flags: nowait postinstall

[Registry]
Root: "HKCR"; Subkey: ".json"; ValueType: string; ValueName: ""; ValueData: "JSONly"; Flags: uninsdeletekeyifempty
Root: HKCR; Subkey: "JSONly"; ValueType: string; ValueName: ""; ValueData: "JSONly"; Flags: uninsdeletekey
Root: HKCR; Subkey: "JSONly\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\JSONly.bat,0"; Flags: uninsdeletekey
Root: HKCR; Subkey: "JSONly\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\JSONly.bat"" ""%1"""; Flags: uninsdeletekey

; NOTE: Don't use "Flags: ignoreversion" on any shared system files
