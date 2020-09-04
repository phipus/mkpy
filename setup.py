from setuptools import setup


setup(
    name="mkpy",
    author="phipus",
    packages=["mkpy"],
    version="0.0.1",
    entry_points={"console_scripts": "mkpy=mkpy.make:main"}
)