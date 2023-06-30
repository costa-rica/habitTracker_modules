from setuptools import setup

setup (
    name="ht-modules",
    version = "0.1",
    author="NickRodriguez",
    author_email="nick@dashanddata.com",
    description = "ht stands for Habit Tracker",
    packages=['ht_config','ht_models'],
    python_requires=">=3.6",
    )