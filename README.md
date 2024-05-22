# mytools

[![MIT License](https://img.shields.io/github/license/jotaven/mytools.svg)](https://github.com/jotaven/mytools/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/jotaven/mytools.svg)](https://github.com/jotaven/mytools/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/jotaven/mytools.svg)](https://github.com/jotaven/mytools/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/jotaven/mytools.svg)](https://github.com/jotaven/mytools/issues)

## Overview

This repository is a collection of tools and scripts.

Tem um monte de Funcionabilidades para você utilizar!

You can access on [tools.jotinha.me](tools.jotinha.me) or [mytools.jotinha.me](mytools.jotinha.me)
### Image Processing
- Remove Background
- Collect text with OCR
- Create a scketch
- Get Countours
### Encode & Decode
- QRCode

## How it's done?

- **Docker Integration**: Easily set up and run the project using Docker.
- **API Service**: Contains multiple API methods for different functionalities.
- **Web Application**: A frontend application built with modern web technologies.
- **Nginx Configuration**: Includes Nginx setup for serving the application.
- **Automation Scripts**: Scripts to automate common tasks and processes.

## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation

Clone the repository:

```bash
git clone https://github.com/jotaven/mytools.git
cd mytools
```

Run the project with Docker:

```bash
docker-compose up -d
```

## Usage

After starting the project with Docker, you can access the web application and API services.

🚨 Make ***sure*** the ports 80, 443, 8000 and 8001 are available.

### Web Application

The web application can be accessed at:

```
http://localhost
```

### API Services

API endpoints are available at:

```
http://localhost/api/
```

API documentation is available at:
```
http://localhost/api/docs/
http://localhost/api/redoc/     <----The-Best-one--
```

Refer to the API documentation for more details on available endpoints and their usage.

## Project Structure

```plaintext
mytools/
├── .github/
│   └── workflows/
├── api/
├── app/
├── docker/
├── nginx/
├── scripts/
├── LICENSE
├── README.md
├── docker-compose.yml
└── requirements.txt
```

- **.github/workflows**: GitHub Actions for CI/CD.
- **api**: Backend APIs.
- **app**: Frontend application.
- **docker**: Docker configurations.
- **nginx**: Nginx configurations.
- **scripts**: Automation scripts.
- **docker-compose.yml**: Docker Compose file for setting up the project.
- **requirements.txt**: Python dependencies.


## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/jotaven/mytools/blob/main/LICENSE) file for details.