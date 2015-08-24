#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Contact: hephaestos@riseup.net - 8764 EF6F D5C1 7838 8D10 E061 CF84 9CE5 42D0 B12B

import os, sys

help_message = """This password strengthener will add up to 24 bits security to your password.\nAfter you entered your password, you have to wait a few seconds.\nOnce you see a 'Go ahead!' message, your password is attached to your clipboard.\n15 seconds after the 'Go ahead!' message, your clipboard will be wiped.\nPassword strengthening should take between 20 and 40 seconds.\n\nOptions:\n-h\t--help\t\tShow this helpful message.\n-p\t--print\t\tDon't attach password to clipboard\n\t\t\tPrint to terminal instead\n-l\t--leave\t\tLeave password attached to clipboard.\n-v\t--verify\tAsk password twice for verification.\n\n"""

	
def countdown(seconds):
	# Shows a countdown in the terminal
	from time import sleep
	os.system('setterm -cursor off')
	for i in range(seconds,0, -1):
		sys.stdout.write(str(i) + '     \r')
		sleep(1)
	os.system('setterm -cursor on')


def encode(b):
    """Encode bytes to a base58-encoded string"""
    from binascii import hexlify
    b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    # Convert big-endian bytes to integer
    n = int('0x0' + hexlify(b).decode('utf8'), 16)

    # Divide that integer into base58
    res = []
    while n > 0:
        n, r = divmod (n, 58)
        res.append(b58_digits[r])
    res = ''.join(res[::-1])

    # Encode leading zeros as base58 zeros
    czero = b'\x00'
    if sys.version > '3':
        # In Python3, indexing a bytes returns numbers, not characters.
        czero = 0
    pad = 0
    for c in b:
        if c == czero: pad += 1
        else: break
    return b58_digits[0] * pad + res


def derive(base):
	from hashlib import sha224, sha512
	
	if sys.version > '3':
		# Get bytes from string
		base = bytes(base, 'utf-8')
	
	for _ in xrange(2**24):
		base = sha512(base).digest()

	return encode(sha224(base).digest())


def clip(string):
	os.system("echo -n '" + string + "' | xclip -selection clipboard")


if __name__=="__main__":
	args = set(sys.argv[1:])

	# Check if all command line arguments are understood
	for arg in args:
		if arg not in set(['-h','--help','-p','--print','-l','--leave','-v','--verify']):
			print("Option not understood, showing help instead.\n")
			sys.exit( help_message )
	
	# Check that -l and -p are not both set:
	if '-p' in args or '--print' in args:
		if '-l' in args or '--leave' in args:
			print("Don't combine '-p' and '-l' options!\n")
			sys.exit(help_message)

	# If help is asked, only show help message
	if '-h' in args or '--help' in args:
		sys.exit( help_message )
	
	# Import to ask the password:
	from getpass import getpass
	base = getpass("Password to derive from:")
	if '-v' in args or '--verify' in args:
		base_v = getpass("Verify password:")
		if not base == base_v:
			sys.exit("Passwords you typed did not match!")
	
	# Get the password
	password = derive(base)
	
	# Communicate password in desired way
	if '-p' in args or '--print' in args:
		# Just print password to screen:
		print( password )
	else:
		# Place password on clipboard:
		clip(password)
		print("Go ahead!")
		
		if '-l' not in args and '--leave' not in args:
			# Flush clipboard after countdown ends:
			countdown(15)
			clip('TooLate!')
			print("Password no longer available")
