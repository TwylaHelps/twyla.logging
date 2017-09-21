from setuptools import setup

dependencies = ['PyYAML>3', 'parse', 'mimeparse']

setup(
    name="twyla.logging",
    version="0.1",
    author="Twyla Devs",
    author_email="dev@twylahelps.com",
    description=("Twyla Logging Utilities"),
    install_requires=dependencies,
    extras_require={
        'test': ['pytest', 'pylint'],
    },
    packages=["twyla.logging"],
    entry_points={},
    url="https://bitbucket.org/twyla/twyla.raml",
)
