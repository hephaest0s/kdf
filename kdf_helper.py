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


