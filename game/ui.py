from game.Params import *
from game.BonusManager import Bonus

BONUS_IMAGES = {
    Bonus.Pause: {
        YELLOW: 'game/images/pause_yellow.png',
        GREEN: 'game/images/pause_green.png',
        BLUE: 'game/images/pause_blue.png',
        RED: 'game/images/pause_red.png'
    },
    Bonus.Reverse: {
        YELLOW: 'game/images/reverse_yellow.png',
        GREEN: 'game/images/reverse_green.png',
        BLUE: 'game/images/reverse_blue.png',
        RED: 'game/images/reverse_red.png'
    },
    Bonus.Bomb: {
        YELLOW: 'game/images/bomb_yellow.png',
        GREEN: 'game/images/bomb_green.png',
        BLUE: 'game/images/bomb_blue.png',
        RED: 'game/images/bomb_red.png'
    },
    Bonus.Speed: {
        YELLOW: 'game/images/speed_yellow.png',
        GREEN: 'game/images/speed_green.png',
        BLUE: 'game/images/speed_blue.png',
        RED: 'game/images/speed_red.png'
    }
}

class Button:
    def __init__(self, button_title, position, width=BTN_WIDTH,
                 height=BTN_HEIGHT, background_color=BLACK, font_color=RED):
        self.title = button_title
        # Sử dụng phông chữ DejaVuSans
        self.font = pygame.font.Font('game/fonts/DejaVuSans.ttf', FONT_SIZE)
        self.title_width, self.title_height = self.font.size(self.title)
        self.center = (position[0], position[1])
        self.width, self.height = width, height
        self.x_start, self.y_start = self.center[0] - self.width // 2, \
                                     self.center[1] - self.height // 2
        self.rect = pygame.Rect((self.x_start, self.y_start,
                                 width, height))
        self.background_color = background_color
        self.font_color = font_color


class Label:
    def __init__(self, text, position, color=RED):
        # Sử dụng phông chữ DejaVuSans
        self.font = pygame.font.Font('game/fonts/DejaVuSans.ttf', FONT_SIZE)
        self.color = color
        self.text = self.font.render(text, True, color)
        self.width, self.height = self.font.size(text)
        self.x_start, self.y_start = position[0] - self.width // 2, \
                                     position[1] - self.height //2
class Label2:
    def __init__(self, text, position, color=RED):
        # Sử dụng phông chữ DejaVuSans
        self.font = pygame.font.Font('game/fonts/DejaVuSans.ttf', FONT_SIZE1)
        self.color = color
        self.text = self.font.render(text, True, color)
        self.width, self.height = self.font.size(text)
        self.x_start, self.y_start = position[0] - self.width // 2, \
                                     position[1] - self.height //2

class Display:
    def __init__(self, background_color=TAUPE, buttons=None, labels=None,
                 sprites=None):
        self.buttons = buttons if buttons is not None else []
        self.sprites = sprites if sprites is not None else []
        self.labels = labels if labels is not None else []
        self.background_color = background_color

class UiManager:
    def __init__(self, screen, level):
        self.screen = screen
        self.level = level

        # Tải hình ảnh background
        self.background_image = pygame.image.load('game/images/background3.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        self.pause_btn = Button('Pause', (WIDTH - 70, 40), width=100, height=40,
                                background_color=TAUPE, font_color=WHITE)

        self.start_game_btn = Button('Bắt đầu', SCREEN_CENTER)
        self.start_game_display = Display(buttons=[self.start_game_btn])

        self.level_label = Label('Cấp độ {}'.format(level.number), (WIDTH // 2, 40))
        sprites = [level.player, level.path, level.ball_generator,
                   level.finish, level.shooting_manager]
        self.game_display = Display(sprites=sprites, labels=[self.level_label])

        self.continue_btn = Button('Tiếp tục', SCREEN_CENTER)
        self.win_level_display = Display(buttons=[self.continue_btn])

        self.start_level_again_btn = Button('Bắt đầu lại', SCREEN_CENTER,
                                            background_color=TAUPE, font_color=GREEN)
        self.lose_level_display = Display(buttons=[self.start_level_again_btn])

        self.finish_btn = Button('Kết thúc', (WIDTH // 2, HEIGHT // 2 + 2 * BTN_HEIGHT))
        self.start_game_again_btn = Button('Bắt đầu lại', SCREEN_CENTER)
        
        # Thay thế Label2 bằng hình ảnh hoàn thành trò chơi
        self.win_image = pygame.image.load('game/images/win.png')  # Tải hình ảnh hoàn thành trò chơi
        self.win_image = pygame.transform.scale(self.win_image, (400, 400))  # Tùy chỉnh kích thước ảnh

        self.win_game_display = Display(buttons=[self.start_game_again_btn, self.finish_btn])

        self.lost_image = pygame.image.load('game/images/lost.png')  # Tải hình ảnh hoàn thành trò chơi
        self.lost_image = pygame.transform.scale(self.lost_image, (400, 400))  # Tùy chỉnh kích thước ảnh
        self.new_game_button = Button('Trò chơi mới', SCREEN_CENTER,
                                      background_color=TAUPE, font_color=BLUE)
        self.lose_game_display = Display(BROWN, buttons=[self.new_game_button])

    def draw_button(self, button):
        width, height = button.width, button.height
        x_start, y_start = button.x_start, button.y_start
        title_params = (x_start + width / 2 - button.title_width / 2,
                        y_start + height / 2 - button.title_height / 2)
        pygame.draw.rect(self.screen, button.background_color, (x_start, y_start, width, height))
        self.screen.blit(button.font.render(button.title, True, button.font_color), title_params)

    def draw_window(self, window):
            # Vẽ background
        self.screen.blit(self.background_image, (0, 0))  # Vẽ hình ảnh background lên màn hình
        for button in window.buttons:
            self.draw_button(button)
        for label in window.labels:
            self.put_label(label)
        for sprite in window.sprites:
            sprite.draw(self.screen)
        self.draw_button(self.pause_btn)
        # Nếu là màn hình thắng game, vẽ thêm hình ảnh thắng
        if window == self.win_game_display:
            # Vẽ hình ảnh tại vị trí giữa màn hình
            self.screen.blit(self.win_image, (WIDTH // 2 - 200, HEIGHT // 2 - 350 ))  # Tùy chỉnh vị trí ảnh
        if window == self.lose_game_display:
                # Vẽ hình ảnh tại vị trí giữa màn hình
            self.screen.blit(self.lost_image, (WIDTH // 2 - 200, HEIGHT // 2 - 350 ))  # Tùy chỉnh vị trí ảnh
    def is_pause_clicked(self, mouse_pos):
        return self.pause_btn.rect.collidepoint(mouse_pos)
    def show_score(self, points):
        points_label = Label('Điểm: {}'.format(points), (WIDTH // 4, 40))
        self.put_label(points_label)

    def show_lives(self, lives):
        self.put_label(Label(str(lives), (3 * WIDTH // 4 + 30, 40)))
        self.screen.blit(pygame.transform.smoothscale(
            pygame.image.load("game/images/life.png"), (20, 20)), (3 * WIDTH // 4, 30))

    def put_label(self, label):
        # Chỉ hiển thị văn bản mà không cần hình chữ nhật phía sau
        self.screen.blit(label.text, (label.x_start, label.y_start))

















