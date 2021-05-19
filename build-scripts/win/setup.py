# http://www.py2exe.org/index.cgi/ListOfOptions

from distutils.core import setup
import py2exe

setup(
        windows=[{
        	"script":"vidstabgui.py", 
        	"icon_resources": [(1, "icon/icon.ico")]
        	}],
        data_files = [(
        	'.', ['ffmpeg.exe']
        	)],
        options={
                "py2exe":{
                		'bundle_files': 1,
                		'compressed': True,
                        "unbuffered": True,
                        'dist_dir': './dist',
                        "optimize": 2,
                        'includes': [
			                'tkinter',
			                'subprocess',
			                'time',
			                'os'
			                ]
                }
        }
)