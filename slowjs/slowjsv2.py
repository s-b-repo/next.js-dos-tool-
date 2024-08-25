import requests
import time

# Configuration
target_url = 'https://your-cdn-endpoint.com/your-resource'
num_requests = 1000
headers = {
    'Cache-Control': 'no-cache',  # Ensure cacheable requests
    'Prefetch': 'true'
}

def send_request():
    try:
        response = requests.get(target_url, headers=headers)
        print(f"Request sent, status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    for _ in range(num_requests):
        send_request()
        time.sleep(0.1)  # Adjust the delay if necessary

if __name__ == "__main__":
    main()
