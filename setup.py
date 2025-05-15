from setuptools import setup, find_packages

setup(
    name="product_matching",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.4.0",
        "rapidfuzz>=2.0.0",
        "openpyxl>=3.0.0"
    ],
    author="Ayesha",
    description="Product Matching Pipeline with strict validation rules and fuzzy matching",
    python_requires=">=3.7"
)
