from setuptools import setup, find_packages

setup(
    name="tbutils",
    url="https://github.com/tboulet/tbutils", 
    author="Timothé Boulet",
    author_email="timothe.boulet0@gmail.com",
    
    packages=find_packages(),

    version="1.1",
    license="MIT",
    description="tbutils is a package of utility functions for python.",
    long_description=open('README.md').read(),      
    long_description_content_type="text/markdown",  
)