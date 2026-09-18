def shift_reduce_parser(input_str):
    stack = []
    # Convert input string into a list of characters
    ip = list(input_str)
    ip.append('$') # Add end marker
    pointer = 0
    
    print("\n\tShift Reduce Parser")
    print("\nGrammar:")
    print("E → E + E\nE → E * E\nE → E / E\nE → a | b")
    print("\nStack\t\tInput\t\tAction")
    
    # Helper function to print the current state of the parser
    def print_state(action):
        # Cleans up spaces in stack printing for neat formatting
        stack_str = ''.join(stack).replace(" ", "")
        input_str_rem = ''.join(ip[pointer:])
        print(f"{stack_str:<16}{input_str_rem:<16}{action}")

    def reduce_stack():
        nonlocal stack
        s = ''.join(stack).replace(" ", "") # Remove spaces for checking
        
        # Check for multi-character rules (E+E, E*E, E/E)
        if s.endswith("E+E") or s.endswith("E*E") or s.endswith("E/E"):
            rule = s[-3:]
            # Rebuild stack by removing the last 3 items and adding 'E'
            stack = list(s[:-3]) + ['E']
            print_state(f"Reduce by E → {rule[0]} {rule[1]} {rule[2]}")
            return True
        # Check for single-character rules (a, b)
        elif stack and stack[-1] in ['a', 'b']:
            char = stack[-1]
            stack[-1] = 'E'
            print_state(f"Reduce by E → {char}")
            return True
        return False

    print_state("--")
    
    # Main loop to Shift items onto the stack
    while pointer < len(ip) - 1:
        stack.append(ip[pointer])
        pointer += 1
        print_state(f"Shift '{stack[-1]}'")
        
        # Keep reducing as long as a rule matches
        while reduce_stack():
            pass

    # Check if we successfully parsed the whole string
    # We clean the stack list to ensure no hidden spaces block the match
    cleaned_stack = [item.strip() for item in stack if item.strip()]
    if cleaned_stack == ['E'] and ip[pointer] == '$':
        print_state("Accept")
    else:
        print_state("Reject")

# Get user input and run the parser
input_expr = input("Enter the input expression (only a, b, +, *, /): ").strip()
shift_reduce_parser(input_expr)
