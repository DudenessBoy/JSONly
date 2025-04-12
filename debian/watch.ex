# Example watch control file for uscan.
# Rename this file to "watch" and then you can run the "uscan" command
# to check for upstream updates and more.
# See uscan(1) for format.

# Compulsory line, this is a version 4 file.
version=4
https://

# GitHub hosted projects.
opts="filenamemangle=s%(?:.*?)?v?([0-9]+(?:\.[0-9]+)+)(@ARCHIVE_EXT@)%@PACKAGE@-$1%" \
   https://github.com/DudenessBoy/JSONly/tags \
   v?([0-9]+(?:\.[0-9]+)+)@ARCHIVE_EXT@
