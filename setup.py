from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proxytunnel",
    version="0.1.0",
    author="workwhileweb",
    author_email="workwhileweb@gmail.com",
    description="fast forward proxy tunnel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/workwhileweb/proxytunnel",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
)
