from game.Sprites import ShootingBall
from game.Params import *
from game.BonusManager import Bonus
import random
import datetime


class ShootingManager:
    def __init__(self, ball_generator, pos, bonus_manager, score_manager):
        self.ball_generator = ball_generator
        self.bonus_manager = bonus_manager
        self.score_manager = score_manager

        self.pos = pos
        self.charged_ball = ShootingBall(random.choice(
            self.ball_generator.colors), self.pos)

        self.shooting_balls = []

        self.combo_chain = []

        self.speed = False

    def shoot(self, target):
        # Nếu danh sách bóng bắn hiện tại trống HOẶC tốc độ tăng (speed) là True 
    # HOẶC thời gian hồi chiêu (cooldown) đã kết thúc
        if len(self.shooting_balls) == 0 or self.speed or \
                (datetime.datetime.now() - 
                self.shooting_balls[-1].time).microseconds > 300000:
            
            # Lấy bóng sẵn sàng bắn từ bóng nạp hiện tại (charged_ball)
            shooting_ball = self.charged_ball
            
            # Đặt mục tiêu bắn cho bóng
            shooting_ball.set_target(target)
            
            # Đặt thời gian bắn là thời điểm hiện tại
            shooting_ball.set_time(datetime.datetime.now())
            
            # Nạp bóng mới để sẵn sàng cho lần bắn kế tiếp
            self.charged_ball = self.recharge()
            
            # Thêm bóng vừa bắn vào danh sách bóng đang bắn
            self.shooting_balls.append(shooting_ball)


    def recharge(self):
        # Tạo bóng bắn mới (ShootingBall) với màu sắc ngẫu nhiên từ các màu có sẵn
    # Vị trí khởi tạo của bóng mới là tại vị trí hiện tại của người chơi (self.pos)
        return ShootingBall(random.choice(
            self.ball_generator.get_available_colors()), self.pos)


    def draw(self, screen):
        self.charged_ball.draw(screen)
        for ball in self.shooting_balls:
            ball.draw(screen)

    def update(self):
            # Cập nhật trạng thái tăng tốc (speed) dựa trên các hiệu ứng từ bonus_manager
        self.speed = self.bonus_manager.handle_speed_bonus()
        # Cập nhật trạng thái của bóng đã nạp (charged_ball)
        self.charged_ball.update()
        # Duyệt qua danh sách các bóng đang bắn (shooting_balls)
        for ball in self.shooting_balls:
            # Cập nhật trạng thái của từng bóng
            ball.update()
            # Kiểm tra và loại bỏ bóng đã bay ra khỏi màn hình
            self.remove_flown_away(ball)
            # Xử lý việc bắn bóng (kiểm tra va chạm và các hiệu ứng khác)
            self.handle_shoot(ball)


    def remove_flown_away(self, ball):
            # Lấy tọa độ x của tâm hình chữ nhật (rect)
        x = ball.rect.center[0]
        # Lấy tọa độ y của tâm hình chữ nhật (rect)
        y = ball.rect.center[1]
        # Nếu x hoặc y vượt ra khỏi giới hạn màn hình
        if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            # Xóa bóng khỏi danh sách bóng đang bắn (shooting_balls)
            self.shooting_balls.remove(ball)


    def handle_shoot(self, shooting_ball):
        # Duyệt qua từng quả bóng trong danh sách balls của ball_generator
        for ball in self.ball_generator.balls:
            # Nếu shooting_ball va chạm với quả bóng hiện tại
            if shooting_ball.rect.colliderect(ball.rect):
                # Thu thập chuỗi các quả bóng có cùng màu với shooting_ball
                chain = self.collect_chain(ball, shooting_ball.color)
                
                # Nếu chuỗi có độ dài lớn hơn 1 (có ít nhất 2 quả bóng cùng màu)
                if len(chain) > 1:
                    # Thêm các phần thưởng vào chuỗi nếu có
                    chain += self.check_for_bonus(chain)
                    
                    # Cộng điểm cho người chơi (10 điểm mỗi quả bóng trong chuỗi)
                    self.score_manager.add_score(10 * len(chain))
                    
                    # Loại bỏ các quả bóng trong chuỗi khỏi ball_generator
                    self.ball_generator.destroy(chain)
                    
                    # Nếu màu của shooting_ball không có trong danh sách màu có sẵn
                    if self.charged_ball.color not in \
                            self.ball_generator.get_available_colors() and \
                            len(self.ball_generator.balls) != 0:
                        # Nạp lại shooting_ball với màu mới
                        self.charged_ball = self.recharge()
                else:
                    # Chèn shooting_ball vào danh sách balls tại vị trí của quả bóng hiện tại
                    ball_index = self.ball_generator.balls.index(ball)
                    self.ball_generator.insert(ball_index, shooting_ball)
                
                # Loại bỏ shooting_ball khỏi danh sách shooting_balls
                self.shooting_balls.remove(shooting_ball)
                
                # Dừng vòng lặp
                break


    def check_for_bonus(self, chain):
        for ball in chain:
            if ball.bonus is not None:
                if ball.bonus is Bonus.Bomb:
                    return self.bonus_manager.handle_bomb_bonus(chain)
                elif ball.bonus is Bonus.Speed:
                    self.speed = True
                    self.bonus_manager.start_bonus(ball.bonus)
                else:
                    self.bonus_manager.start_bonus(ball.bonus)
        return []

    def collect_chain(self, ball, color):
            # ball_index = Lấy chỉ số của quả bóng hiện tại trong danh sách balls
        ball_index = self.ball_generator.balls.index(ball)
        
        # ball_color = Lấy màu của quả bóng hiện tại
        ball_color = ball.color

        # left_half = collect_half_chain(ball_index - 1, -1, color)
        # (Thu thập nửa chuỗi bên trái từ chỉ số ball_index - 1, tìm kiếm màu giống)
        left_half = self.collect_half_chain(ball_index - 1, -1, color)
        
        # right_half = collect_half_chain(ball_index + 1, 1, color)
        # (Thu thập nửa chuỗi bên phải từ chỉ số ball_index + 1, tìm kiếm màu giống)
        right_half = self.collect_half_chain(ball_index + 1, 1, color)

        # if ball_color == color:
        # Kiểm tra nếu màu của quả bóng hiện tại giống với màu yêu cầu
        if ball_color == color:
            # chain = left_half + [self.ball_generator.balls[ball_index]] + right_half
            # (Ghép nửa chuỗi bên trái, quả bóng hiện tại và nửa chuỗi bên phải lại với nhau)
            chain = left_half + [self.ball_generator.balls[ball_index]] + right_half
            
            # chain.sort(key=lambda ball: ball.pos_in_path)
            # (Sắp xếp chuỗi các quả bóng theo vị trí của chúng trong đường đi)
            chain.sort(key=lambda ball: ball.pos_in_path)
            
            # return chain
            # (Trả về chuỗi các quả bóng đã thu thập và sắp xếp)
            return chain

        # return right_half
        # (Nếu không, chỉ trả về nửa chuỗi bên phải)
        return right_half

    
    '''
    collect_half_chain(ball_index - 1, -1, color): 
    Gọi hàm này thu thập các quả bóng ở bên trái của quả bóng bắt đầu ( ball_index - 1) trong danh sách, di chuyển ngược lại trong danh sách (do đó có kích thước bước -1), cho đến khi nó gặp một quả bóng không khớp với color. Bộ sưu tập này được lưu trữ trong left_half.
    collect_half_chain(ball_index + 1, 1, color): 
    Hàm gọi này thu thập các quả bóng ở bên phải quả bóng bắt đầu ( ball_index + 1), di chuyển về phía trước trong danh sách (kích thước bước 1), cho đến khi gặp một quả bóng không khớp với color. Bộ sưu tập này được lưu trữ trong right_half.
    
    Nếu bạn thu thập quả bóng từ bên trái (left_half) và từ bên phải (right_half), các quả bóng trong chuỗi có thể bị lộn xộn theo thứ tự mà chúng xuất hiện trên đường đi.
ball.pos_in_path là một thuộc tính thể hiện vị trí của quả bóng trong con đường, vì vậy khi bạn sắp xếp chuỗi bóng theo ball.pos_in_path, bạn đang đảm bảo rằng các quả bóng trong chuỗi được sắp xếp đúng theo thứ tự của chúng dọc theo con đường.
    
    '''
    def collect_half_chain(self, i, delta, color):
        half_chain = []
        while len(self.ball_generator.balls) > i >= 0 and \
                self.ball_generator.balls[i].color == color:
            half_chain.append(self.ball_generator.balls[i])
            i += delta

        return half_chain

    '''
    Hàm collect_half_chain:
Hàm này chỉ thu thập các quả bóng có màu giống nhau ở một phía của quả bóng hiện tại (hoặc bên trái, hoặc bên phải của quả bóng bắt đầu).

Ví dụ:
Nếu bạn muốn thu thập các quả bóng có màu giống nhau ở phía trái của quả bóng hiện tại, bạn sẽ gọi collect_half_chain với delta = -1.
Nếu bạn muốn thu thập các quả bóng có màu giống nhau ở phía phải, bạn sẽ gọi collect_half_chain với delta = 1.
2. Hàm collect_chain:
Hàm collect_chain sử dụng hàm collect_half_chain để thu thập các quả bóng ở cả hai phía của quả bóng bắt đầu, tức là cả phía trái và phải.

Đầu tiên, nó gọi collect_half_chain với delta = -1 để thu thập các quả bóng bên trái của quả bóng hiện tại.
Sau đó, nó gọi collect_half_chain với delta = 1 để thu thập các quả bóng bên phải của quả bóng hiện tại.
Cuối cùng, nó kết hợp các quả bóng thu thập được từ hai phía và sắp xếp chúng theo thứ tự vị trí trong chuỗi.
    '''