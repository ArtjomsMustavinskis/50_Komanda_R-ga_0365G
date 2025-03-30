INF = float('inf')  # Define a representation of infinity for alpha/beta initial values

def generate_moves(sequence):
    """Generate all possible moves (take or split) from the current sequence."""
    moves = []
    for i, value in enumerate(sequence):
        # Taking the number at index i is always a possible move
        moves.append(("take", i, value))
        # If the value is 2 or 4, the respective split moves are possible
        if value == 2:
            moves.append(("split2", i, value))
        elif value == 4:
            moves.append(("split4", i, value))
    return moves

def apply_move(sequence, ai_score, human_score, current_turn_is_ai, move):
    """Apply the given move to the state (sequence and scores), returning the new state."""
    # Copy the sequence to avoid mutating the original state
    new_sequence = sequence.copy()
    action, index, value = move

    if action == "take":
        # Remove the number from sequence and add its value to the current player's score
        new_sequence.pop(index)
        if current_turn_is_ai:
            ai_score += value
        else:
            human_score += value

    elif action == "split2":
        # Remove the '2' and replace it with two '1's in the sequence
        new_sequence[index:index+1] = [1, 1]
        # Give +1 point to the opponent
        if current_turn_is_ai:
            human_score += 1   # AI split 2, so human gains 1 point
        else:
            ai_score += 1      # Human split 2, so AI gains 1 point

    elif action == "split4":
        # Remove the '4' and replace it with two '2's in the sequence
        new_sequence[index:index+1] = [2, 2]
        # Subtract 1 point from the opponent (not going below 0)
        if current_turn_is_ai:
            # AI split 4, subtract 1 from human's score
            human_score = max(0, human_score - 1)
        else:
            # Human split 4, subtract 1 from AI's score
            ai_score = max(0, ai_score - 1)

    # Switch turn for the next state
    new_turn_is_ai = not current_turn_is_ai
    return new_sequence, ai_score, human_score, new_turn_is_ai

def alphabeta(sequence, ai_score, human_score, depth, alpha, beta, current_turn_is_ai):
    """
    Perform alpha-beta search and return the heuristic value of the state.
    """
    # Terminal condition: depth limit reached or no moves available (game over)
    moves = generate_moves(sequence)
    if depth == 0 or len(moves) == 0:
        # Evaluate state: return score difference (AI - Human)
        return ai_score - human_score

    if current_turn_is_ai:
        # Maximizing player's turn (AI)
        value = -INF
        for move in moves:
            # Simulate this move
            new_seq, new_ai, new_human, new_turn = apply_move(sequence, ai_score, human_score, True, move)
            # Recurse with decreased depth
            score = alphabeta(new_seq, new_ai, new_human, depth-1, alpha, beta, new_turn)
            # Update the best value
            value = max(value, score)
            alpha = max(alpha, value)
            if alpha >= beta:
                # Beta cut-off: prune remaining moves
                break
        return value
    else:
        # Minimizing player's turn (Human)
        value = INF
        for move in moves:
            new_seq, new_ai, new_human, new_turn = apply_move(sequence, ai_score, human_score, False, move)
            score = alphabeta(new_seq, new_ai, new_human, depth-1, alpha, beta, new_turn)
            value = min(value, score)
            beta = min(beta, value)
            if beta <= alpha:
                # Alpha cut-off
                break
        return value

def find_best_move(sequence, ai_score, human_score, current_turn_is_ai=True):
    """
    Determine the best move for the current player (usually AI) using alpha-beta search.
    Returns the move tuple (action, index, value) that leads to the optimal outcome.
    """
    # Decide search depth based on sequence length for performance
    if len(sequence) <= 7:
        depth = 4
    else:
        depth = 3

    best_move = None
    if current_turn_is_ai:
        # AI (maximizing) is choosing a move
        best_value = -INF
        for move in generate_moves(sequence):
            new_seq, new_ai, new_human, new_turn = apply_move(sequence, ai_score, human_score, True, move)
            # Evaluate this move using alpha-beta
            score = alphabeta(new_seq, new_ai, new_human, depth-1, -INF, INF, new_turn)
            if best_move is None or score > best_value:
                best_value = score
                best_move = move
    else:
        # Human (minimizing) is choosing a move – typically not used in main, but included for completeness
        best_value = INF
        for move in generate_moves(sequence):
            new_seq, new_ai, new_human, new_turn = apply_move(sequence, ai_score, human_score, False, move)
            score = alphabeta(new_seq, new_ai, new_human, depth-1, -INF, INF, new_turn)
            if best_move is None or score < best_value:
                best_value = score
                best_move = move

    return best_move

def ai_move(sequence, ai_score, human_score):
    """
    Choose and perform the best move for the AI using Alpha-Beta pruning.
    Returns a tuple (move, new_sequence, new_ai_score, new_human_score).
    """
    # Find the best move for AI (maximizing player) from the current state
    move = find_best_move(sequence, ai_score, human_score, current_turn_is_ai=True)
    if move is None:
        # No moves available (game over)
        return None
    # Apply the chosen move to get the updated state
    new_sequence, new_ai_score, new_human_score, _ = apply_move(sequence, ai_score, human_score, True, move)
    return move, new_sequence, new_ai_score, new_human_score

