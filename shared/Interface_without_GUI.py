import random

def generate_sequence(length):
    return [random.choice([1, 2, 3, 4]) for _ in range(length)]

def ai_move(seq, ai_score):
    if not seq:
        return seq, ai_score
    chosen_val = random.choice(seq)
    seq.remove(chosen_val)
    ai_score += chosen_val
    return seq, ai_score

def main():
    player_name = input("Enter your name: ")
    if not player_name.strip():
        player_name = "Player"
    print("Choose an algorithm: 1) Minimax or 2) Alpha-Beta")
    algo = input("Enter 1 or 2: ")
    length = 15
    first_mover = "player"
    current_level = 1
    best_level = 0
    while True:
        sequence = generate_sequence(length)
        player_score = 0
        ai_score = 0
        player_turn = (first_mover == "player")
        while sequence:
            if player_turn:
                print(f"\nCurrent sequence: {sequence}")
                print(f"{player_name} = {player_score} | Computer = {ai_score}")
                move = input("Enter a number from the list or 'shift2'/'shift4': ")
                if move.lower().startswith("shift"):
                    val = int(move[5:])
                    if val in sequence:
                        if val == 2:
                            idx = sequence.index(val)
                            sequence.pop(idx)
                            sequence.insert(idx, 1)
                            sequence.insert(idx+1, 1)
                            ai_score += 1
                        elif val == 4:
                            idx = sequence.index(val)
                            sequence.pop(idx)
                            sequence.insert(idx, 2)
                            sequence.insert(idx+1, 2)
                            ai_score = max(0, ai_score - 1)
                else:
                    val = int(move)
                    if val in sequence:
                        sequence.remove(val)
                        player_score += val
                player_turn = False
            else:
                sequence, ai_score = ai_move(sequence, ai_score)
                player_turn = True
        print(f"\nFinal scores: {player_name} = {player_score}, Computer = {ai_score}")
        if player_score > ai_score:
            print("You win!")
            if current_level > best_level:
                best_level = current_level
            print(f"Best level reached: {best_level}")
            current_level += 1
            c = input("Proceed to next level? (y/n): ")
            if c.lower() != 'y':
                break
        else:
            print("You lost or it's a draw.")
            current_level = 1
            c = input("Play again? (y/n): ")
            if c.lower() != 'y':
                break

if __name__ == "__main__":
    main()
