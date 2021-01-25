# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false
import setuptools

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

setuptools.setup(
    name="absqrtc",
    version="2021.04",
    author="Mushinako",
    author_email="ridoedee@gmail.com",
    description="a + b sqrt(c) calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mushinako/absqrtc",
    packages=setuptools.find_packages(include=("absqrtc",)),
    package_data={
        "absqrtc": ["*.pyi", "py.typed"],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
