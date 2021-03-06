from setuptools import setup, find_packages

with open("requirements.txt", "r") as req_fp:
    required_packages = req_fp.readlines()

# Use README for long description
with open("README.md", "r") as readme_fp:
    long_description = readme_fp.read()

setup(
    name="oc_web_scraper",
    version="1.0.0",
    author="PabloLec",
    author_email="pablolec@pm.me",
    description="Demo web scraper made for OpenClassrooms studies.",
    license="MIT License",
    keywords="web scraping scraper",
    url="https://github.com/PabloLec/oc_web_scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "docs"]),
    entry_points={
        "console_scripts": [
            "oc_web_scraper = oc_web_scraper:main",
        ],
    },
    install_requires=required_packages,
    package_data={"oc_web_scraper": ["config.yml"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
