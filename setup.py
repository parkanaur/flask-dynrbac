from setuptools import setup, find_packages
from io import open

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Flask-DynRBAC',
    version='0.0.1',
    packages=find_packages(),
    description='A Flask extension for dynamic role-based access',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/parkanaur/flask-dynrbac',
    author='Daniil Kraynov',
    author_email='krd@airmail.cc',
    install_requires=['flask', 'flask-sqlalchemy'],
    extras_require={
        'api': ['flask-restful']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4'
)
