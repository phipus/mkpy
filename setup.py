from setuptools import setup


setup(
    name="mkpy",
    author="phipus",
    author_email="phipuspam@gmx.ch",
    description="A (minimalistic) build tool simmilar to make. Written in Python 3",
    url="https://github.com/phipus/mkpy",
    packages=["mkpy"],
    version="0.0.2",
    entry_points={"console_scripts": "mkpy=mkpy.make:main"},
)