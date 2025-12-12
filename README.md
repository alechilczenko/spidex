 # Kimi: Attack Surface Discovery Engine


#### Developed with 💜 by [@alechilczenko](https://github.com/alechilczenko)


> **Project Context:** This project serves as a portfolio piece demonstrating concepts in offensive security, concurrency, and distributed architecture.

## 1. Introducing Kimi: The Origin Story

### What was Kimi ?

During my early days venturing into the world of offensive security, I was always fascinated by how major search engines like **Shodan** indexed information from millions of devices. This concept kept spinning in my head; I needed to understand the engineering behind it by simulating it myself.

**Kimi** is the result of that curiosity. It is a continuous reconnaissance scanner designed to prioritize the analysis of external attack surface exposure. It performs large-scale, port-oriented scanning to collect information from services connected to the Internet.

My goal was to create an efficient architecture: the implementation of **threads and queues** was designed to maximize performance per scan cycle, significantly reducing execution time for massive IP ranges.

---

## 2. Key Aspects

Kimi serves as a proof of concept in critical areas:

- **Concurrency:** Usage of **Threads and Queues** in Python to orchestrate up to ≈500 simultaneous network I/O operations.
    
- **Decoupled Architecture:** Design of a distributed system (Engine → API → DB), separating the execution of the scan from data persistence.
    
- **Networking:** Low-level socket programming for **TCP/UDP handshakes** and precise timeout management.
    
- **NoSQL Databases:** Implementation of **MongoDB** to store scan results, which are inherently variable and unstructured.
    

---

## 3. The Learning Curve

Revisiting Kimi today allows me to apply a modern engineering and ethical perspective to my initial work:

- **Technical Evolution:** The biggest challenge was mastering `threading` in Python. Today, I recognize that the most scalable solution would be migrating the **Engine to asynchronous programming (`asyncio`)** to avoid GIL overhead and scale concurrency even further.
    
- **Ethical Maturity:** The most important lesson has been **professional responsibility**. The project evolved from a curiosity-driven experiment to a demonstration tool. **Kimi** is strictly limited to ethical testing on controlled networks, highlighting my commitment to legal and responsible security practices.

## 4. Architecture & Workflow

The system is divided into the **Engine (Scanner)** and the **API (Persistence)**.

### Data Architecture

**MongoDB** acts as the primary ingestion store. The architecture is designed to be compatible with **Elasticsearch / Kibana (ELK)** integration, enabling full-text search capabilities and analytical visualizations of the collected data.

### Concurrency Examples (CLI)

|**Scenario**|**Command Example**|**Description**|
|---|---|---|
|**Rapid Scan**|`python3 engine.py -r 192.168.0.0,192.168.0.255 -t 150 --top-ports`|Scans a range using 150 threads.|
|**Custom CIDR**|`python3 engine.py -r 192.168.0.0/24 -t 350 -C 80 443 21`|Scans specific ports using 350 threads.|
## 5. Contact & Legal

- **Deployment:** The project is fully containerized with Docker.
    
- **License:** [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).
    
- **Contact:** alechilczenko@gmail.com
    
- **Legal Disclaimer:** **Kimi** is presented solely for educational purposes and technical demonstration. Usage outside of controlled environments is the sole responsibility of the user.
