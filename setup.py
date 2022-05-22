import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Plot 3D Medical Image",
    version="0.0.1",
    author="Pi",
    description="Plot Medical Image.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DreamthreePi/Medical_Image_Plot.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
