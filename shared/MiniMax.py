import copy

def generate_moves(sequence):
    moves = []
    for i, val in enumerate(sequence):
        # Ņemt skaitli
        moves.append(("take", i))
        # Dalīt 2
        if val == 2:
            moves.append(("split2", i))
        # Dalīt 4
        elif val == 4:
            moves.append(("split4", i))
    return moves

def apply_move(sequence, ai_score, player_score, move, is_ai_turn):
    move_type, index = move
    seq = copy.deepcopy(sequence)
    ai = ai_score
    player = player_score

    val = seq[index]
    if move_type == "take":
        del seq[index]
        if is_ai_turn:
            ai += val
        else:
            player += val

    elif move_type == "split2":
        del seq[index]
        seq.insert(index, 1)
        seq.insert(index + 1, 1)
        if is_ai_turn:
            player += 1
        else:
            ai += 1

    elif move_type == "split4":
        del seq[index]
        seq.insert(index, 2)
        seq.insert(index + 1, 2)
        if is_ai_turn:
            player = max(0, player - 1)
        else:
            ai = max(0, ai - 1)

    return seq, ai, player

def minimax(sequence, ai_score, player_score, depth, is_ai_turn):
    if depth == 0 or not sequence:
        return ai_score - player_score

    moves = generate_moves(sequence)

    if is_ai_turn:
        max_eval = float('-inf')
        for move in moves:
            new_seq, new_ai, new_player = apply_move(sequence, ai_score, player_score, move, is_ai_turn=True)
            eval = minimax(new_seq, new_ai, new_player, depth - 1, is_ai_turn=False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_seq, new_ai, new_player = apply_move(sequence, ai_score, player_score, move, is_ai_turn=False)
            eval = minimax(new_seq, new_ai, new_player, depth - 1, is_ai_turn=True)
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(sequence, ai_score, player_score):
    depth = 4 if len(sequence) <= 7 else 3
    best_value = float('-inf')
    best_move = None

    for move in generate_moves(sequence):
        new_seq, new_ai, new_player = apply_move(sequence, ai_score, player_score, move, is_ai_turn=True)
        eval = minimax(new_seq, new_ai, new_player, depth - 1, is_ai_turn=False)
        if eval > best_value:
            best_value = eval
            best_move = move

    return best_move

def ai_move(sequence, ai_score):
    move = find_best_move(sequence, ai_score, 0)
    if move is None:
        return sequence, ai_score

    move_type, index = move
    val = sequence[index]

    if move_type == "take":
        sequence.pop(index)
        ai_score += val
    elif move_type == "split2":
        sequence.pop(index)
        sequence.insert(index, 1)
        sequence.insert(index + 1, 1)
        # cilvēkam +1, ja integrējam — nodod spēles funkcijai
    elif move_type == "split4":
        sequence.pop(index)
        sequence.insert(index, 2)
        sequence.insert(index + 1, 2)
        # cilvēkam -1, ja integrējam — nodod spēles funkcijai

    return sequence, ai_score
