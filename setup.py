from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="locust-performance-framework",
    version="1.0.0",
    author="Pritam Dharme",
    author_email="pritamdharme@gmail.com",
    description="Production-grade performance testing framework with Locust, Python, and CI/CD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pritamdharme/locust-performance",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.11",
    install_requires=[
        "locust==2.24.0",
        "requests==2.31.0",
        "python-dotenv==1.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "locust-perf=locust.main:main",
        ],
    },
)
