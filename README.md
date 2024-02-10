# TCP-WS 🌐

🌟 TCP-WS is a WebSocket TCP Redirector, implemented as an 🌀 asynchronous Python backend.  
It relays incoming TCP data to all connected WebSocket clients.


## Features 🔥

- Real-time redirection of TCP data to WebSocket clients.
- Implemented as an 🌀 asynchronous Python backend.
- Dockerized setup for simplified deployment.
- Utilizes s6 process supervision for reliable service management.

## How It Works 🛠️

TCP-WS operates by simultaneously listening for TCP and WebSocket connections. Upon connection from a TCP client and subsequent data transmission, the server forwards this data to all WebSocket clients currently connected, ensuring seamless communication between the two protocols.  

By defaults the TCP port is `8080` and the Websocket port is `8765` .


## Installation and Usage 📦

To run TCP-WS, Docker and Docker Compose are recommended:

1. Clone this repository: `git clone https://github.com/simone-desantis/tcp-ws.git`
2. Navigate to the project directory: `cd tcp-ws`
3. If needed, modify the `docker-compose.yml` file to suit your requirements.
4. Execute `docker-compose up -d` to initiate the service.

## Contributing 🤝

Contributions to TCP-WS are encouraged! Whether you encounter issues or have suggestions for enhancements, feel free to open an issue or submit a pull request.

## License 📝

Refer to the [LICENSE](LICENSE) file for more information.

