if __name__=="__main__":
	import os
	import sys
	from time import sleep

	def countdown(seconds):
		# Shows a countdown in the terminal
		os.system('setterm -cursor off')
		for i in range(seconds,0, -1):
			sys.stdout.write(str(i) + '     \r')
			sleep(1)
		os.system('setterm -cursor on')

	message = """This password strengthener will add about 24 bits security to your password. After you entered your password you should wait a few seconds. Once you see the 'Go ahead!' message your password is attached to your clipboard. 15 seconds after the 'Go ahead!' message your clipboard will be wiped.\nPassword strengthening should take between 20 and 30 seconds\n\nOptions:\n-h\t--help\t\tShow this helpful message.\n-p\t--print\t\tDon't attach password to clipboard but print to terminal\n-l\t--leave\t\tLeave password attached to clipboard.\n-v\t--verify\tAsk password twice for verification.\n\n"""

	args = set(sys.argv[1:])

	# Check if all command line arguments are understood
	for arg in args:
		if arg not in set(['-h','--help','-p','--print','-l','--leave','-v','--verify']):
			print("Option not understood, showing help instead.\n")
			print( message )
			sys.exit(0)

	# If help is asked, only show help message.
	if '-h' in args or '--help' in args:
		sys.exit( message )
	
	# Derive password:
	else:
		if '-p' in args or '--print' in args:
			# Print password to screen:
			from kdf_helper import derive
			print( derive('-v' in args or '--verify' in args) )
		else:
			# Place password on clipboard:
			verify = "-v " if ( '-v' in args or '--verify' in args ) else ""
			os.system("python3 kdf_helper.py " + verify + "| xclip -selection clipboard")
			print("Go ahead!")
			
			if '-l' not in args and '--leave' not in args:
				# Flush clipboard after countdown ends:
				countdown(15)
				os.system("echo 'Too late!' | xclip -selection clipboard")
				print("Password no longer available")

		
