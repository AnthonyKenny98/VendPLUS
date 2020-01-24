<img src="img/vend.png" alt="project logo image" width="200"/>

# Vend Inventory Upload &middot; [![Known Vulnerabilities](https://snyk.io/test/github/AnthonyKenny98/Vend_Inventory_Upload/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/AnthonyKenny98/Vend_Inventory_Upload?targetFile=requirements.txt) [![Build Status](https://travis-ci.org/AnthonyKenny98/Vend_Inventory_Upload.svg?branch=master)](https://travis-ci.org/AnthonyKenny98/Vend_Inventory_Upload) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/AnthonyKenny98/Vend_Inventory_Upload/blob/master/LICENSE)
> Locally Hosted Web Application for easy CSV upload of inventory numbers for the POS and Inventory Management Software "Vend"

This README is intended to give an overview of this project and how to install and run the application. Help for how to use the application can be found on the initial loading page.


## Table of Contents

+ [Installation/Setup](#setup)
  + [Built With](#builtwith)
  + [Prerequisites](#prereq)
  + [Building](#build)
+ [Versioning](#version)
+ [Configuration](#config)
+ [Tests](#tests)
+ [Style Guide](#style)
+ [API Reference](#api)
+ [Licensing](#license)

## <a name="setup"></a>Installation/Setup

Once you have satisfied all the [prerequisites](#prereq), you can clone the repository:

```shell
git clone https://github.com/AnthonyKenny98/Vend_Inventory_Upload.git
```
Alternatively, you can download the zip of the files [here](https://github.com/AnthonyKenny98/Vend_Inventory_Upload/archive/master.zip).
Extract the files, and double click the Install file. This will open the terminal and walk through the installation. Provided all prerequisites are satisfied, you should not have to do anything during this part.

Once installed, you can open the application by double clicking the executable file generated called "VendPLUS".

### <a name="builtwith"> </a>Built With
+ [Flask](http://flask.palletsprojects.com/en/1.1.x/): The app is a simple, locally hosted web application built with the Flask framework.
+ [Bootstrap](https://getbootstrap.com/): The UI of the app is built using the Bootstrap library. Acknowledgement to [BlackRock Digital](https://github.com/BlackrockDigital) for the [StartBootstrap Admin Template](https://github.com/BlackrockDigital/startbootstrap-sb-admin) template, which served as a foundation for this application's UI.
+ [Jinja2](https://jinja.palletsprojects.com/en/2.10.x/): The python application passes data to the bootstrap UI using the Jinja2 Library.

### <a name="prereq"></a>Prerequisites
+ [Homebrew](https://brew.sh/#install): Homebrew is a package manager for MacOS and Linux. It is only important for downloading and installing Python 3.7.6. Homebrew can be installed by executing the following command in the Terminal:

  ```
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  ```
+ [Python 3.7.6](https://www.python.org/downloads/release/python-376/): Installed with Homebrew
+ [pip3](https://pip.pypa.io/en/stable/): Installed with Homebrew

## <a name="tests"></a>Tests

This project uses pytest for unit testing.

```shell
(venv) $ python3 -m pytest
```

## <a name="style"></a>Style Guide

This project uses the flake8 style guide for python. It can also be tested using pytest:

```shell
(venv) $ python3 -m pytest --flake8
```

## <a name="api"></a>Api Reference

+ [Vend POS API](https://docs.vendhq.com/)

## <a name="license"></a>Licensing

This project is licensed under the MIT License.  See the [LICENSE](LICENSE) file for more information.
