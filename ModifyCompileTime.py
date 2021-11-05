import pefile
from struct import unpack
from binascii import hexlify, a2b_uu

# Reference: https://github.com/deptofdefense/SalSA/wiki/PE-File-Format
def getTimeDateStamp(filename):
    pe = pefile.PE(filename)
    print("TimeDateStamp: "+hex(pe.FILE_HEADER.TimeDateStamp))

# Reference: https://gist.github.com/geudrik/03152ba1a148d9475e81
def writeTimeDateStamp(filename, newTimeDateStamp):
    # Open file in read or write binary mode r+b
    try:
        filehandle = open(filename, 'r+b')
        # Check that file opened is Portable Executable file
        if hexlify(filehandle.read(2)) != hexlify(bytes('MZ', encoding="utf8")):
            filehandle.close()
            print("File is not in PE format!")
            return
    except Exception as e:
        print(e)
        return

    # Find the offset of the timeDateStamp and write into it
    try:
        # Get PE offset (@60, DWORD) from DOS header
        #   It's little-endian so we have to flip it
        #   We also need the HEX representation which is an INT value
        filehandle.seek(60, 0)
        offset = filehandle.read(4)
        offset = hexlify(offset[::-1])

        # This was added in due to an issue with offset being set to '' on rare occasions (see comments below)
        if offset == '':
            print("offset is empty")
            filehandle.close()
            return

        #   ValueError: invalid literal for int() with base 16: ''
        #   https://stackoverflow.com/questions/11826054/valueerror-invalid-literal-for-int-with-base-16-x0e-xa3-python
        #   https://stackoverflow.com/questions/20375706/valueerror-invalid-literal-for-int-with-base-10-python
        #       This indicates that for some reason, 'offset' from above is being set as '' and thus can't be converted to a base 16 int
        offset = int(offset, 16)

        # Seek to PE header and read second DWORD
        filehandle.seek(offset+8, 0)
        filehandle.write(newTimeDateStamp)
        filehandle.close()
    except Exception as e:
        print(e)
        return

getTimeDateStamp("test.exe")
# Changing timeDateStamp field to 5c4570dd
writeTimeDateStamp("test.exe", bytes.fromhex('dd70455c'))
getTimeDateStamp("test.exe")
