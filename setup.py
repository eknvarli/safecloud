from setuptools import setup, find_packages

setup(
    name="safecloud",
    version="1.0.0",
    description="Smart cloud security at a glance",
    packages=find_packages(),
    install_requires=[
        "click",
        "rich",
        "boto3",
        "cryptography",
        "requests",
        "pyfiglet",
        "dnspython",
        "gpt4all"
    ],
    entry_points={
        "console_scripts": [
            "safecloud = safecloud.cli:cli"
        ]
    },
    license="GPL-3.0-or-later",
    python_requires=">=3.8",
)
