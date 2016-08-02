from distutils.core import setup
import py2exe

setup(
    name='eventer',
    version='1.70',
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