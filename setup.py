import setuptools
import os

HERE = os.path.dirname(__file__)

setuptools.setup(
    name='linediff',
    version="0.1.0",
    author='Tal Wrii',
    author_email='talwrii@gmail.com',
    description='',
    license='GPLv3',
    keywords='',
    url='',
    packages=['linediff'],
    long_description='See https://github.com/talwrii/linediff',
    entry_points={
        'console_scripts': ['linediff=linediff.linediff:main']
    },
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ],
    test_suite='nose.collector',
    install_requires=[]
)
