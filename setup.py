import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdk-py",
    version="1.1.0.post1",
    author="Emre Özcan",
    author_email="justsomechars@gmail.com",
    description="Python API for the Turkish Language Foundation",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/EmreOzcan/tdk-py",
    project_urls={
        "Issue Tracker": "https://github.com/EmreOzcan/tdk-py/issues",
    },
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    package_dir={
        "": "src",
    },
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
