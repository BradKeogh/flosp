import os
try:
    print('hi')
    os.chdir(os.path.join(os.getcwd()))
    print(os.getcwd())
except:
	pass

import flosp