.\"                                      Hey, EMACS: -*- nroff -*-
.\" (C) Copyright 2025 Luke Moyer <DudenessBoy_software@disroot.org>,
.\"
.\" First parameter, NAME, should be all caps
.\" Second parameter, SECTION, should be 1-8, maybe w/ subsection
.\" other parameters are allowed: see man(7), man(1)
.\" Manpage for Jsonly
.TH JSONLY 1 "March 2025" "1.0.1" "Jsonly Manual"
.SH NAME
jsonly \- A graphical JSON editor
.SH SYNOPSIS
.B jsonly
[\fIoptions\fR]
.SH DESCRIPTION
Jsonly is a simple graphical tool to view, edit, and manage JSON files.
.PP
It offers features such as a graphical list of keys and editing values with the simple text entry
.SH OPTIONS
.TP
.B \-h, \-\-help
Show help message and exit.
.TP
.B \-v, \-\-version
Show version information and exit.
.SH EXAMPLES
To open a JSON file:
.PP
.B jsonly example.json
.SH SEE ALSO
json(1), jq(1)
