import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hydrate",
    version="0.1.0",
    author='andrewDoing',
    author_email='andrew.doing@mst.edu',
    description="A package to generate an HLD for your kubernetes cluster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewDoing/hydrate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
)
