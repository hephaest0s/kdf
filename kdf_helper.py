# Import for hashing:
import hashlib, binascii
# Import to ask the password:
from getpass import getpass

# Function that will ask and derive the password
def derive(verify=False):
	# Query the base password
	base = getpass("Password to derive from:")
	if verify:
		base_v = getpass("Verify password:")
		assert base == base_v, "Passwords you typed did not match!"

	# Get bytes from string
	base = bytes(base, 'utf-8')

	# Perform 2^24 HMAC operations using sha512
	# That means over 16.000.000 times hmac-sha-512
	data = hashlib.pbkdf2_hmac('sha512', base, base, 2**24)

	# Perform one last sha224 operation and get hex values.
	password = hashlib.sha224(data).hexdigest()

	return password

if __name__=="__main__":
	# Import for printing without newline:
	import sys

	# Print the password without newline
	sys.stdout.write( derive( '-v' in sys.argv or '--verify' in sys.argv ) )


