import pygame
import random
import sys

# ======================================================================
# ======================== MINIMAX & ALPHA-BETA ========================
# ======================================================================
# --------- Minimax Implementation --------- #
import copy

def generate_moves_minimax(sequence):
    """
    Funkcija, kas ģenerē visus iespējamos gājienus (take vai split),
    ko spēlētājs var veikt dotajā stāvoklī (sequence).
    """
    moves = []
    for i, val in enumerate(sequence):
        # 'take' skaitli
        moves.append(("take", i))
        # ja skaitlis == 2, var dalīt 2
        if val == 2:
            moves.append(("split2", i))
        # ja skaitlis == 4, var dalīt 4
        elif val == 4:
            moves.append(("split4", i))
    return moves

def apply_move_minimax(sequence, ai_score, player_score, move, is_ai_turn):
    """
    Funkcija, kas pielieto izvēlēto gājienu 'move' (take vai split)
    un atgriež jauno sequence, ai_score, player_score.
    """
    move_type, index = move
    seq = copy.deepcopy(sequence)
    new_ai = ai_score
    new_player = player_score

    val = seq[index]
    if move_type == "take":
        del seq[index]
        if is_ai_turn:
            new_ai += val
        else:
            new_player += val

    elif move_type == "split2":
        # 2 -> [1,1], pretiniekam +1
        del seq[index]
        seq.insert(index, 1)
        seq.insert(index + 1, 1)
        if is_ai_turn:
            new_player += 1
        else:
            new_ai += 1

    elif move_type == "split4":
        # 4 -> [2,2], pretiniekam -1 (nezem nulles)
        del seq[index]
        seq.insert(index, 2)
        seq.insert(index + 1, 2)
        if is_ai_turn:
            new_player = max(0, new_player - 1)
        else:
            new_ai = max(0, new_ai - 1)

    return seq, new_ai, new_player

def minimax(sequence, ai_score, player_score, depth, is_ai_turn):
    """
    Minimax algoritms ar fiksētu 'depth'.
    Atgriež stāvokļa vērtību: (AI_score - player_score).
    """
    # Ja nav gājienu vai dziļums sasniegts, tad atgriež heuristiku (AI - Player)
    if depth == 0 or not sequence:
        return ai_score - player_score

    moves = generate_moves_minimax(sequence)

    if is_ai_turn:
        max_eval = float('-inf')
        for move in moves:
            new_seq, new_ai, new_player = apply_move_minimax(sequence, ai_score, player_score, move, True)
            eval_val = minimax(new_seq, new_ai, new_player, depth - 1, False)
            max_eval = max(max_eval, eval_val)
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_seq, new_ai, new_player = apply_move_minimax(sequence, ai_score, player_score, move, False)
            eval_val = minimax(new_seq, new_ai, new_player, depth - 1, True)
            min_eval = min(min_eval, eval_val)
        return min_eval

def find_best_move_minimax(sequence, ai_score, player_score):
    """
    Atrod labāko gājienu, izmantojot Minimax.
    """
    # Ja secības garums <= 7, padziļinātais dziļums 4, citādi 3
    depth = 4 if len(sequence) <= 7 else 3
    best_value = float('-inf')
    best_move = None

    moves = generate_moves_minimax(sequence)
    if not moves:
        return None

    for move in moves:
        new_seq, new_ai, new_player = apply_move_minimax(sequence, ai_score, player_score, move, True)
        eval_val = minimax(new_seq, new_ai, new_player, depth - 1, False)
        if eval_val > best_value:
            best_value = eval_val
            best_move = move

    return best_move

def ai_move_minimax(sequence, ai_score, player_score):
    """
    Veic AI gājienu, izmantojot Minimax.
    Atgriež (new_sequence, new_ai_score, new_player_score).
    """
    move = find_best_move_minimax(sequence, ai_score, player_score)
    if move is None:
        # nav gājienu
        return sequence, ai_score, player_score

    new_seq, new_ai, new_player = apply_move_minimax(sequence, ai_score, player_score, move, True)
    return new_seq, new_ai, new_player


# --------- Alpha-Beta Implementation --------- #
INF = float('inf')

def generate_moves_ab(sequence):
    """
    Līdzīgi kā generate_moves_minimax, bet atsevišķi
    priekš Alpha-Beta (lai neizraisītu kolīzijas).
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
    Pielieto norādīto gājienu (take, split2, split4) un atgriež jauno stāvokli.
    """
    new_sequence = sequence.copy()
    action, index, value = move

    # Lokālās kopijas
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
    Alpha-Beta algoritms, kas atgriež heuristiku (ai_score - human_score).
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
    Izmantojot Alpha-Beta, atrod labāko gājienu dotajā stāvoklī.
    """
    if len(sequence) <= 7:
        depth = 4
    else:
        depth = 3

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
        # (Nav obligāti vajadzīgs šai spēlei, jo AI mēs saucam ar current_turn_is_ai=True)
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
    Veic AI gājienu, izmantojot Alpha-Beta.
    Atgriež (new_sequence, new_ai_score, new_player_score).
    """
    move = find_best_move_ab(sequence, ai_score, player_score, current_turn_is_ai=True)
    if move is None:
        # Nav gājienu
        return sequence, ai_score, player_score

    new_sequence, new_ai, new_human, _ = apply_move_ab(sequence, ai_score, player_score, True, move)
    return new_sequence, new_ai, new_human

# ======================================================================
# ============================ PYGAME INTERFACE =========================
# ======================================================================

pygame.init()

# --- Window config ---
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Splitting Game (Pygame)")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (200, 200, 200)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE  = (0, 100, 255)

# --- Fonts ---
FONT_BIG = pygame.font.SysFont("Arial", 40, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 30)
FONT_SML = pygame.font.SysFont("Arial", 24)

# --- Game states ---
STATE_MAIN_MENU       = 0
STATE_ENTER_NAME      = 1
STATE_CHOOSE_SETTINGS = 2
STATE_GAME            = 3
STATE_GAME_OVER_WIN   = 4
STATE_GAME_OVER_LOSE  = 5
STATE_RULES           = 6
STATE_GAME_OVER_DRAW  = 7   # JAUNS stāvoklis priekš neizšķirta

# --- Simple Button class ---
class Button:
    def __init__(self, x, y, w, h, text, callback,
                 font=FONT_MED, color=GRAY, text_color=BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = font
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

# --- Generate random sequence ---
def generate_sequence(length):
    """
    Funkcija, kas ģenerē nejaušu virkni garumā 'length' ar vērtībām [1, 2, 3, 4].
    """
    return [random.choice([1, 2, 3, 4]) for _ in range(length)]

# --- AI move dispatcher ---
def ai_move(sequence, ai_score, player_score, chosen_algo):
    """
    Funkcija, kas izsauc atbilstošo AI algoritmu (Minimax vai Alpha-Beta),
    un veic atgriešanu: (sequence, ai_score, player_score).
    Ja algoritms nav izvēlēts, AI veic nejaušu gājienu.
    """
    if not sequence:
        return sequence, ai_score, player_score

    if chosen_algo == "Minimax":
        # Izmantojam Minimax
        new_seq, new_ai, new_pl = ai_move_minimax(sequence, ai_score, player_score)
        return new_seq, new_ai, new_pl

    elif chosen_algo == "Alpha-Beta":
        # Izmantojam Alpha-Beta
        new_seq, new_ai, new_pl = ai_move_alphabeta(sequence, ai_score, player_score)
        return new_seq, new_ai, new_pl

    else:
        # Ja nav izvēlēts algoritms -> nejaušs gājiens (fallback)
        chosen_value = random.choice(sequence)
        sequence.remove(chosen_value)
        ai_score += chosen_value
        return sequence, ai_score, player_score

# --- Screens drawing ---
def draw_main_menu():
    SCREEN.fill(WHITE)
    title_surf = FONT_BIG.render("Main Menu", True, BLACK)
    title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
    SCREEN.blit(title_surf, title_rect)

def draw_best_level(best_level):
    if best_level > 0:
        txt = f"Best level reached: {best_level}"
    else:
        txt = "No best level yet (haven't played/won yet)"
    text_surf = FONT_SML.render(txt, True, BLACK)
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//4 + 50))
    SCREEN.blit(text_surf, text_rect)

def draw_enter_name(player_name):
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render("Enter your name:", True, BLACK)
    txt_rect = txt_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
    SCREEN.blit(txt_surf, txt_rect)

    name_surf = FONT_MED.render(player_name, True, BLACK)
    name_rect = name_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
    pygame.draw.rect(SCREEN, GRAY,
                     (name_rect.x - 10, name_rect.y - 5,
                      name_rect.width + 20, name_rect.height + 10),
                     2)
    SCREEN.blit(name_surf, name_rect)

def draw_choose_settings(player_name, chosen_algo, chosen_length, first_mover, show_error):
    SCREEN.fill(WHITE)
    # Title
    title_surf = FONT_BIG.render("Game Settings", True, BLACK)
    title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
    SCREEN.blit(title_surf, title_rect)

    # Player name
    name_text = f"Player: {player_name}"
    name_surf = FONT_MED.render(name_text, True, BLACK)
    name_rect = name_surf.get_rect(center=(WIDTH//2, 110))
    SCREEN.blit(name_surf, name_rect)

    # Algorithm
    algo_str = chosen_algo if chosen_algo else "Not selected"
    algo_color = RED if (show_error and chosen_algo is None) else BLACK
    algo_text = f"Algorithm: {algo_str}"
    algo_surf = FONT_SML.render(algo_text, True, algo_color)
    algo_rect = algo_surf.get_rect(center=(WIDTH//2, 160))
    SCREEN.blit(algo_surf, algo_rect)

    # Length
    len_text = f"Length: {chosen_length}"
    len_surf = FONT_SML.render(len_text, True, BLACK)
    len_rect = len_surf.get_rect(center=(WIDTH//2, 190))
    SCREEN.blit(len_surf, len_rect)

    # Who goes first
    fm_text = "Player" if first_mover == "player" else "Computer"
    fm_surf_text = f"Goes first: {fm_text}"
    fm_surf = FONT_SML.render(fm_surf_text, True, BLACK)
    fm_rect = fm_surf.get_rect(center=(WIDTH//2, 220))
    SCREEN.blit(fm_surf, fm_rect)

    # Error message if needed
    if show_error and chosen_algo is None:
        error_msg = "Please select an algorithm!"
        err_surf = FONT_SML.render(error_msg, True, RED)
        err_rect = err_surf.get_rect(center=(WIDTH//2, 260))
        SCREEN.blit(err_surf, err_rect)

def draw_rules_screen():
    SCREEN.fill(WHITE)
    title_surf = FONT_BIG.render("Brief Game Description", True, BLACK)
    title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
    SCREEN.blit(title_surf, title_rect)

    # Explanation
    lines = [
        "1. Initially, a sequence of numbers is generated. Each player starts with 0 points.",
        "2. Players move in turns. During a turn, a player can:",
        "   - Take any number from the sequence and add it to their score.",
        "   - Split the number 2 into two 1s and give +1 point to the opponent.",
        "   - Split the number 4 into two 2s and subtract 1 point from the opponent’s score.",
        "3. The game ends when the sequence is empty. The player with the most points wins.",
        "",
        "Click << Start >> to begin the game."
    ]

    y_offset = 120
    for line in lines:
        line_surf = FONT_SML.render(line, True, BLACK)
        SCREEN.blit(line_surf, (50, y_offset))
        y_offset += 30

def draw_game_screen(player_name, player_score, ai_name, ai_score,
                     level, best_level, sequence):
    SCREEN.fill(WHITE)

    # Top-left: player name + score
    left_text = f"{player_name} (Score: {player_score})"
    left_surf = FONT_SML.render(left_text, True, BLACK)
    SCREEN.blit(left_surf, (20, 20))

    # Top-right: AI name + level + score
    right_text = f"{ai_name} Level {level} (Score: {ai_score})"
    right_surf = FONT_SML.render(right_text, True, BLACK)
    SCREEN.blit(right_surf, (WIDTH - right_surf.get_width() - 20, 20))

    # Top-center: best level
    if best_level > 0:
        center_text = f"Best level: {best_level}"
        center_surf = FONT_SML.render(center_text, True, BLACK)
        center_rect = center_surf.get_rect(center=(WIDTH//2, 20))
        SCREEN.blit(center_surf, center_rect)

    # Display the sequence as small "buttons"
    start_x = 50
    start_y = 100
    gap = 10
    btn_w, btn_h = 50, 50

    global number_buttons
    number_buttons = []

    x = start_x
    y = start_y
    for val in sequence:
        rect = pygame.Rect(x, y, btn_w, btn_h)
        pygame.draw.rect(SCREEN, GRAY, rect)
        val_surf = FONT_SML.render(str(val), True, BLACK)
        val_rect = val_surf.get_rect(center=rect.center)
        SCREEN.blit(val_surf, val_rect)

        number_buttons.append((rect, val))

        x += btn_w + gap
        if x + btn_w > WIDTH - 50:
            x = start_x
            y += btn_h + gap

    # Hints about SHIFT
    shift_text1 = "Shift + click 2 => splits into (1 and 1), giving +1 to opponent."
    shift_text2 = "Shift + click 4 => splits into (2 and 2), subtracting 1 from opponent."
    st1_surf = FONT_SML.render(shift_text1, True, BLACK)
    st2_surf = FONT_SML.render(shift_text2, True, BLACK)
    SCREEN.blit(st1_surf, (50, HEIGHT - 60))
    SCREEN.blit(st2_surf, (50, HEIGHT - 30))

def draw_game_over_win(player_name):
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render(f"Congratulations, {player_name}!", True, BLACK)
    txt_rect = txt_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(txt_surf, txt_rect)

    txt_surf2 = FONT_MED.render("You won! What’s next?", True, BLACK)
    txt_rect2 = txt_surf2.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(txt_surf2, txt_rect2)

def draw_game_over_lose(ai_name):
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render("Game Over...", True, BLACK)
    txt_rect = txt_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(txt_surf, txt_rect)

    txt_surf2 = FONT_MED.render(f"Victory goes to {ai_name}.", True, BLACK)
    txt_rect2 = txt_surf2.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(txt_surf2, txt_rect2)

def draw_game_over_draw():
    """
    Zīmējam ekrānu, ja spēle beidzas neizšķirti (player_score == ai_score).
    """
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render("It's a draw!", True, BLACK)
    txt_rect = txt_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(txt_surf, txt_rect)

    txt_surf2 = FONT_MED.render("Tie game. Continue or go to Main Menu?", True, BLACK)
    txt_rect2 = txt_surf2.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(txt_surf2, txt_rect2)

# ======================================================================
# ============================= MAIN LOOP ==============================
# ======================================================================
def main():
    clock = pygame.time.Clock()

    # States
    state = STATE_MAIN_MENU

    # Player and AI info
    player_name = ""
    ai_name = "Computer"

    # Settings chosen by the user
    chosen_algo = None
    chosen_length = 15
    first_mover = "player"  # or "computer"

    current_level = 1
    best_level = 0

    # Game data
    player_score = 0
    ai_score = 0
    sequence = []
    player_turn = True

    show_error = False

    # --- Main Menu Buttons ---
    def start_enter_name():
        nonlocal state
        state = STATE_ENTER_NAME

    buttons_main_menu = [
        Button(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 60, "Play",
               callback=start_enter_name, font=FONT_MED, color=GREEN),
        Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60, "Exit",
               callback=lambda: sys.exit(0), font=FONT_MED, color=RED)
    ]

    # --- Choose Settings Buttons ---
    def set_algo_minimax():
        nonlocal chosen_algo, show_error
        chosen_algo = "Minimax"
        show_error = False

    def set_algo_alphabeta():
        nonlocal chosen_algo, show_error
        chosen_algo = "Alpha-Beta"
        show_error = False

    def length_minus():
        nonlocal chosen_length
        if chosen_length > 15:
            chosen_length -= 1

    def length_plus():
        nonlocal chosen_length
        if chosen_length < 20:
            chosen_length += 1

    def set_first_player():
        nonlocal first_mover
        first_mover = "player"

    def set_first_computer():
        nonlocal first_mover
        first_mover = "computer"

    def go_to_rules():
        nonlocal chosen_algo, show_error, state
        if chosen_algo is None:
            show_error = True
        else:
            show_error = False
            state = STATE_RULES

    buttons_choose_settings = [
        Button(WIDTH//2 - 160, 280, 140, 50, "Minimax", set_algo_minimax),
        Button(WIDTH//2 +  20, 280, 140, 50, "Alpha-Beta", set_algo_alphabeta),

        Button(WIDTH//2 - 160, 350, 60, 50, "-Len", length_minus),
        Button(WIDTH//2 + 100, 350, 60, 50, "+Len", length_plus),

        Button(WIDTH//2 - 160, 420, 140, 50, "Player", set_first_player),
        Button(WIDTH//2 +  20, 420, 140, 50, "Computer", set_first_computer),

        Button(WIDTH//2 - 100, 500, 200, 60, "Start Game", go_to_rules, color=GREEN)
    ]

    # --- Rules Screen Button ---
    def init_game():
        """
        Iniciē jaunu raundu (jaunu spēli) ar izvēlētajiem iestatījumiem.
        """
        nonlocal state, sequence, player_score, ai_score, player_turn
        sequence = generate_sequence(chosen_length)
        player_score = 0
        ai_score = 0
        player_turn = (first_mover == "player")
        state = STATE_GAME

    buttons_rules_screen = [
        Button(WIDTH//2 - 100, HEIGHT - 100, 200, 60, "Start",
               callback=init_game, color=BLUE)
    ]

    # --- Win Screen Buttons ---
    def go_main_menu():
        nonlocal state
        state = STATE_MAIN_MENU

    def continue_game():
        nonlocal current_level
        current_level += 1
        init_game()

    buttons_game_over_win = [
        Button(WIDTH//2 - 220, HEIGHT//2 + 50, 200, 60, "Main Menu",
               callback=go_main_menu, font=FONT_MED, color=GRAY),
        Button(WIDTH//2 + 20, HEIGHT//2 + 50, 200, 60, "Continue",
               callback=continue_game, font=FONT_MED, color=GREEN)
    ]

    # --- Lose Screen Buttons ---
    def replay_game():
        nonlocal current_level
        current_level = 1
        init_game()

    buttons_game_over_lose = [
        Button(WIDTH//2 - 220, HEIGHT//2 + 50, 200, 60, "Play Again",
               callback=replay_game, font=FONT_MED, color=GRAY),
        Button(WIDTH//2 + 20, HEIGHT//2 + 50, 200, 60, "Main Menu",
               callback=go_main_menu, font=FONT_MED, color=RED)
    ]

    # --- Draw Screen Buttons ---
    # Same logic: user can continue or go to main menu
    buttons_game_over_draw = [
        Button(WIDTH//2 - 220, HEIGHT//2 + 50, 200, 60, "Main Menu",
               callback=go_main_menu, font=FONT_MED, color=GRAY),
        Button(WIDTH//2 + 20, HEIGHT//2 + 50, 200, 60, "Continue",
               callback=continue_game, font=FONT_MED, color=GREEN)
    ]

    # --- End Game function ---
    def end_game(result):
        """
        result var būt: 'player' (win), 'ai' (lose) vai 'draw' (neizšķirts).
        """
        nonlocal state, best_level, current_level
        if result == 'player':
            # Player win
            if current_level > best_level:
                best_level = current_level
            state = STATE_GAME_OVER_WIN
        elif result == 'ai':
            # Player lose
            state = STATE_GAME_OVER_LOSE
        else:
            # draw
            state = STATE_GAME_OVER_DRAW

    # --- Main Loop ---
    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle text input for player's name
            if state == STATE_ENTER_NAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(player_name.strip()) == 0:
                            player_name = "Player"
                        state = STATE_CHOOSE_SETTINGS
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 15 and event.unicode.isprintable():
                            player_name += event.unicode

            # Buttons in different states
            if state == STATE_MAIN_MENU:
                for btn in buttons_main_menu:
                    btn.check_event(event)

            elif state == STATE_CHOOSE_SETTINGS:
                for btn in buttons_choose_settings:
                    btn.check_event(event)

            elif state == STATE_RULES:
                for btn in buttons_rules_screen:
                    btn.check_event(event)

            elif state == STATE_GAME:
                if player_turn:
                    # Player clicks
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = event.pos
                        for rect, val in number_buttons:
                            if rect.collidepoint(mouse_pos) and val in sequence:
                                mods = pygame.key.get_mods()
                                if mods & pygame.KMOD_SHIFT:
                                    # Shift-click -> split
                                    if val == 2:
                                        idx_in_seq = sequence.index(val)
                                        sequence.pop(idx_in_seq)
                                        sequence.insert(idx_in_seq, 1)
                                        sequence.insert(idx_in_seq+1, 1)
                                        # Splitting 2: +1 to AI
                                        ai_score += 1
                                    elif val == 4:
                                        idx_in_seq = sequence.index(val)
                                        sequence.pop(idx_in_seq)
                                        sequence.insert(idx_in_seq, 2)
                                        sequence.insert(idx_in_seq+1, 2)
                                        # Splitting 4: -1 to AI
                                        ai_score = max(0, ai_score - 1)
                                else:
                                    # Take
                                    player_score += val
                                    idx_in_seq = sequence.index(val)
                                    sequence.pop(idx_in_seq)

                                player_turn = False
                                break
                else:
                    # AI turn
                    pygame.time.wait(500)  # AI "thinking"
                    sequence, ai_score, player_score = ai_move(sequence, ai_score, player_score, chosen_algo)
                    player_turn = True

                # Check if sequence is empty -> end game
                if len(sequence) == 0:
                    if player_score > ai_score:
                        end_game("player")
                    elif ai_score > player_score:
                        end_game("ai")
                    else:
                        end_game("draw")

            elif state == STATE_GAME_OVER_WIN:
                for btn in buttons_game_over_win:
                    btn.check_event(event)

            elif state == STATE_GAME_OVER_LOSE:
                for btn in buttons_game_over_lose:
                    btn.check_event(event)

            elif state == STATE_GAME_OVER_DRAW:
                for btn in buttons_game_over_draw:
                    btn.check_event(event)

        # --- Rendering ---
        if state == STATE_MAIN_MENU:
            draw_main_menu()
            draw_best_level(best_level)
            for btn in buttons_main_menu:
                btn.draw(SCREEN)

        elif state == STATE_ENTER_NAME:
            draw_enter_name(player_name)

        elif state == STATE_CHOOSE_SETTINGS:
            draw_choose_settings(player_name, chosen_algo, chosen_length, first_mover, show_error)
            for btn in buttons_choose_settings:
                btn.draw(SCREEN)

        elif state == STATE_RULES:
            draw_rules_screen()
            for btn in buttons_rules_screen:
                btn.draw(SCREEN)

        elif state == STATE_GAME:
            draw_game_screen(player_name, player_score,
                             ai_name, ai_score,
                             current_level, best_level, sequence)

        elif state == STATE_GAME_OVER_WIN:
            draw_game_over_win(player_name)
            for btn in buttons_game_over_win:
                btn.draw(SCREEN)

        elif state == STATE_GAME_OVER_LOSE:
            draw_game_over_lose(ai_name)
            for btn in buttons_game_over_lose:
                btn.draw(SCREEN)

        elif state == STATE_GAME_OVER_DRAW:
            draw_game_over_draw()
            for btn in buttons_game_over_draw:
                btn.draw(SCREEN)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
