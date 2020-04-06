import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="middling_export_todoist", # Replace with your own username
    version="0.0.1",
    author="Jacob Williams",
    author_email="jacobaw@gmail.com",
    description="Downloads data from Todoist and saves it to the filesystem.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brokensandals/middling_export_todoist",
    packages=setuptools.find_packages('src'),
    package_dir={'':'src'},
    entry_points={
        'console_scripts': [
            'middling_export_todoist = middling_export_todoist.cli:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    python_requires='>=3.7',
)
