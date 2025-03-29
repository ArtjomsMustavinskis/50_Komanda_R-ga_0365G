import pygame
import random
import sys

pygame.init()

# --- Глобальные настройки окна ---
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра с разделением чисел (Pygame)")

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

# ----------------------------------------------------------------------------------
def ai_move(sequence, ai_score, chosen_algo):
    """
    Здесь вы можете вставить логику Minimax или Alpha-Beta, в зависимости от
    значения chosen_algo (например, 'Minimax' или 'Alpha-Beta').

    # TODO: Вставьте реализацию Minimax / Alpha-Beta ниже:
    """

    if not sequence:
        return sequence, ai_score

    if chosen_algo == "Minimax":
        # TODO: Здесь вызываем/реализуем Minimax
        # Заглушка: берём случайное число
        chosen_value = random.choice(sequence)
        sequence.remove(chosen_value)
        ai_score += chosen_value

    elif chosen_algo == "Alpha-Beta":
        # TODO: Здесь вызываем/реализуем Alpha-Beta
        # Заглушка: берём случайное число
        chosen_value = random.choice(sequence)
        sequence.remove(chosen_value)
        ai_score += chosen_value

    else:
        # На случай, если алгоритм не выбран, делаем простой ход (берём случайное число)
        chosen_value = random.choice(sequence)
        sequence.remove(chosen_value)
        ai_score += chosen_value

    return sequence, ai_score
# ----------------------------------------------------------------------------------

# --- Главное меню ---
def draw_main_menu():
    SCREEN.fill(WHITE)
    title_surf = FONT_BIG.render("Главное меню", True, BLACK)
    title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
    SCREEN.blit(title_surf, title_rect)

def draw_best_level(best_level):
    """
    Рисует текст с лучшим достигнутым уровнем (если он есть).
    """
    if best_level > 0:
        txt = f"Лучший достигнутый уровень: {best_level}"
    else:
        txt = "Ещё нет лучшего уровня (не играли/не выигрывали)"
    text_surf = FONT_SML.render(txt, True, BLACK)
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//4 + 50))
    SCREEN.blit(text_surf, text_rect)

# --- Ввод имени ---
def draw_enter_name(player_name):
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render("Введите ваше имя:", True, BLACK)
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
    title_surf = FONT_BIG.render("Параметры игры", True, BLACK)
    title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
    SCREEN.blit(title_surf, title_rect)

    # Имя игрока (под заголовком)
    name_text = f"Игрок: {player_name}"
    name_surf = FONT_MED.render(name_text, True, BLACK)
    name_rect = name_surf.get_rect(center=(WIDTH//2, 110))
    SCREEN.blit(name_surf, name_rect)

    # Текущие настройки
    algo_str = chosen_algo if chosen_algo else "Не выбран"
    # Если пользователь нажимает «Начать игру», но алгоритм не выбран, выводим красный текст
    algo_color = RED if (show_error and chosen_algo is None) else BLACK
    algo_text = f"Алгоритм: {algo_str}"
    algo_surf = FONT_SML.render(algo_text, True, algo_color)
    algo_rect = algo_surf.get_rect(center=(WIDTH//2, 160))
    SCREEN.blit(algo_surf, algo_rect)

    len_text = f"Длина: {chosen_length}"
    len_surf = FONT_SML.render(len_text, True, BLACK)
    len_rect = len_surf.get_rect(center=(WIDTH//2, 190))
    SCREEN.blit(len_surf, len_rect)

    fm_text = "Игрок" if first_mover == "player" else "Компьютер"
    fm_surf_text = f"Первым ходит: {fm_text}"
    fm_surf = FONT_SML.render(fm_surf_text, True, BLACK)
    fm_rect = fm_surf.get_rect(center=(WIDTH//2, 220))
    SCREEN.blit(fm_surf, fm_rect)

    # Если надо показать сообщение об ошибке
    if show_error and chosen_algo is None:
        error_msg = "Пожалуйста, выберите алгоритм!"
        err_surf = FONT_SML.render(error_msg, True, RED)
        err_rect = err_surf.get_rect(center=(WIDTH//2, 260))
        SCREEN.blit(err_surf, err_rect)

# --- Игровой экран ---
def draw_game_screen(player_name, player_score, ai_name, ai_score,
                     level, best_level, sequence):
    SCREEN.fill(WHITE)

    # Левый верхний угол: Имя игрока и его очки
    left_text = f"{player_name} (Очки: {player_score})"
    left_surf = FONT_SML.render(left_text, True, BLACK)
    SCREEN.blit(left_surf, (20, 20))

    # Правый верхний угол: Имя (Компьютер) + Уровень + Очки
    right_text = f"{ai_name} Уровень {level} (Очки: {ai_score})"
    right_surf = FONT_SML.render(right_text, True, BLACK)
    SCREEN.blit(right_surf, (WIDTH - right_surf.get_width() - 20, 20))

    # По центру сверху - лучший достигнутый уровень
    if best_level > 0:
        center_text = f"Лучший уровень: {best_level}"
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
        if x + btn_w > WIDTH - 50:
            x = start_x
            y += btn_h + gap

# --- Экран завершения игры (выиграл игрок) ---
def draw_game_over_win(player_name):
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render(f"Поздравляем, {player_name}!", True, BLACK)
    txt_rect = txt_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(txt_surf, txt_rect)

    txt_surf2 = FONT_MED.render("Вы выиграли! Что дальше?", True, BLACK)
    txt_rect2 = txt_surf2.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(txt_surf2, txt_rect2)

# --- Экран завершения игры (выиграл ИИ / ничья) ---
def draw_game_over_lose(ai_name):
    SCREEN.fill(WHITE)
    txt_surf = FONT_BIG.render("Вы проиграли...", True, BLACK)
    txt_rect = txt_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(txt_surf, txt_rect)

    txt_surf2 = FONT_MED.render(f"Победил {ai_name} или ничья.", True, BLACK)
    txt_rect2 = txt_surf2.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(txt_surf2, txt_rect2)

# --- Основной цикл ---
def main():
    clock = pygame.time.Clock()

    # Переменные состояний
    state = STATE_MAIN_MENU

    # Данные игрока и игры
    player_name = ""
    ai_name = "Компьютер"

    # Параметры, которые пользователь настраивает:
    chosen_algo = None
    chosen_length = 15
    first_mover = "player"  # либо 'player', либо 'computer'

    current_level = 1
    best_level = 0

    # Данные для игры (очки, последовательность, чьи ход)
    player_score = 0
    ai_score = 0
    sequence = []
    player_turn = True  # Кто ходит сейчас

    # Флаг для ошибки (если пытаются начать без алгоритма)
    show_error = False

    # --- Кнопки (некоторые будут видны только в нужных состояниях) ---
    def start_enter_name():
        nonlocal state
        state = STATE_ENTER_NAME

    buttons_main_menu = [
        Button(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 60, "Сыграть",
               callback=start_enter_name,
               font=FONT_MED, color=GREEN, text_color=BLACK),
        Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60, "Выйти",
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

    def start_game():
        """
        При нажатии "Начать игру" проверяем, выбрал ли пользователь алгоритм.
        Если нет, показываем сообщение об ошибке (show_error = True).
        Если да, запускаем init_game().
        """
        nonlocal chosen_algo, show_error
        if chosen_algo is None:
            show_error = True
        else:
            show_error = False
            init_game()

    buttons_choose_settings = [
        # Первая строка: выбор алгоритма
        Button(WIDTH//2 - 160, 280, 140, 50, "Minimax", set_algo_minimax),
        Button(WIDTH//2 +  20, 280, 140, 50, "Alpha-Beta", set_algo_alphabeta),

        # Вторая строка: длина -/+
        Button(WIDTH//2 - 160, 350, 60, 50, "-Len", length_minus),
        Button(WIDTH//2 +  100, 350, 60, 50, "+Len", length_plus),

        # Третья строка: кто ходит первым
        Button(WIDTH//2 - 160, 420, 140, 50, "Игрок", set_first_player),
        Button(WIDTH//2 +  20, 420, 140, 50, "Компьютер", set_first_computer),

        # Кнопка "Начать игру"
        Button(WIDTH//2 - 100, 500, 200, 60, "Начать игру", start_game, color=GREEN)
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
        Button(WIDTH//2 - 220, HEIGHT//2 + 50, 200, 60, "Главное меню",
               callback=go_main_menu,
               font=FONT_MED, color=GRAY, text_color=BLACK),
        Button(WIDTH//2 + 20, HEIGHT//2 + 50, 200, 60, "Продолжить",
               callback=continue_game,
               font=FONT_MED, color=GREEN, text_color=BLACK)
    ]

    # На экране "Проигрыш"
    def replay_game():
        nonlocal current_level
        current_level = 1
        init_game()

    buttons_game_over_lose = [
        Button(WIDTH//2 - 220, HEIGHT//2 + 50, 200, 60, "Сыграть заново",
               callback=replay_game,
               font=FONT_MED, color=GRAY, text_color=BLACK),
        Button(WIDTH//2 + 20, HEIGHT//2 + 50, 200, 60, "Главное меню",
               callback=go_main_menu,
               font=FONT_MED, color=RED, text_color=BLACK)
    ]

    # --- Локальные функции ---
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
                        # Закончили ввод, переходим к экрану настроек
                        if len(player_name.strip()) == 0:
                            player_name = "Игрок"
                        state = STATE_CHOOSE_SETTINGS
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        # Добавляем символ (если это не спец.клавиша)
                        if len(player_name) < 15 and event.unicode.isprintable():
                            player_name += event.unicode

            # Проверка нажатия кнопок (зависит от state)
            if state == STATE_MAIN_MENU:
                for btn in buttons_main_menu:
                    btn.check_event(event)

            elif state == STATE_CHOOSE_SETTINGS:
                for btn in buttons_choose_settings:
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
                                        # Пример: при разделении 4, -1 к ИИ (но не меньше нуля)
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
