import random
import sys
import copy

# ======================================================================
# ======================== MINIMAX & ALPHA-BETA ========================
# ======================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Šeit definējam visas nepieciešamās funkcijas Minimax un Alpha-Beta,
# lai AI varētu izvēlēties labāko gājienu (take vai split).
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------- Minimax Implementation --------- #
def generate_moves_minimax(sequence):
    """
    Funkcija, kas ģenerē visus iespējamos gājienus (take, split2, split4),
    kas pieejami dotajā stāvoklī (sequence).
    """
    moves = []
    for i, val in enumerate(sequence):
        # 'take'
        moves.append(("take", i))
        # ja skaitlis == 2, var 'split2'
        if val == 2:
            moves.append(("split2", i))
        # ja skaitlis == 4, var 'split4'
        elif val == 4:
            moves.append(("split4", i))
    return moves

def apply_move_minimax(sequence, ai_score, player_score, move, is_ai_turn):
    """
    Funkcija, kas pielieto norādīto gājienu (take, split2, split4),
    atjaunina AI un spēlētāja punktus un atgriež jauno stāvokli.
    """
    move_type, index = move
    new_seq = copy.deepcopy(sequence)
    new_ai = ai_score
    new_player = player_score

    val = new_seq[index]
    if move_type == "take":
        del new_seq[index]
        if is_ai_turn:
            new_ai += val
        else:
            new_player += val

    elif move_type == "split2":
        # 2 -> [1, 1], pretiniekam +1
        del new_seq[index]
        new_seq.insert(index, 1)
        new_seq.insert(index + 1, 1)
        if is_ai_turn:
            new_player += 1
        else:
            new_ai += 1

    elif move_type == "split4":
        # 4 -> [2, 2], pretiniekam -1 (ne zem 0)
        del new_seq[index]
        new_seq.insert(index, 2)
        new_seq.insert(index + 1, 2)
        if is_ai_turn:
            new_player = max(0, new_player - 1)
        else:
            new_ai = max(0, new_ai - 1)

    return new_seq, new_ai, new_player

def minimax(sequence, ai_score, player_score, depth, is_ai_turn):
    """
    Minimax algoritms ar noteiktu 'depth'.
    Atgriež (ai_score - player_score) kā stāvokļa novērtējumu.
    """
    # Bāzes gadījums: ja dziļums = 0 vai nav gājienu, atgriež heuristiku
    if depth == 0 or not sequence:
        return ai_score - player_score

    moves = generate_moves_minimax(sequence)

    if is_ai_turn:
        max_eval = float('-inf')
        for move in moves:
            new_seq, new_ai, new_pl = apply_move_minimax(sequence, ai_score, player_score, move, True)
            eval_val = minimax(new_seq, new_ai, new_pl, depth - 1, False)
            max_eval = max(max_eval, eval_val)
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_seq, new_ai, new_pl = apply_move_minimax(sequence, ai_score, player_score, move, False)
            eval_val = minimax(new_seq, new_ai, new_pl, depth - 1, True)
            min_eval = min(min_eval, eval_val)
        return min_eval

def find_best_move_minimax(sequence, ai_score, player_score):
    """
    Funkcija, kas atrod labāko gājienu, izmantojot Minimax.
    Ja sequence garums <= 7, tad dziļums = 4, citādi = 3.
    """
    depth = 4 if len(sequence) <= 7 else 3
    best_value = float('-inf')
    best_move = None

    moves = generate_moves_minimax(sequence)
    if not moves:
        return None

    for move in moves:
        new_seq, new_ai, new_pl = apply_move_minimax(sequence, ai_score, player_score, move, True)
        eval_val = minimax(new_seq, new_ai, new_pl, depth - 1, False)
        if eval_val > best_value:
            best_value = eval_val
            best_move = move

    return best_move

def ai_move_minimax(sequence, ai_score, player_score):
    """
    Funkcija, kas ļauj AI izdarīt gājienu, izmantojot Minimax.
    Atgriež jauno (sequence, ai_score, player_score).
    """
    move = find_best_move_minimax(sequence, ai_score, player_score)
    if move is None:
        return sequence, ai_score, player_score

    new_seq, new_ai, new_pl = apply_move_minimax(sequence, ai_score, player_score, move, True)
    return new_seq, new_ai, new_pl

# --------- Alpha-Beta Implementation --------- #
INF = float('inf')

def generate_moves_ab(sequence):
    """
    Funkcija, kas ģenerē iespējamos gājienus (take, split2, split4)
    Alpha-Beta algoritmam.
    """
    moves = []
    for i, value in enumerate(sequence):
        moves.append(("take", i, value))
        if value == 2:
            moves.append(("split2", i, value))
        elif value == 4:
            moves.append(("split4", i, value))
    return moves

def apply_move_ab(sequence, ai_score, human_score, current_turn_is_ai, move):
    """
    Pielieto gājienu (take, split2, split4) un atgriež jauno stāvokli,
    jaunos punktus un nākamā spēlētāja karodziņu.
    """
    new_sequence = sequence.copy()
    action, index, value = move

    new_ai = ai_score
    new_human = human_score

    if action == "take":
        new_sequence.pop(index)
        if current_turn_is_ai:
            new_ai += value
        else:
            new_human += value

    elif action == "split2":
        new_sequence[index:index+1] = [1, 1]
        if current_turn_is_ai:
            new_human += 1
        else:
            new_ai += 1

    elif action == "split4":
        new_sequence[index:index+1] = [2, 2]
        if current_turn_is_ai:
            new_human = max(0, new_human - 1)
        else:
            new_ai = max(0, new_ai - 1)

    return new_sequence, new_ai, new_human, not current_turn_is_ai

def alphabeta(sequence, ai_score, human_score, depth, alpha, beta, current_turn_is_ai):
    """
    Alpha-Beta algoritms, kas atgriež (ai_score - human_score).
    """
    moves = generate_moves_ab(sequence)
    if depth == 0 or len(moves) == 0:
        return ai_score - human_score

    if current_turn_is_ai:
        value = -INF
        for move in moves:
            new_seq, new_ai, new_human, new_turn = apply_move_ab(sequence, ai_score, human_score, True, move)
            score = alphabeta(new_seq, new_ai, new_human, depth - 1, alpha, beta, new_turn)
            value = max(value, score)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = INF
        for move in moves:
            new_seq, new_ai, new_human, new_turn = apply_move_ab(sequence, ai_score, human_score, False, move)
            score = alphabeta(new_seq, new_ai, new_human, depth - 1, alpha, beta, new_turn)
            value = min(value, score)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def find_best_move_ab(sequence, ai_score, human_score, current_turn_is_ai=True):
    """
    Funkcija, kas atrod labāko gājienu, izmantojot Alpha-Beta.
    """
    depth = 4 if len(sequence) <= 7 else 3
    best_move = None

    if current_turn_is_ai:
        best_value = -INF
        possible_moves = generate_moves_ab(sequence)
        if not possible_moves:
            return None

        for move in possible_moves:
            new_seq, new_ai, new_human, new_turn = apply_move_ab(sequence, ai_score, human_score, True, move)
            score = alphabeta(new_seq, new_ai, new_human, depth - 1, -INF, INF, new_turn)
            if best_move is None or score > best_value:
                best_value = score
                best_move = move
    else:
        best_value = INF
        possible_moves = generate_moves_ab(sequence)
        if not possible_moves:
            return None

        for move in possible_moves:
            new_seq, new_ai, new_human, new_turn = apply_move_ab(sequence, ai_score, human_score, False, move)
            score = alphabeta(new_seq, new_ai, new_human, depth - 1, -INF, INF, new_turn)
            if best_move is None or score < best_value:
                best_value = score
                best_move = move

    return best_move

def ai_move_alphabeta(sequence, ai_score, player_score):
    """
    Funkcija, kas ļauj AI izdarīt gājienu, izmantojot Alpha-Beta.
    Atgriež jauno (sequence, ai_score, player_score).
    """
    move = find_best_move_ab(sequence, ai_score, player_score, current_turn_is_ai=True)
    if move is None:
        return sequence, ai_score, player_score

    new_sequence, new_ai, new_human, _ = apply_move_ab(sequence, ai_score, player_score, True, move)
    return new_sequence, new_ai, new_human

# ======================================================================
# ======================== SPĒLES LOĢIKA (KONSOLE) =====================
# ======================================================================

def generate_sequence(length):
    """
    Funkcija, kas ģenerē nejaušu skaitļu virkni (no [1, 2, 3, 4]) garumā 'length'.
    """
    return [random.choice([1, 2, 3, 4]) for _ in range(length)]

def ai_move(sequence, ai_score, player_score, chosen_algo):
    """
    Funkcija, kas atkarībā no izvēlētā algoritma (Minimax vai Alpha-Beta),
    veic AI gājienu. Ja nav izvēlēts, veic nejaušu gājienu.
    """
    if not sequence:
        return sequence, ai_score, player_score

    if chosen_algo == "Minimax":
        return ai_move_minimax(sequence, ai_score, player_score)
    elif chosen_algo == "Alpha-Beta":
        return ai_move_alphabeta(sequence, ai_score, player_score)
    else:
        chosen_value = random.choice(sequence)
        sequence.remove(chosen_value)
        ai_score += chosen_value
        return sequence, ai_score, player_score

def print_sequence(seq):
    """
    Palīgfunkcija, kas izdrukā pašreizējo virkni konsolē.
    """
    print("Current sequence:", seq)

def print_scores(player_name, player_score, ai_name, ai_score):
    """
    Palīgfunkcija, kas izdrukā punktus abām pusēm (spēlētājam un AI).
    """
    print(f"{player_name} (Your score): {player_score} | {ai_name} (AI score): {ai_score}")

def player_turn(sequence, player_score, ai_score):
    """
    Funkcija, kas nolasa spēlētāja ievadi (take, split2, split4),
    pielieto to un atgriež atjaunoto (sequence, player_score, ai_score).
    """
    if not sequence:
        return sequence, player_score, ai_score

    while True:
        print_sequence(sequence)
        move = input("Your move (e.g., 'take 3', 'split2 2', or 'split4 4'): ").strip().lower()
        parts = move.split()
        if len(parts) != 2:
            print("Invalid input format. Try again.")
            continue

        action, value_str = parts
        if not value_str.isdigit():
            print("The second part must be a number from the sequence. Try again.")
            continue

        value = int(value_str)

        if value not in sequence:
            print("This number is not in the sequence. Try again.")
            continue

        if action == "take":
            # Uzņem skaitli no virknes
            index_in_seq = sequence.index(value)
            sequence.pop(index_in_seq)
            player_score += value
            break

        elif action == "split2":
            # Split2 iespējams tikai uz 2
            if value != 2:
                print("You can only split2 a '2'. Try again.")
                continue
            index_in_seq = sequence.index(value)
            sequence.pop(index_in_seq)
            sequence.insert(index_in_seq, 1)
            sequence.insert(index_in_seq+1, 1)
            # split2 => pretinieks (AI) saņem +1
            ai_score += 1
            break

        elif action == "split4":
            # Split4 iespējams tikai uz 4
            if value != 4:
                print("You can only split4 a '4'. Try again.")
                continue
            index_in_seq = sequence.index(value)
            sequence.pop(index_in_seq)
            sequence.insert(index_in_seq, 2)
            sequence.insert(index_in_seq+1, 2)
            # split4 => pretiniekam -1 (min 0)
            ai_score = max(0, ai_score - 1)
            break

        else:
            print("Unknown command. Valid commands: take, split2, split4.")
            continue

    return sequence, player_score, ai_score

def main():
    print("Welcome to the Number Splitting Game (Console version)!")
    player_name = input("Enter your name (leave empty to use 'Player'): ").strip()
    if not player_name:
        player_name = "Player"

    print("Choose the AI algorithm:")
    print("1) Minimax")
    print("2) Alpha-Beta")
    alg_choice = input("Enter 1 or 2 (or press Enter for a random AI move): ").strip()

    chosen_algo = None
    if alg_choice == "1":
        chosen_algo = "Minimax"
    elif alg_choice == "2":
        chosen_algo = "Alpha-Beta"

    while True:
        length_str = input("Enter sequence length (15 to 20). Press Enter for 15: ").strip()
        if not length_str:
            chosen_length = 15
            break
        if length_str.isdigit():
            val = int(length_str)
            if 15 <= val <= 20:
                chosen_length = val
                break
        print("Please enter a valid number in the range [15..20].")

    first = input("Who goes first? (player / computer). Press Enter for 'player': ").strip().lower()
    if first not in ["player", "computer"]:
        first_mover = "player"
    else:
        first_mover = first

    ai_name = "Computer"
    current_level = 1
    best_level = 0

    while True:
        print(f"\n=== Starting game at level {current_level} ===")
        sequence = generate_sequence(chosen_length)
        player_score = 0
        ai_score = 0
        player_turn_flag = (first_mover == "player")

        while sequence:
            print_scores(player_name, player_score, ai_name, ai_score)
            if player_turn_flag:
                print(f"\n{player_name}'s turn:")
                sequence, player_score, ai_score = player_turn(sequence, player_score, ai_score)
            else:
                print(f"\n{ai_name}'s turn...")
                sequence, ai_score, player_score = ai_move(sequence, ai_score, player_score, chosen_algo)
            player_turn_flag = not player_turn_flag

        # Kad virkne ir tukša, nosakām uzvarētāju (vai neizšķirtu)
        print("\nThe sequence is empty!")
        print_scores(player_name, player_score, ai_name, ai_score)

        if player_score > ai_score:
            print(f"\nCongratulations, {player_name} has won this round!")
            if current_level > best_level:
                best_level = current_level
            print(f"Your best level so far: {best_level}")
            ans = input("Do you want to continue to the next level? (y/n): ").strip().lower()
            if ans == "y":
                current_level += 1
                continue
            else:
                print("Thank you for playing!")
                break
        elif ai_score > player_score:
            print(f"\n{ai_name} has won! You lost at level {current_level}.")
            ans = input("Do you want to restart at level 1? (y/n): ").strip().lower()
            if ans == "y":
                current_level = 1
                continue
            else:
                print("Thank you for playing!")
                break
        else:
            print("\nIt's a draw!")
            ans = input("Do you want to continue to the next level? (y/n): ").strip().lower()
            if ans == "y":
                current_level += 1
                continue
            else:
                print("Thank you for playing!")
                break

if __name__ == "__main__":
    main()
