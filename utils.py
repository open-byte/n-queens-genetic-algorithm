from colorama import Fore, Back, Style
brand = """
  ____                     ____        _
 / __ \                   |  _ \      | |
| |  | |_ __   ___ _ __   | |_) |_   _| |_ ___
| |  | | '_ \ / _ \ '_ \  |  _ <| | | | __/ _ \\
| |__| | |_) |  __/ | | | | |_) | |_| | ||  __/
 \____/| .__/ \___|_| |_| |____/ \__, |\__\___|
       | |                        __/ |
       |_|                       |___/
     _                _                                  _   
  __| | _____   _____| | ___  _ __  _ __ ___   ___ _ __ | |_ 
 / _` |/ _ \ \ / / _ \ |/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __|
| (_| |  __/\ V /  __/ | (_) | |_) | | | | | |  __/ | | | |_ 
 \__,_|\___| \_/ \___|_|\___/| .__/|_| |_| |_|\___|_| |_|\__|
                             |_|                             
"""

def formatter_side_by_side(s1, s2) -> str:
    """
    Print two strings side by side
    """
    s1 = s1.split('\n')[1:-1]
    s2 = s2.split('\n')
    
    if len(s1) > len(s2):
        s2.extend([' '] * (len(s1) - len(s2)))
        
    else:
        s1.extend([' '] * (len(s2) - len(s1)))
    
    text = ''
    for s1_line, s2_line in zip(s1, s2):
        text += f'{s1_line:<65}{s2_line}\n'

    text = f"{(100 * '-')}\n\n{text}{(100 * '-')}\n"
    
    return text
    

