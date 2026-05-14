# 🚀 DNS Harvest

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/the-cybercaptain/dns-harvest?style=for-the-badge&logo=github)](https://github.com/the-cybercaptain/dns-harvest/stargazers)

[![GitHub forks](https://img.shields.io/github/forks/the-cybercaptain/dns-harvest?style=for-the-badge&logo=github)](https://github.com/the-cybercaptain/dns-harvest/network)

[![GitHub issues](https://img.shields.io/github/issues/the-cybercaptain/dns-harvest?style=for-the-badge&logo=github)](https://github.com/the-cybercaptain/dns-harvest/issues)

[![GitHub license](https://img.shields.io/github/license/the-cybercaptain/dns-harvest?style=for-the-badge)](https://github.com/the-cybercaptain/dns-harvest/blob/main/LICENSE)

[![Python version](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)

**A powerful, modular DNS Reconnaissance and OSINT Harvesting tool in Python.**
🔍⚡ Conduct automated subdomain discovery, email mining, advanced DNS auditing, and flexible data export.

</div>

## 📖 Overview

DNS Harvest is a sophisticated command-line interface (CLI) tool designed for cybersecurity professionals, penetration testers, and researchers to perform comprehensive DNS reconnaissance and Open-Source Intelligence (OSINT) gathering. Leveraging a modular architecture, it automates the process of identifying subdomains, extracting email addresses, performing in-depth DNS record analysis, and detecting advanced DNS vulnerabilities like spoofing and wildcard configurations.

The tool focuses on efficiency and flexibility, supporting various data export formats and offering granular control over its harvesting and auditing capabilities. It is engineered to provide actionable intelligence by meticulously analyzing an organization's DNS footprint.

## ✨ Features

-   🎯 **Automated Subdomain Discovery**: Utilize multiple techniques (e.g., brute-forcing, search engine scraping, certificate transparency logs) to uncover extensive subdomain lists.
-   📧 **Email Address Harvesting**: Scan web pages and other sources to extract publicly available email addresses for OSINT purposes.
-   🔬 **Advanced DNS Auditing**:
    -   **DNS Record Enumeration**: Query and analyze various DNS record types (A, AAAA, MX, NS, TXT, SPF, SRV, CNAME).
    -   **DNS Spoofing Detection**: Identify potential DNS cache poisoning or response manipulation.
    -   **Wildcard DNS Detection**: Pinpoint domains configured with wildcard DNS records.
-   🌐 **WHOIS Information Retrieval**: Perform lookups to gather domain registration details.
-   💻 **Operating System Detection**: Attempt to infer the operating system of discovered hosts based on DNS/network characteristics.
-   📦 **Multi-format Data Export**: Save reconnaissance results in various formats like CSV, JSON, or plain text for further analysis or integration.
-   ⚡ **Asynchronous Operations**: Utilize `asyncio` and `aiohttp` for high-performance, concurrent network requests.
-   🎨 **Rich Terminal Output**: Enjoy a user-friendly command-line experience with colored output and progress indicators using `rich` and `colorama`.
-   🧩 **Modular Design**: Easily extendable architecture allowing for new reconnaissance modules to be integrated.

## 🛠️ Tech Stack

**Runtime:**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**Core Libraries:**
-   [![requests](https://img.shields.io/badge/requests-HTTP_Library-000000?style=for-the-badge&logo=python&logoColor=white)](https://requests.readthedocs.io/en/latest/)
-   [![dnspython](https://img.shields.io/badge/dnspython-DNS_Tools-blueviolet?style=for-the-badge&logo=python&logoColor=white)](https://www.dnspython.org/)
-   [![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-Web_Scraping-green?style=for-the-badge&logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   [![python-whois](https://img.shields.io/badge/python--whois-WHOIS_Lookup-informational?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/python-whois/)
-   [![httpx](https://img.shields.io/badge/httpx-Async_HTTP-purple?style=for-the-badge&logo=python&logoColor=white)](https://www.python-httpx.org/)
-   [![aiohttp](https://img.shields.io/badge/aiohttp-Async_Client-brightgreen?style=for-the-badge&logo=python&logoColor=white)](https://aiohttp.readthedocs.io/en/stable/)
-   [![asyncio](https://img.shields.io/badge/asyncio-Concurrency-blue?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/asyncio.html)

**CLI & Utility:**
-   [![Rich](https://img.shields.io/badge/Rich-Terminal_UI-8B008B?style=for-the-badge&logo=python&logoColor=white)](https://rich.readthedocs.io/en/latest/)
-   [![Colorama](https://img.shields.io/badge/Colorama-Terminal_Colors-orange?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/colorama/)
-   [![tqdm](https://img.shields.io/badge/tqdm-Progress_Bars-5F9EA0?style=for-the-badge&logo=python&logoColor=white)](https://github.com/tqdm/tqdm)
-   [![PyYAML](https://img.shields.io/badge/PyYAML-YAML_Parser-C6A664?style=for-the-badge&logo=yaml&logoColor=white)](https://pyyaml.org/)
-   `argparse` (Standard Python library for command-line parsing)

## 🚀 Quick Start

### Prerequisites
-   **Python 3.8+**: Ensure you have a compatible Python version installed.
    ```bash
    python --version
    ```
-   **pip**: Python's package installer, usually bundled with Python.

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/the-cybercaptain/dns-harvest.git
    cd dns-harvest
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

The `main.py` script serves as the primary entry point for all operations.

#### Basic Usage

To see all available commands and global options:
```bash
python main.py --help
```

To get help for a specific command (e.g., `subdomain`):
```bash
python main.py subdomain --help
```

#### Available Commands

| Command | Description | Options (common) |

| :------ | :---------- | :--------------- |

| `subdomain` | Discover subdomains for a target domain. | `--domain <DOMAIN>`, `--wordlist <FILE>`, `--recursive`, `--engine <ENGINE>`, `--output <FILE>`, `--format <FORMAT>` |

| `email` | Harvest email addresses from a target domain. | `--domain <DOMAIN>`, `--output <FILE>`, `--format <FORMAT>` |

| `dns-audit` | Perform advanced DNS record auditing. | `--domain <DOMAIN>`, `--check-spoofing`, `--check-wildcard`, `--dns-server <IP>`, `--output <FILE>`, `--format <FORMAT>` |

| `full-harvest` | Run a comprehensive harvest including subdomain and email discovery. | `--domain <DOMAIN>`, `--wordlist <FILE>`, `--recursive`, `--output <FILE>`, `--format <FORMAT>` |

| `os-detect` | Attempt to detect the operating system of discovered hosts. | `--domain <DOMAIN>`, `--output <FILE>`, `--format <FORMAT>` |

#### Global Options

| Option        | Description                                       |

| :------------ | :------------------------------------------------ |

| `--verbose`, `-v` | Increase output verbosity.                          |

| `--quiet`, `-q`   | Suppress most output, only show results.            |

| `--threads <N>`   | Number of concurrent threads/tasks (for applicable operations). |

| `--timeout <SEC>` | Set timeout for network requests in seconds.        |

| `--proxy <URL>`   | Use a proxy for HTTP requests (e.g., `http://127.0.0.1:8080`). |

| `--output <FILE>` | Specify an output file for results.                 |

| `--format <FORMAT>`| Specify output format (e.g., `json`, `csv`, `txt`).|

| `--config <FILE>` | Use a custom configuration file.                   |

#### Examples

```bash

# Discover subdomains for example.com using default methods
python main.py subdomain --domain example.com

# Discover subdomains recursively with a custom wordlist and save to JSON
python main.py subdomain --domain example.com --wordlist custom_words.txt --recursive --output subdomains.json --format json

# Harvest email addresses from example.com
python main.py email --domain example.com

# Perform a full harvest and save results to a CSV file
python main.py full-harvest --domain example.com --output full_results.csv --format csv

# Audit DNS records for spoofing and wildcard detection on example.com
python main.py dns-audit --domain example.com --check-spoofing --check-wildcard

# Run OS detection on hosts found for example.com
python main.py os-detect --domain example.com --output os_results.txt
```

## 📁 Project Structure

```
dns-harvest/
├── advanced_features.py   # Advanced DNS auditing functions (spoofing, wildcard, etc.)
├── config.py              # Configuration settings and default values
├── dns_core.py            # Core DNS querying and resolution logic
├── email_harvest.py       # Functions for extracting email addresses
├── full_harvest.py        # Orchestrates a comprehensive DNS and OSINT harvest
├── harvest_core.py        # Generic harvesting utilities and helpers
├── main.py                # Main entry point and command-line interface parser
├── os_detection.py        # Logic for identifying operating systems of hosts
├── output_handlers.py     # Handles formatting and exporting results to various formats
├── subdomain_discovery.py # Modules for discovering subdomains using various techniques
├── requirements.txt       # List of Python dependencies
├── LICENSE                # Project license file
└── README.md
```

## ⚙️ Configuration

The `config.py` file defines default settings for various aspects of the tool, such as API keys, timeout values, and wordlist paths. You can customize these defaults directly in `config.py` or override specific settings via command-line arguments.

For example, `config.py` might define:
```python

# config.py (example snippets)
DEFAULT_WORDLIST = "wordlists/default.txt"
TIMEOUT_SECONDS = 10
DNS_RESOLVERS = ["1.1.1.1", "8.8.8.8"]

# ...
```

You can often specify a custom configuration file using the `--config` global option, though specific implementation might vary.

## 🔧 Development

### Development Setup
1.  Follow the [Installation](#installation) steps.
2.  Make sure you have a code editor (like VS Code) with Python support.

### Running Tests (TODO: If testing framework detected)
*(No explicit testing framework or test directory was detected from the provided structure. This section is a placeholder for future additions.)*

## 🤝 Contributing

We welcome contributions! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a Pull Request.

Please ensure your code adheres to Python's PEP 8 style guidelines.

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

-   Thanks to the developers of all the incredible open-source Python libraries used in this project, especially `dnspython`, `requests`, `beautifulsoup4`, `httpx`, `aiohttp`, and `rich`.
-   Inspired by various open-source reconnaissance tools and techniques in the cybersecurity community.

## 📞 Support & Contact

-   🐛 Issues: [GitHub Issues](https://github.com/the-cybercaptain/dns-harvest/issues)
-   Feel free to reach out to the repository owner `the-cybercaptain` for further assistance or questions.

---

<div align="center">

**⭐ Star this repo if you find it helpful for your reconnaissance needs!**

Made with ❤️ by [the-cybercaptain](https://github.com/the-cybercaptain)

</div>
```
