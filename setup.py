"""Setup configuration for Idea2Image package."""

from setuptools import setup, find_packages

with open("Readme_new.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f
                    if line.strip() and not line.startswith("#")]

setup(
    name="idea2image",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description=(
        "Turn ideas into rendering-ready AI image prompts "
        "using templates, semantic search, and LLM refinement"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/idea2image",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "idea2image=app.ui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "app": ["attribute_config.json"],
        "data": ["sample_prompts.json"],
    },
)
