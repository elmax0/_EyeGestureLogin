from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="depthai_recorder",
    version="0.1.0",
    author="Omair Shahzad Bhatti",
    author_email="ombh01@dfki.de",
    description="A video recording package using DepthAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(
        include=["depthai_recorder.*", "depthai_recorder"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "depthai",
        "ffmpeg"
    ],
)
