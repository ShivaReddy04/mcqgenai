from setuptools import setup, find_packages


setup(
    name="mcqgenerator",
    version="0.1.0",
    description="Simple MCQ generator from text",
    author="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mcqgen=mcqgenerator.cli:main",
        ]
    },
)


