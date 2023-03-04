from distutils.core import setup

# Readme file
readmeFilename = "README.md"

setup(
    #
    # Change This Section
    #

    # Name of package
    # Should be the same as the import name and the folder name in src/
    name="fluent_toolkit",
    packages=["fluent_toolkit"],
    package_data={"fluent_toolkit": ["lib/*",
                                            "lib/*/*",
                                            "lib/*/*/*",
                                            "lib/*/*/*/*",
                                         ]},

    # Version of the package
    # Format X.Y.Z Based on Semantic Versioning
    # https://semver.org
    version="1.4.0",

    # Short description
    description="A system for executing fluent in an automated fashion.",

    # Author
    author="Scott Lindsay",

    # Dependencies
    # This list is found by running "pip freeze" in the activated venv
    # DO NOT include the package this setup.py file defines
    # When possible, change the ==X.Y.Z to >=X.Y.Z<X+1.Y.Z
    install_requires=["numpy",
                      "matplotlib",
                      "jinja2",
                      "pytest",
                      ],

    #
    # Keep This Section The Same
    #
    package_dir={"": "src", },
    long_description=open(readmeFilename, "r").read(),
    long_description_content_type="text/markdown",

    #
    # Optional Section
    #

    # If command line access is needed
    # point to the main function here
    entry_points={"console_scripts": ["c6_example_package=c6_example_package.core:testModPrint"]},
)
