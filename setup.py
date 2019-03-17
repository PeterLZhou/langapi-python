import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="langapi",
    version="0.0.1",
    description="Python module for Lang API - see https://docs.langapi.co/ for more information.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/peterlzhou/langapi-python",
    author="Peter Zhou",
    author_email="peter@langapi.co",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude="__tests__"),
    include_package_data=True,
    install_requires=[],
    entry_points={},
)
