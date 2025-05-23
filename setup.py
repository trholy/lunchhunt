from setuptools import setup, find_packages

setup(
    name="lunchhunt",
    version="0.1.0",
    author="Thomas R. Holy",
    author_email="thomas.robert.holy@gmail.com",
    description="LunchHunt! Your Personal Food Concierge!",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/trholy/lunchhunt",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license_files=('LICENSE',),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.32.3",
        "beautifulsoup4>=4.13.3",
        "dash>=3.0.0"
    ],
    extras_require={
        "dev": [
            "pytest",
            "ruff"
        ]
    },
    test_suite='pytest',
    entry_points={
        'console_scripts': [
            'lunchhunt-web = lunchhunt.web.webUI:main',
        ]
    },
)
