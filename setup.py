from setuptools import setup, find_packages


with open('pyhiss/__init__.py') as f:
    info = {}
    for line in f.readlines():
        if line.startswith('version'):
            exec(line, info)
            break


setup_info = dict(
    name='pyhiss',
    version=info['version'],
    author='Bryan Goodrich',
    author_email='Bryan.Goodrich@smud.org',
    url='',
    download_url='http://pypi.python.org/pypi/pyhiss',
    project_urls={
        'Documentation': 'https://pyglet.readthedocs.io/en/latest',
        'Source': 'https://github.com/bryan-goodrich/hiss',
        'Tracker': 'https://github.com/bryan-goodrich/hiss/issues',
    },
    description='Feed the snek',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Package info
    packages=['pyhiss'] + ['pyhiss.' + pkg for pkg in find_packages('pyhiss')],

    # Add _ prefix to the names of temporary build dirs
    options={'build': {'build_base': '_build'}, },
    zip_safe=True,
)
