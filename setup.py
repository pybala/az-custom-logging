from os import path
from setuptools import setup, find_packages
 
curPath = path.abspath(path.dirname(__file__))

with open(path.join(curPath, 'README.md'), encoding='utf-8') as f:
    longDescription = f.read()
 

if __name__ == '__main__':
    setup(
        name="az-custom-logging",
        version="0.0.1",
        author="Balakumar Parameshwaran",
        author_email="youcompleteit@gmail.com",
        description="Package for Azure custom logging",
        long_description=longDescription,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        license="MIT",
        keywords="utils",
        classifiers=[
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        python_requires='>=3.7',
        install_requires=["requests", "aiohttp"],
    )