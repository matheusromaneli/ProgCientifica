def generate(square_len, n):
    """ 
    Generate stradil references (only for square models)
    
    """
    conn = []
    for i in range(1, n+1):
        left = i-1 if i%square_len != 1 else 0
        right= i+1 if i%square_len != 0 else 0
        down = i-square_len if i > square_len else 0
        up   = i+square_len if i <= n-square_len else 0
        aux = [left, right, down, up, i]
        conn.append(aux)
    return conn