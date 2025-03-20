
@classmethod
def from_string(cls, s):
    """
    Parses a PBT from a string of balanced square brackets.
    For example, "[10[5][3]]" creates a node with value 10, 
    left child 5, and right child 3.
    :param s: The string representation of the PBT.
    :return: A PBT object.
    """
    if not s or s == "[]":
        return PBT()

    # Extract the value (before any brackets)
    value = ""
    i = 0
    while i < len(s) and s[i] not in "[]":
        value += s[i]
        i += 1

    # Create root node
    node = cls(int(value) if value.strip() else None)
    
    # If we have children to process
    if i < len(s) and s[i] == "[":
        # Find matched brackets for left child
        balance = 1
        j = i + 1
        while j < len(s) and balance > 0:
            if s[j] == "[":
                balance += 1
            elif s[j] == "]":
                balance -= 1
            j += 1
            
        # Parse left child and insert
        left_child = cls.from_string(s[i+1:j-1])
        if left_child is not None:
            node.left = left_child
            
        # Check for right child
        if j < len(s) and s[j] == "[":
            balance = 1
            k = j + 1
            while k < len(s) and balance > 0:
                if s[k] == "[":
                    balance += 1
                elif s[k] == "]":
                    balance -= 1
                k += 1
                
            # Parse right child and insert
            right_child = cls.from_string(s[j+1:k-1])
            if right_child is not None:
                node.right = right_child
                
    return node
