from game.Path import Path
from game.Sprites import *
from game.BallGenerator import BallGenerator
from game.ShootingManager import ShootingManager
from game.BonusManager import BonusManager
from game.ScoreManager import ScoreManager
from game.ui import *


class Level:
    def __init__(self, number, score_manager):
        self.number = number
        
        self.path = Path(number)
        self.ball_generator = BallGenerator(self.path, number * 20, score_manager)
        self.bonus_manager = BonusManager(self.ball_generator)
        self.player = Player(number)
        self.finish = Finish(self.path, self.ball_generator.balls, score_manager)
        self.shooting_manager = ShootingManager(self.ball_generator, self.player.pos,
                                                 self.bonus_manager, score_manager)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Zuma")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level_num = 1
        self.score_manager = ScoreManager()
        self.setup_new_game()
        self.is_quit = False
        self.is_paused = False  # Trạng thái Pause

    def play(self):
        self.continue_game(self.ui_manager.start_game_btn,
                           self.ui_manager.start_game_display)
        while not self.is_quit:
            self.setup_new_game()
            self.play_game()

        pygame.quit()

    def setup_new_game(self):
        self.level = Level(self.level_num, self.score_manager)
        self.ui_manager = UiManager(self.screen, self.level)
    def draw_pause_message(self):
        if self.is_paused:
            pause_label = Label("PAUSED", (WIDTH // 2, HEIGHT // 2), color=WHITE)
            self.ui_manager.put_label(pause_label)

    def play_game(self):
        game_finished = False

        while not game_finished and not self.is_quit:
            if not self.is_paused:  # Chỉ cập nhật trò chơi khi không ở trạng thái Pause
                self.level.ball_generator.generate()
                self.clock.tick(FPS)
                self.update_sprites()

            self.update_display(self.ui_manager.game_display)  # Cập nhật giao diện trò chơi
            self.draw_pause_message()  # Hiển thị thông báo Pause nếu cần

            if not self.is_paused:  # Chỉ kiểm tra trạng thái thắng/thua khi không Pause
                if self.score_manager.is_win:
                    game_finished = True
                    self.handle_win()
                elif self.score_manager.is_lose:
                    game_finished = True
                    self.handle_lose()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Xử lý nút Pause
                    if self.ui_manager.is_pause_clicked(mouse_pos):
                        self.is_paused = not self.is_paused  # Chuyển đổi trạng thái Pause
                    elif not self.is_paused:  # Chỉ bắn bóng nếu không Pause
                        self.level.shooting_manager.shoot(mouse_pos)



    def handle_win(self):
        if self.level_num == 3:
            self.win_game()
        else:
            self.continue_game(self.ui_manager.continue_btn,
                               self.ui_manager.win_level_display)
            self.level_num += 1
            self.score_manager.setup_next_level()

    def handle_lose(self):
        """
    Phương thức xử lý khi người chơi thua trò chơi:
    - Giảm số mạng sống của người chơi.
    - Hiển thị giao diện tương ứng (thua trò chơi hoặc thua cấp độ).
    - Nếu người chơi hết mạng, đặt lại trò chơi từ đầu.
    - Nếu người chơi còn mạng, cho phép bắt đầu lại cấp độ.

    Variables:
        self.score_manager: Quản lý điểm số và số mạng của người chơi.
        self.ui_manager: Quản lý giao diện màn hình hiển thị.
        self.level_num: Biến lưu cấp độ hiện tại của trò chơi.
    """
        # 1. Giảm số mạng sống của người chơi khi thua
        self.score_manager.take_live()  
        
        # 2. Kiểm tra nếu người chơi đã hết mạng sống (thua trò chơi hoàn toàn)
        if self.score_manager.lose_game:  
            # Hiển thị giao diện thua toàn bộ trò chơi
            self.continue_game(self.ui_manager.new_game_button,
                            self.ui_manager.lose_game_display)
            
            # Đặt lại trò chơi: 
            # - Cấp độ trở về 1.
            # - Khởi tạo lại ScoreManager để reset điểm và số mạng.
            self.level_num = 1
            self.score_manager = ScoreManager()
        
        # 3. Người chơi vẫn còn mạng, cho phép bắt đầu lại cấp độ hiện tại
        else:
            # Hiển thị giao diện thua cấp độ hiện tại và cho phép người chơi bắt đầu lại cấp độ
            self.continue_game(self.ui_manager.start_level_again_btn,
                            self.ui_manager.lose_level_display)
            
            # Thiết lập lại trạng thái cho cấp độ tiếp theo
            self.score_manager.setup_next_level()


  
    

    def continue_game(self, button, window):
        """
        Phương thức này giúp tạm dừng trò chơi tại một màn hình cụ thể 
        (ví dụ: màn hình thắng, thua, hoặc bắt đầu) và chỉ tiếp tục khi người chơi 
        nhấn vào một nút xác định.

        Args:
            button: Nút mà người chơi cần nhấn để tiếp tục trò chơi.
            window: Giao diện màn hình hiện tại (hiển thị nút và các yếu tố khác).

        Variables:
            game_continued: Cờ báo hiệu liệu người chơi đã nhấn nút để tiếp tục hay chưa.
            mouse: Vị trí hiện tại của con trỏ chuột.
        """
        game_continued = False  # Khởi tạo cờ báo hiệu trò chơi chưa tiếp tục

        while not game_continued and not self.is_quit:  # Vòng lặp chờ người chơi nhấn nút
            mouse = pygame.mouse.get_pos()  # Lấy vị trí hiện tại của chuột
            
            for event in pygame.event.get():  # Lặp qua các sự kiện trong hàng đợi sự kiện
                if event.type == pygame.QUIT:  # Kiểm tra nếu người chơi muốn thoát trò chơi
                    self.is_quit = True  # Đặt cờ thoát là True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra nếu có nhấn chuột
                    if button.rect.collidepoint(mouse):  # Kiểm tra nếu nhấn vào nút được chỉ định
                        game_continued = True  # Cập nhật cờ báo hiệu để thoát vòng lặp

            # Cập nhật màn hình giao diện tạm dừng (màn hình thắng, thua, hoặc bắt đầu)
            self.update_display(window)


    def win_game(self):
        on_win_window = True
        while on_win_window and not self.is_quit:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui_manager.start_game_again_btn.rect.collidepoint(mouse):
                        on_win_window = False
                        self.level_num = 1
                    elif self.ui_manager.finish_btn.rect.collidepoint(mouse):
                        self.is_quit = True

            self.update_display(self.ui_manager.win_game_display)

    def update_sprites(self):
        self.level.player.update()
        self.level.shooting_manager.update()
        self.level.ball_generator.update()
        self.level.bonus_manager.update()
        self.level.finish.update()

    def update_display(self, display):
        self.ui_manager.draw_window(display)
        if display is self.ui_manager.game_display:
            self.ui_manager.show_score(self.score_manager.score)
            self.ui_manager.show_lives(self.score_manager.lives)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.play()
