# исправления добавления интсрукции

import pygame
import random
import sys

pygame.init()

# --- Глобальные настройки окна ---
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Splitting Game (Pygame)")

# --- Общие цвета ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (200, 200, 200)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE  = (0, 100, 255)

# --- Шрифты ---
FONT_BIG = pygame.font.SysFont("Arial", 40, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 30)
FONT_SML = pygame.font.SysFont("Arial", 24)

# --- Разные состояния игры (экраны) ---
STATE_MAIN_MENU       = 0  # Главное меню
STATE_ENTER_NAME      = 1  # Ввод имени
STATE_CHOOSE_SETTINGS = 2  # Параметры игры (алгоритм, длина и кто ходит первым)
STATE_GAME            = 3  # Игровое поле
STATE_GAME_OVER_WIN   = 4  # Экран завершения (победа игрока)
STATE_GAME_OVER_LOSE  = 5  # Экран завершения (победа ИИ или ничья)
STATE_RULES           = 6  # Экран с правилами

# --- Кнопка (простая заготовка) ---
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

# --- Функции для генерации и логики ---
def generate_sequence(length):
    """
    Генерирует список случайных чисел заданной длины (length) из [1, 2, 3, 4].
    """
    sequence = [random.choice([1, 2, 3, 4]) for _ in range(length)]
    return sequence

def ai_move(sequence, ai_score, chosen_algo):
    """
    Логика хода ИИ в зависимости от chosen_algo.
    По умолчанию (заглушка) ИИ берёт случайное число из последовательности.
    """
    if not sequence:
        return sequence, ai_score

    if chosen_algo == "Minimax":
        # TODO: Реализовать Minimax
        # Заглушка: берём случайное число
        chosen_value = random.choice(sequence)
        sequence.remove(chosen_value)
        ai_score += chosen_value

    elif chosen_algo == "Alpha-Beta":
        # TODO: Реализовать Alpha-Beta
        # Заглушка: берём случайное число
        chosen_value = random.choice(sequence)
        sequence.remove(chosen_value)
        ai_score += chosen_value

    else:
        # Если алгоритм не выбран, делаем простой (случайный) ход
        chosen_value = random.choice(sequence)
        sequence.remove(chosen_value)
        ai_score += chosen_value

    return sequence, ai_score

# --- Главное меню ---
def draw_main_menu():
    SCREEN.fill(WHITE)
    title_surf = FONT_BIG.render("Main Menu", True, BLACK)
    title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
    SCREEN.blit(title_surf, title_rect)

def draw_best_level(best_level):
    """
    Рисует текст с лучшим достигнутым уровнем (если он есть).
    """
    if best_level > 0:
        txt = f"Best level reached: {best_level}"
    else:
        txt = "No best level yet (haven't played/won yet)"
    text_surf = FONT_SML.render(txt, True, BLACK)
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//4 + 50))
    SCREEN.blit(text_surf, text_rect)

# --- Ввод имени ---
def draw_enter_name(player_name):
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render("Enter your name:", True, BLACK)
    txt_rect = txt_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
    SCREEN.blit(txt_surf, txt_rect)

    # Отображаем текущее значение player_name
    name_surf = FONT_MED.render(player_name, True, BLACK)
    name_rect = name_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
    # Рамка вокруг имени
    pygame.draw.rect(SCREEN, GRAY,
                     (name_rect.x - 10, name_rect.y - 5,
                      name_rect.width + 20, name_rect.height + 10),
                     2)
    SCREEN.blit(name_surf, name_rect)

# --- Экран выбора настроек ---
def draw_choose_settings(player_name, chosen_algo, chosen_length, first_mover, show_error):
    """
    Отрисовка экрана «Параметры игры», где выбираются алгоритм, длина последовательности,
    кто ходит первым и кнопка «Начать игру».
    """
    SCREEN.fill(WHITE)
    # Заголовок
    title_surf = FONT_BIG.render("Game Settings", True, BLACK)
    title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
    SCREEN.blit(title_surf, title_rect)

    # Имя игрока (под заголовком)
    name_text = f"Player: {player_name}"
    name_surf = FONT_MED.render(name_text, True, BLACK)
    name_rect = name_surf.get_rect(center=(WIDTH//2, 110))
    SCREEN.blit(name_surf, name_rect)

    # Текущие настройки
    algo_str = chosen_algo if chosen_algo else "Not selected"
    algo_color = RED if (show_error and chosen_algo is None) else BLACK
    algo_text = f"Algorithm: {algo_str}"
    algo_surf = FONT_SML.render(algo_text, True, algo_color)
    algo_rect = algo_surf.get_rect(center=(WIDTH//2, 160))
    SCREEN.blit(algo_surf, algo_rect)

    len_text = f"Length: {chosen_length}"
    len_surf = FONT_SML.render(len_text, True, BLACK)
    len_rect = len_surf.get_rect(center=(WIDTH//2, 190))
    SCREEN.blit(len_surf, len_rect)

    fm_text = "Player" if first_mover == "player" else "Computer"
    fm_surf_text = f"Goes first: {fm_text}"
    fm_surf = FONT_SML.render(fm_surf_text, True, BLACK)
    fm_rect = fm_surf.get_rect(center=(WIDTH//2, 220))
    SCREEN.blit(fm_surf, fm_rect)

    # Если надо показать сообщение об ошибке
    if show_error and chosen_algo is None:
        error_msg = "Please select an algorithm!"
        err_surf = FONT_SML.render(error_msg, True, RED)
        err_rect = err_surf.get_rect(center=(WIDTH//2, 260))
        SCREEN.blit(err_surf, err_rect)

# --- Экран (окошко) с правилами ---
def draw_rules_screen():
    SCREEN.fill(WHITE)
    # Заголовок
    title_surf = FONT_BIG.render("Īss spēles apraksts", True, BLACK)
    title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
    SCREEN.blit(title_surf, title_rect)

    # Список правил (на латышском, как вы попросили)
    lines = [
        "1. At the beginning of the game, a generated sequence of numbers is presented. Each player initially has 0 points.",
        "2. Players take turns in sequence. During a turn, a player can:",
        "   - Take any number from the sequence and add it to their score.",
        "   - Split the number '2' into two '1's and give one point to the opponent.",
        "   - Split the number '4' into two '2's and subtract one point from the opponent’s score.",
        "3. The game ends when the sequence is empty. The player with the most points wins.",
        "",
        "Click << Start >> to proceed directly to the game."
    ]

    y_offset = 120
    for line in lines:
        line_surf = FONT_SML.render(line, True, BLACK)
        SCREEN.blit(line_surf, (50, y_offset))
        y_offset += 30

# --- Игровой экран ---
def draw_game_screen(player_name, player_score, ai_name, ai_score,
                     level, best_level, sequence):
    SCREEN.fill(WHITE)

    # Левый верхний угол: Имя игрока и его очки
    left_text = f"{player_name} (Score: {player_score})"
    left_surf = FONT_SML.render(left_text, True, BLACK)
    SCREEN.blit(left_surf, (20, 20))

    # Правый верхний угол: Имя (Компьютер) + Уровень + Очки
    right_text = f"{ai_name} Level {level} (Score: {ai_score})"
    right_surf = FONT_SML.render(right_text, True, BLACK)
    SCREEN.blit(right_surf, (WIDTH - right_surf.get_width() - 20, 20))

    # По центру сверху - лучший достигнутый уровень
    if best_level > 0:
        center_text = f"Best level: {best_level}"
        center_surf = FONT_SML.render(center_text, True, BLACK)
        center_rect = center_surf.get_rect(center=(WIDTH//2, 20))
        SCREEN.blit(center_surf, center_rect)

    # Отображаем последовательность "кнопками"
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
        # Перенос на следующую строку, если не влезает
        if x + btn_w > WIDTH - 50:
            x = start_x
            y += btn_h + gap

    # Пояснение про SHIFT
    shift_text1 = "Shift + 2 => splits into (1 and 1) and gives +1 point to the opponent."
    shift_text2 = "Shift + 4 => splits into (2 and 2) and subtracts 1 point from the opponent."
    st1_surf = FONT_SML.render(shift_text1, True, BLACK)
    st2_surf = FONT_SML.render(shift_text2, True, BLACK)
    SCREEN.blit(st1_surf, (50, HEIGHT - 60))
    SCREEN.blit(st2_surf, (50, HEIGHT - 30))

# --- Экран завершения игры (выиграл игрок) ---
def draw_game_over_win(player_name):
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render(f"Congratulations, {player_name}!", True, BLACK)
    txt_rect = txt_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(txt_surf, txt_rect)

    txt_surf2 = FONT_MED.render("You won! What’s next?", True, BLACK)
    txt_rect2 = txt_surf2.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(txt_surf2, txt_rect2)

# --- Экран завершения игры (выиграл ИИ / ничья) ---
def draw_game_over_lose(ai_name):
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render("You lost...", True, BLACK)
    txt_rect = txt_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(txt_surf, txt_rect)

    txt_surf2 = FONT_MED.render(f"You won {ai_name} Or it's a draw.", True, BLACK)
    txt_rect2 = txt_surf2.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(txt_surf2, txt_rect2)

# --- Основной цикл ---
def main():
    clock = pygame.time.Clock()

    # Переменные состояний
    state = STATE_MAIN_MENU

    # Данные игрока и игры
    player_name = ""
    ai_name = "Computer"

    # Параметры, которые пользователь настраивает:
    chosen_algo = None
    chosen_length = 15
    first_mover = "player"  # 'player' или 'computer'

    current_level = 1
    best_level = 0

    # Данные для игры (очки, последовательность, чей ход)
    player_score = 0
    ai_score = 0
    sequence = []
    player_turn = True  # Кто ходит сейчас

    # Флаг для ошибки (если пытаются начать без алгоритма)
    show_error = False

    # --- Функции и кнопки ---
    def start_enter_name():
        nonlocal state
        state = STATE_ENTER_NAME

    buttons_main_menu = [
        Button(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 60, "Play",
               callback=start_enter_name,
               font=FONT_MED, color=GREEN, text_color=BLACK),
        Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60, "Exit",
               callback=lambda: sys.exit(0),
               font=FONT_MED, color=RED, text_color=BLACK)
    ]

    # Кнопки экрана "Параметры игры"
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

    # Раньше здесь вызывали init_game(), теперь переходим к экрану правил:
    def go_to_rules():
        nonlocal chosen_algo, show_error, state
        if chosen_algo is None:
            show_error = True
        else:
            show_error = False
            state = STATE_RULES

    buttons_choose_settings = [
        # Первая строка: выбор алгоритма
        Button(WIDTH//2 - 160, 280, 140, 50, "Minimax", set_algo_minimax),
        Button(WIDTH//2 +  20, 280, 140, 50, "Alpha-Beta", set_algo_alphabeta),

        # Вторая строка: длина - / +
        Button(WIDTH//2 - 160, 350, 60, 50, "-Len", length_minus),
        Button(WIDTH//2 + 100, 350, 60, 50, "+Len", length_plus),

        # Третья строка: кто ходит первым
        Button(WIDTH//2 - 160, 420, 140, 50, "Player", set_first_player),
        Button(WIDTH//2 +  20, 420, 140, 50, "Computer", set_first_computer),

        # Кнопка "Начать игру" -> ведёт на экран правил
        Button(WIDTH//2 - 100, 500, 200, 60, "Start Game", go_to_rules, color=GREEN)
    ]

    # Экран правил (STATE_RULES)
    def init_game():
        """
        Инициализация новой партии (раунда).
        """
        nonlocal state, sequence, player_score, ai_score, player_turn
        # Генерируем новую последовательность, учитывая chosen_length
        sequence = generate_sequence(chosen_length)
        # Обнуляем очки
        player_score = 0
        ai_score = 0
        # Кто ходит первым зависит от first_mover
        player_turn = (first_mover == "player")

        state = STATE_GAME

    # Кнопка на экране правил
    buttons_rules_screen = [
        Button(WIDTH//2 - 100, HEIGHT - 100, 200, 60, "Start", callback=init_game, color=BLUE)
    ]

    # На экране "Победа игрока"
    def go_main_menu():
        nonlocal state
        state = STATE_MAIN_MENU

    def continue_game():
        nonlocal current_level
        current_level += 1
        init_game()

    buttons_game_over_win = [
        Button(WIDTH//2 - 220, HEIGHT//2 + 50, 200, 60, "Main Menu",
               callback=go_main_menu,
               font=FONT_MED, color=GRAY, text_color=BLACK),
        Button(WIDTH//2 + 20, HEIGHT//2 + 50, 200, 60, "Continue",
               callback=continue_game,
               font=FONT_MED, color=GREEN, text_color=BLACK)
    ]

    # На экране "Проигрыш"
    def replay_game():
        nonlocal current_level
        current_level = 1
        init_game()

    buttons_game_over_lose = [
        Button(WIDTH//2 - 220, HEIGHT//2 + 50, 200, 60, "Play Again",
               callback=replay_game,
               font=FONT_MED, color=GRAY, text_color=BLACK),
        Button(WIDTH//2 + 20, HEIGHT//2 + 50, 200, 60, "Main Menu",
               callback=go_main_menu,
               font=FONT_MED, color=RED, text_color=BLACK)
    ]

    # --- Локальные функции ---
    def end_game(winner):
        nonlocal state, best_level, current_level
        if winner == 'player':
            # Проверяем, не побили ли мы лучший уровень
            if current_level > best_level:
                best_level = current_level
            state = STATE_GAME_OVER_WIN
        else:
            # ИИ выиграл или ничья
            state = STATE_GAME_OVER_LOSE

    # --- Основной цикл приложения ---
    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Ввод текста при STATE_ENTER_NAME
            if state == STATE_ENTER_NAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(player_name.strip()) == 0:
                            player_name = "Игрок"
                        state = STATE_CHOOSE_SETTINGS
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 15 and event.unicode.isprintable():
                            player_name += event.unicode

            # Обработка кнопок в разных состояниях
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
                # Если сейчас ход игрока и кликаем по числам
                if player_turn:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = event.pos
                        for rect, val in number_buttons:
                            if rect.collidepoint(mouse_pos):
                                # Защита от двойного клика
                                if val not in sequence:
                                    break

                                mods = pygame.key.get_mods()
                                # Если SHIFT зажат -> "разделить" число
                                if mods & pygame.KMOD_SHIFT:
                                    if val == 2:
                                        idx_in_seq = sequence.index(val)
                                        sequence.pop(idx_in_seq)
                                        sequence.insert(idx_in_seq, 1)
                                        sequence.insert(idx_in_seq+1, 1)
                                        # Пример: при разделении 2, +1 к ИИ
                                        ai_score += 1
                                    elif val == 4:
                                        idx_in_seq = sequence.index(val)
                                        sequence.pop(idx_in_seq)
                                        sequence.insert(idx_in_seq, 2)
                                        sequence.insert(idx_in_seq+1, 2)
                                        # Пример: при разделении 4, -1 к ИИ (не меньше нуля)
                                        ai_score = max(0, ai_score - 1)
                                    # Если число не 2 и не 4 – игнорируем
                                else:
                                    # Просто берём число и добавляем к очкам игрока
                                    player_score += val
                                    idx_in_seq = sequence.index(val)
                                    sequence.pop(idx_in_seq)

                                # Ход закончен, передаём ход ИИ
                                player_turn = False
                                break
                else:
                    # Ход ИИ:
                    pygame.time.wait(500)  # ИИ "думает" (полсекунды)
                    sequence, ai_score = ai_move(sequence, ai_score, chosen_algo)
                    # Возврат хода игроку
                    player_turn = True

                # Проверяем, не опустела ли последовательность
                if len(sequence) == 0:
                    if player_score > ai_score:
                        end_game("player")
                    else:
                        end_game("ai")  # ничья тоже считаем поражением игрока

            elif state == STATE_GAME_OVER_WIN:
                for btn in buttons_game_over_win:
                    btn.check_event(event)

            elif state == STATE_GAME_OVER_LOSE:
                for btn in buttons_game_over_lose:
                    btn.check_event(event)

        # --- Отрисовка ---
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

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
