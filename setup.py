import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
README += "\n"
README += (HERE / "docs" / "index.md").read_text()

# This call to setup() does all the work
setup(
    name="csaf-lint",
    version="0.0.2",
    description="Experimental CSAF validator for envelope and body profiles.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sthagen/fluffy-funicular",
    author="Stefan Hagen",
    author_email="stefan@hagen.link",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="csaf cvrf validation baseline extension core profile envelope body development",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "jsonschema",
        "xmlschema"
    ],
    entry_points={
        "console_scripts": [
            "csaf-lint=csaf_lint.cli:main",
        ]
    },
)
