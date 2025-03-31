import icnsutil

# Load the PNG file
icon = icnsutil.IcnsFile()
icon.add_media(file='../icon.png')

# Write the ICNS file
icon.write('JSONly/resources/icon.icns')
