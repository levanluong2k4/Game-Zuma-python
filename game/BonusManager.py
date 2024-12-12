import datetime
import random
from enum import Enum


class Bonus(Enum):
    Pause = 0
    Reverse = 1
    Bomb = 2
    Speed = 3


class BonusManager:
    def __init__(self, ball_generator):
        self.ball_generator = ball_generator
        self.bonuses = [Bonus.Pause, Bonus.Reverse, Bonus.Bomb, Bonus.Speed]
        self.game_start_time = datetime.datetime.now()
        self.pause_start_time = None
        self.reverse_start_time = None
        self.speed_start_time = None
        self.balls_with_bonuses = []

    def start_bonus(self, bonus):
        # Nếu bonus là Pause
        if bonus is Bonus.Pause:
            # Gọi phương thức start_pause để xử lý pause
            self.start_pause()
        # Nếu bonus là Reverse
        elif bonus is Bonus.Reverse:
            # Gọi phương thức start_reverse để xử lý reverse
            self.start_reverse()
        # Nếu bonus là Speed
        elif bonus is Bonus.Speed:
            # Gọi phương thức start_speed để xử lý speed
            self.start_speed()


    def start_speed(self):
        self.speed_start_time = datetime.datetime.now()

    def start_reverse(self):
        self.reverse_start_time = datetime.datetime.now()
        self.ball_generator.reverse = True

    def start_pause(self):
        self.pause_start_time = datetime.datetime.now()
        self.ball_generator.pause = True

    def stop_reverse(self):
        self.reverse_start_time = None
        self.ball_generator.reverse = False

    def stop_pause(self):
        self.pause_start_time = None
        self.ball_generator.pause = False

    def stop_speed(self):
        self.speed_start_time = None

    def handle_reverse_bonus(self):
        # Nếu reverse_start_time không phải là None (tức là đã bắt đầu reverse)
        if self.reverse_start_time is not None:
            # Nếu thời gian trôi qua kể từ reverse_start_time ít hơn 4 giây
            if (datetime.datetime.now() - self.reverse_start_time).seconds < 4:
                # Di chuyển tất cả các viên bóng lùi lại
                self.move_balls_back()
            else:
                # Dừng chức năng reverse
                self.stop_reverse()


    def move_balls_back(self):
        for i in range(len(self.ball_generator.balls)):
            self.ball_generator.balls[i].move(-1)

    def handle_pause_bonus(self):
        # Nếu pause_start_time không phải là None (tức là đã bắt đầu pause)
        if self.pause_start_time is not None:
            # Nếu thời gian trôi qua kể từ pause_start_time đạt 5 giây
            if (datetime.datetime.now() - self.pause_start_time).seconds == 3:
                # Dừng chức năng pause
                self.stop_pause()


    def handle_speed_bonus(self):
        if self.speed_start_time is None or (datetime.datetime.now() -
                                             self.speed_start_time).seconds == 5:
            self.stop_speed()
            return False
        return True

    def handle_bomb_bonus(self, chain):
        # Lấy chỉ số của đuôi và đầu chuỗi
        chain_tail = self.ball_generator.balls.index(chain[0]) - 1
        chain_head = self.ball_generator.balls.index(chain[-1]) + 1

        result_chain = []

        # Thêm 3 viên bóng trước đuôi chuỗi vào result_chain
        for _ in range(3):
            if chain_tail < 0:
                break
            result_chain.append(self.ball_generator.balls[chain_tail])
            chain_tail -= 1

        # Thêm 3 viên bóng sau đầu chuỗi vào result_chain
        for _ in range(3):
            if chain_head > len(self.ball_generator.balls) - 1:
                break
            result_chain.append(self.ball_generator.balls[chain_head])
            chain_head += 1

        # Trả về chuỗi kết quả
        return result_chain


    def update(self):
        self.handle_reverse_bonus()
        self.handle_pause_bonus()
        self.update_balls_with_bonuses()
        self.generate_bonus()

    def generate_bonus(self):
            # Lấy thời gian hiện tại
        cur_time = datetime.datetime.now()
        
        # Nếu thời gian đã trôi qua 15 giây kể từ khi bắt đầu trò chơi
        if (cur_time - self.game_start_time).seconds == 15:
            # Chọn một viên bóng ngẫu nhiên từ ball_generator.balls
            ball_with_bonus = random.choice(self.ball_generator.balls)
            
            # Chọn một bonus ngẫu nhiên từ danh sách bonus
            bonus = random.choice(self.bonuses)
            
            # Gán bonus cho viên bóng đã chọn
            ball_with_bonus.set_bonus(bonus)
            
            # Thêm viên bóng và thời gian hiện tại vào danh sách balls_with_bonuses
            self.balls_with_bonuses.append((ball_with_bonus, cur_time))
            
            # Cập nhật lại game_start_time bằng thời gian hiện tại
            self.game_start_time = cur_time


    def update_balls_with_bonuses(self):
        for ball, time in self.balls_with_bonuses:
            if (datetime.datetime.now() - time).seconds == 15:
                ball.set_bonus(None)
