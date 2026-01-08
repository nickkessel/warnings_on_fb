import os
import psutil
from colorama import Fore, Back, Style
def get_current_mem_usage():
    """Get current ram usage for the active process (pid)
        Prints directly from the function
    Returns:
        float: amount of RAM used, in MB
    """    
    process = psutil.Process(os.getpid())
    ram_used = process.memory_info().rss / (1024 * 1024) #outputs in mb
    ram_used = round(ram_used, 2)
    print(Fore.MAGENTA + f'USAGE: CurrentRAM {ram_used}mb' + Fore.RESET)
    return ram_used