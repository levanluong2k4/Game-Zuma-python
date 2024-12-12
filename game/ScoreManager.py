class ScoreManager:
    def __init__(self):
        self.score = 0
        self.lives = 2
        self.is_win = False
        self.is_lose = False
        self.lose_game = False

    def add_score(self, score):
        # Gọi hàm add_lives(score) để kiểm tra và cộng thêm mạng sống nếu cần
        self.add_lives(score)
        # Cộng thêm điểm mới vào tổng điểm hiện tại
        self.score += score


    def add_lives(self, score):
            # Lặp qua từng điểm từ (self.score + 1) đến (self.score + score)
        for i in range(self.score + 1, self.score + score + 1):
            # Nếu điểm hiện tại chia hết cho 500
            if i % 500 == 0:
                # Tăng thêm một mạng sống (lives)
                self.lives += 1


    def take_live(self):
            # Giảm số mạng sống (lives) đi 1
        self.lives -= 1
        # Gọi hàm kiểm tra trạng thái thua (check_for_game_lose)
        self.check_for_game_lose()

    def check_for_game_lose(self):
        # Nếu số mạng sống (lives) bằng 0
        if self.lives == 0:
            # Đặt trạng thái thua trò chơi (lose_game) thành True
            self.lose_game = True


    def win(self):
        # Đặt trạng thái thắng (is_win) thành True để ghi nhận người chơi đã thắng
        self.is_win = True

    def lose(self):
        # Đặt trạng thái thua (is_lose) thành True để ghi nhận người chơi đã thua
        self.is_lose = True


    def setup_next_level(self):
            # Đặt trạng thái thắng (is_win) về False, chuẩn bị cho cấp độ mới
        self.is_win = False
        
        # Đặt trạng thái thua (is_lose) về False, chuẩn bị cho cấp độ mới
        self.is_lose = False

