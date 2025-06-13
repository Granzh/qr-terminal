from setuptools import setup, find_packages
import os

def read_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "QR Code generator for terminal - pipe any output to QR codes"

setup(
    name="qr-terminal",
    version="1.0.0",
    author="FlintWithBlackCrown",
    author_email="kbolokhov@gmail.com",
    description="Generate QR codes in terminal from piped input or arg",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qr-terminal",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
        "Topic :: System :: Shells",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
    install_requires=[
        "qrcode[pil]>=7.0",
    ],
    entry_points={
        "console_scripts": [
            "qrterm=qr_terminal.__main__:main",
        ],
    }, 
    project_urls={
        "Bug Reports": "https://github.com/yourusername/qr-terminal/issues",
        "Source": "https://github.com/yourusername/qr-terminal",
    },
    keywords="qr qrcode terminal cli pipe linux unix",
    include_package_data=True,
)