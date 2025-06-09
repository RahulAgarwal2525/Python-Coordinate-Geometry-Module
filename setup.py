from setuptools import setup, find_packages

setup(
    name="Coord_Geom",
    version="0.1",
    description="A modular coordinate geometry library with plotting tools",
    author="Rahul Agarwal",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "scipy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
