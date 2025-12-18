from setuptools import setup, find_packages

setup(
    name="pypandoc-hwpx",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'pypandoc_hwpx': ['blank.hwpx'],
    },
    install_requires=[
        "pypandoc",
        "Pillow",
    ],
    entry_points={
        'console_scripts': [
            'pypandoc-hwpx=pypandoc_hwpx.cli:main',
        ],
    },
    author="pypandoc-hwpx Contributors",
    url="https://github.com/msjang/pypandoc-hwpx",
    project_urls={
        "Source": "https://github.com/msjang/pypandoc-hwpx",
        "Tracker": "https://github.com/msjang/pypandoc-hwpx/issues",
    },
    description="Convert Markdown/DOCX to HWPX using Pandoc AST",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
