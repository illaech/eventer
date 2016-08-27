from distutils.core import setup
import py2exe

setup(
    name='eventer',
    version='2.0',
    author='illaech',
    
    windows=[
        {
            'script': 'eventer.py',
            'icon_resources': [(0, 'add.ico')]
        }
    ],
    options={
        'py2exe': {
            'includes': ['sip']
        }
    }
)