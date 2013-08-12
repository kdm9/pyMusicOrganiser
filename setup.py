from __future__ import print_function
from setuptools import setup

desc = """
pyMusicOrganiser (pymo)

Renames and organises your music collection based on id3 tags.
"""

setup(
    name="pyMusicOrganiser",
    packages=['pymo', ],
    install_requires=["id3reader==1.53.20070415", "docopt==0.6.1",],
    version="0.1",
    description=desc,
    author="Kevin Murray",
    author_email="k.d.murray.91@gmail.com",
    url="https://github.com/kdmurray91/pyMusicOrganiser",
    keywords=["music", "id3",],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "License :: OSI Approved :: GNU General Public License v3 or later " +
            "(GPLv3+)",
        ],
    test_suite="test",
    scripts=["bin/pymo",],
#    data_files=[
#        ("share/doc/pymo", ["README.txt",]),
#        ]
    )
