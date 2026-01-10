import os
import psutil
from colorama import Fore, Back, Style
import gc
from pympler import muppy, summary
def get_current_mem_usage():
    """Get current ram usage for the active process (pid)
        Prints directly from the function
    Returns:
        float: amount of RAM used, in MB
    """    
    process = psutil.Process(os.getpid())
    ram_used = process.memory_info().rss / (1024 * 1024) #outputs in mb
    ram_used = round(ram_used, 2)
    #print(Fore.MAGENTA + f'USAGE: CurrentRAM {ram_used}mb' + Fore.RESET)
    return ram_used

def log_memory_breakdown():
    """
    Prints a summary of the largest object types in memory.
    Useful for finding leaks (e.g., if 'Figure' or 'Polygon' counts keep growing).
    """
    current_usage = get_current_mem_usage()
    print(Back.MAGENTA + Fore.WHITE + f"\n--- MEMORY OBJECT ANALYSIS (current: {current_usage}mb) ---" + Fore.RESET + Back.RESET)
    
    # Force garbage collection first to ensure we aren't counting temporary junk
    gc.collect()
    
    # Get all objects currently in RAM
    all_objects = muppy.get_objects()
    
    # Summarize and sort by size
    sum1 = summary.summarize(all_objects)
    
    # Print the top 20 object types consuming memory
    summary.print_(sum1, limit=20)
    
    print("--------------------------------------------------\n")

log_memory_breakdown()