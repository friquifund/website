"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import os
import pathlib

here = pathlib.Path(__file__).parent.resolve()


def get_requirements_list():
    # get requirements list from requirements.txt
    requirements_list = open(os.path.join(here, "requirements.txt")).read().strip().split("\n")

    # clean requirements list
    requirements_list = [x for x in requirements_list if x.strip() != ""]
    requirements_list = [x for x in requirements_list if not x.startswith("#")]
    return requirements_list


requirements_list = get_requirements_list()


setup(
    name="scraper",
    version="0.0.1",
    description="",
    long_description="",

    # The project's main homepage.
    # url='https://github.com/pypa/sampleproject',

    # Author details
    author="Borja",
    author_email="",

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs"]),
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=[],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        "src": ["configs/*.yaml"],
    },
    install_requires=requirements_list,

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

)