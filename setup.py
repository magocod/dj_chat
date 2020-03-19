from setuptools import find_packages, setup

from dj_chat import __version__

setup(
    name="dj_chat",
    version=__version__,
    url="https://github.com/magocod/dj_chat",
    author="Yson",
    author_email="androvirtual12@gmail.com",
    description="basic chat application, using websockets",
    python_requires=">=3.7",
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
