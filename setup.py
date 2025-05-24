from setuptools import setup, find_packages

setup(
    name="aurorabot",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "nextcord>=2.0.0",
        "psutil>=5.9.0",
        "pyyaml>=6.0.0",
    ],
    python_requires=">=3.8",
    author="Aurora Development Team",
    author_email="your.email@example.com",
    description="A Discord bot built with Nextcord",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AuroraDevelopmentTeam/AuroraBot",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 