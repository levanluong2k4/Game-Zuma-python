from game.Params import *
from game.Sprites import Ball
import random
import datetime


class BallGenerator:
    def __init__(self, path, number, score_manager):
        self.score_manager = score_manager
        self.path = path
        self.colors = [BLUE, RED, GREEN, YELLOW]
        self.balls = []
        self.number_to_generate = number
        self.number_of_generated = 0

        self.reverse = False
        self.pause = False  

    def generate(self):
            # Kiểm tra nếu số quả bóng đã sinh ra chưa đủ số lượng yêu cầu
        if self.number_of_generated < self.number_to_generate:
            # Nếu danh sách quả bóng trống hoặc quả bóng đầu tiên đủ xa để di chuyển
            if len(self.balls) == 0 or \
                    self.balls[0].pos_in_path >= 2 * BALL_RADIUS // \
                    self.path.step:
                # Tạo quả bóng mới với màu ngẫu nhiên và thêm vào đầu đường đi
                self.balls.insert(0, Ball(random.choice(self.colors), 0,
                                        self.path))
                # Tăng số lượng quả bóng đã tạo ra
                self.number_of_generated += 1

    def move_stopped_ball(self, i):
        # Kiểm tra xem quả bóng không thể di chuyển
        if not self.balls[i].can_move:
            if i == 0:
                # Nếu là quả bóng đầu tiên, cho phép nó di chuyển
                self.balls[i].can_move = True

            elif self.balls[i - 1].can_move and \
                    self.balls[i - 1].rect.colliderect(self.balls[i].rect):
                # Nếu quả bóng trước có thể di chuyển và va chạm với quả bóng hiện tại
                self.balls[i].can_move = True


    def update_balls(self):
            # Kiểm tra nếu trò chơi đang tạm dừng
        if self.pause:  # Nếu trò chơi tạm dừng
            return  # Không cập nhật bóng nếu trò chơi tạm dừng

        # Duyệt qua tất cả các quả bóng trong danh sách balls
        for i in range(len(self.balls)):
            self.balls[i].update()  # Cập nhật vị trí của quả bóng
            self.move_stopped_ball(i)  # Di chuyển quả bóng nếu cần


    def update_chain(self):
            # Kiểm tra nếu trò chơi đang tạm dừng
        if self.pause:
            return  # Không cập nhật chuỗi nếu trò chơi tạm dừng

        # Duyệt qua các quả bóng từ quả bóng thứ hai trong danh sách
        for i in range(1, len(self.balls)):
            left_ball = self.balls[i - 1]  # Quả bóng bên trái
            right_ball = self.balls[i]  # Quả bóng bên phải

            # Kiểm tra khoảng cách giữa hai quả bóng
            if right_ball.pos_in_path - left_ball.pos_in_path > 20:
                # Nếu màu của hai quả bóng giống nhau, kết hợp chúng lại
                if left_ball.color == right_ball.color:
                    self.join_balls(i - 1)
                # Nếu màu không giống nhau, dừng các quả bóng lại
                else:
                    self.stop_balls(i)


    def update(self):
        self.update_chain()
        if not self.reverse and not self.pause:  # Chỉ cập nhật khi không bị tạm dừng
            self.update_balls()
        if len(self.balls) == 0 and self.number_of_generated == \
                self.number_to_generate:
            self.score_manager.win()

    def draw(self, screen):
        for ball in self.balls:
            ball.draw(screen)

    def get_available_colors(self):
        return [ball.color for ball in self.balls]

    def insert(self, index, shooting_ball):
        # Tạo một quả bóng mới từ shooting_ball
        ball = self.convert_shooting_ball(index, shooting_ball)
        
        # Chèn quả bóng mới vào danh sách balls tại vị trí index + 1
        self.balls.insert(index + 1, ball)
        
        # Điều chỉnh vị trí của các quả bóng phía sau nếu cần
        for i in range(index + 2, len(self.balls)):
            # Nếu khoảng cách giữa hai quả bóng quá nhỏ, dừng việc điều chỉnh
            if self.balls[i].pos_in_path - self.balls[i - 1].pos_in_path >= \
                    2 * BALL_RADIUS // self.path.step:
                break
            # Cập nhật vị trí của quả bóng hiện tại
            self.balls[i].set_position(self.count_next_pos(i - 1))


    def convert_shooting_ball(self, index, shooting_ball):
        ball = Ball(shooting_ball.color,
                    self.count_next_pos(index), self.path)
        ball.can_move = self.balls[index].can_move
        return ball

    def destroy(self, chain):
            # Duyệt qua mỗi quả bóng trong chuỗi chain
        for ball in chain:
            # Xóa quả bóng khỏi danh sách balls
            self.balls.remove(ball)


    def join_balls(self, index):
        for i in range(index, len(self.balls)):
            self.balls[i].set_position(self.count_next_pos(i - 1))

    def stop_balls(self, tail_index):
        for i in range(tail_index, len(self.balls)):
            self.balls[i].can_move = False

    def count_next_pos(self, index):
        return self.balls[index].pos_in_path + 2 * BALL_RADIUS // self.path.step

    def set_pause(self, state):
        self.pause = state  # Cập nhật trạng thái tạm dừng


