from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='site-primes',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    description='Compteur (mode session) avec détection des nombres premiers pour simuler une activité humaine',
    install_requires=[
        'flask',
        'redis',
        'Flask-Session',
        'Flask-Markdown',
    ],
    python_requires='>=3.6',
    author='Grand Dub',
    author_email='',
    url='https://github.com/jcd717/flask-primes',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicence",
        "Operating System :: OS Independent",
    ],
    long_description_content_type="text/markdown",
    long_description=long_description,
)
