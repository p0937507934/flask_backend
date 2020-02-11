import os
import re

from setuptools import setup

install_requires = [
    "flask==1.1.1",
    "requests==2.22.0",
    "flask_sqlalchemy==2.4.1",
    "pymysql==0.9.3",
    "sqlalchemy_utils==0.36.1",
    "numpy==1.15.0",
    "spectral==0.20",
    "scikit-image==0.13.1"
]
dev_requires = ["black==19.3b0", "isort==4.3.21", "pylint==2.4.3"]
test_requires = [
    "coverage==4.5.4",
    "pytest==5.2.1",
    "pytest-cov==2.8.1",
    "pytest-html==2.0.0",
    "pytest-runner==5.1",
    "tox==3.14.0",
]

package_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "haoez_api_server"
)
init_path = os.path.join(package_path, "__init__.py")
with open(init_path, "r") as f:
    version = re.findall(r"^__version__ = \"([^']+)\"\r?$", f.read(), re.M)[0]

setup(
    name="haoez_api_server",
    version=version,
    packages=["haoez_api_server"],
    install_requires=install_requires,
    extras_require={"dev": dev_requires + test_requires, "test": test_requires},
)
