import numpy as np



COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0


# don’t change the class name
level_one = 100000
level_higher_two = 35000
level_higher_two1 = 30000
level_higher_two2 = 29000
level_higher_two3 = 28000
level_higher_two4 = 27000
level_higher_two5 = 26000
level_higher_two6 = 25000
level_higher_two7 = 24000
level_higher_two8 = 23000
level_two1 = 10000
level_two2 = 9000
level_three1 = 5000
level_three2 = 4900
level_four1 = 1000
level_four2 = 900
level_higher_five1 = 600
level_higher_five2 = 590
level_five = 500
level_six = 400
level_seven = 100
level_eight = 90
level_nine = 50
level_ten = 10
level_eleven = 9
level_twelve = 5
level_thirteen = 2
level_fourteen = 1

class AI(object):

    # chessboard_size, color, time_out passed from agent              !!!: , time_out
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm’s run time must not exceed t
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get th
        self.candidate_list = []

        self.new_pos = [0, 0]


    def go(self, chessboard):
        self.candidate_list.clear()
        # print(chessboard)
        # print(self.color)
        if self.is_blank(chessboard):
            self.new_pos = [7, 7]
        else:
            self.ai(chessboard)

        assert chessboard[self.new_pos[0], self.new_pos[1]] == 0
        # print(chessboard)
        # print(self.new_pos)
        self.candidate_list.append(self.new_pos)

    def is_blank(self, chessboard):

        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):

                if chessboard[i][j] != 0:
                    return False
        return True

    def generate_kids(self, chessboard):
        kids_list = []
        for i in range(15):
            for j in range(15):
                if chessboard[i][j] == 0 and self.has_neighbor(i, j, chessboard):
                    kids_list.append((i, j))
        return kids_list  # [(x1,y1), (x2,y2), (x3,y3), ...]

    def has_neighbor(self, i, j, chessboard):
        for p in range(-2, 3):
            for q in range(-2, 3):
                if p == 0 and q == 0:
                    continue
                if (i + p) in range(0, 15) and (j + q) in range(0, 15):
                    if chessboard[i + p][j + q] != 0:
                        return True
        return False

    def ai(self, chessboard):
        # print('ai')
        chessboard1 = np.ones((15, 15))
        for i in range(15):
            for j in range(15):
                chessboard1[i][j] = chessboard[i][j]
        self.decide_new_pos(chessboard)

    def decide_new_pos(self, chessboard):
        kids_list = self.generate_kids(chessboard)

        max1 = 0
        max2 = 0

        pos1 = [0, 0]
        pos2 = [0, 0]
        ene_color = 0

        if self.color == COLOR_BLACK:
            ene_color = COLOR_WHITE
        else:
            ene_color = COLOR_BLACK

        mylist = []
        for l in kids_list:
            chessboard[l[0]][l[1]] = self.color  # me

            mylist.append(l)

            score1 = self.evaluate(True, chessboard, mylist)
            if score1 > max1:
                max1 = score1
                pos1[0] = l[0]
                pos1[1] = l[1]
            chessboard[l[0]][l[1]] = 0

        mylist = []
        for l in kids_list:
            chessboard[l[0]][l[1]] = ene_color  # enemy
            mylist.append(l)

            score2 = self.evaluate(False, chessboard, mylist)
            if score2 > max2:
                max2 = score2
                pos2[0] = l[0]
                pos2[1] = l[1]
            chessboard[l[0]][l[1]] = 0

        # if max1 > max2:
        #     self.new_pos = pos1
        # elif max2 > max1:
        #     self.new_pos = pos2
        # elif max1 == max2:
        #     if max1 == 100000:
        #         self.new_pos = pos1
        #     elif max1 >= 4900:
        #         self.new_pos = pos1
        #     elif max2 >= 90:
        #         self.new_pos = pos2
        #     else:
        #         self.new_pos = pos1

        # if max1 >= 4900:
        #     self.new_pos = pos1
        # elif max2 > max1:
        #     self.new_pos = pos2
        # elif max1 == max2:
        #     if max2 >= 90:
        #         self.new_pos = pos2
        #     else:
        #         self.new_pos = pos1
        if max2 == 100000:
            self.new_pos = pos2
        elif max1 >= 10000:
            self.new_pos = pos1
        elif max2 >= 10000:
            self.new_pos = pos2
        elif max1 >= 4900:
            self.new_pos = pos1
        elif max2 >= 4900:
            self.new_pos = pos2
        elif max1 > max2:
            self.new_pos = pos1
        elif max2 > max1:
            self.new_pos = pos2
        elif max1 == max2:
            if max2 >= 90:
                self.new_pos = pos2
            else:
                self.new_pos = pos1

    def evaluate(self, is_me, chessboard, mylist):
        # scoreTabel[15][15]
        # score_tabel = [None] * 15
        #
        # for i in range(len(score_tabel)):
        #     score_tabel[i] = [0] * 15

        # total_score = 0
        # if len(mylist) == 0:
        #     return -99999999

        pos = mylist[-1]
        i = pos[0]
        j = pos[1]

        if is_me:

            color = self.color
        else:
            if self.color == COLOR_BLACK:
                color = COLOR_WHITE
            else:
                color = COLOR_BLACK

        if color == COLOR_BLACK:
            ene_color = COLOR_WHITE
        else:
            ene_color = COLOR_BLACK


        situation = []

        # 竖
        checking = []
        count = 0
        flag = 0
        for x in range(-4, 5):
            if (i + x) in range(0, 15):
                checking.append(chessboard[i + x][j])
                count = count + 1
            if x == 0:
                flag = count - 1

        situation.append(self.one_direction(flag, checking, color, ene_color))

        # 横
        checking = []
        count = 0
        flag = 0
        for y in range(-4, 5):
            if (j + y) in range(0, 15):
                checking.append(chessboard[i][j + y])
                count = count + 1
            if y == 0:
                flag = count - 1

        situation.append(self.one_direction(flag, checking, color, ene_color))

        # 斜1
        checking = []
        count = 0
        flag = 0
        for v in range(-4, 5):
            if (i + v) in range(0, 15) and (j + v) in range(0, 15):
                checking.append(chessboard[i + v][j + v])
                count = count + 1
            if v == 0:
                flag = count - 1

        situation.append(self.one_direction(flag, checking, color, ene_color))

        # 斜2
        checking = []
        count = 0
        flag = 0
        for v in range(-4, 5):
            if (i + v) in range(0, 15) and (j - v) in range(0, 15):
                checking.append(chessboard[i + v][j - v])
                count = count + 1
            if v == 0:
                flag = count - 1

        situation.append(self.one_direction(flag, checking, color, ene_color))

        # 综合四个方向评分：
        if situation.count('win5') >= 1:
            return level_one
        if situation.count('alive4')>=2:
            return level_higher_two
        if situation.count('alive4') >= 1 and situation.count('alive3') >= 1:
            return level_higher_two1
        if situation.count('alive4') >= 1 and situation.count('tiao3') >= 1:
            return level_higher_two2
        if situation.count('alive4') >= 1 and situation.count('die4') >= 1:
            return level_higher_two3

        if situation.count('alive4') >= 1 and situation.count('lowdie4') >= 1:
            return level_higher_two4
        if situation.count('alive4') >= 1 and situation.count('alive2') >= 1:
            return level_higher_two5
        if situation.count(('alive4')) >= 1 and situation.count('lowalive2') >=1:
            return level_higher_two6
        if situation.count('alive4') >= 1 and situation.count('die3') >= 1:
            return level_higher_two7
        if situation.count('alive4') >= 1 and situation.count('die2') >= 1:
            return level_higher_two8
        if situation.count('alive4') >= 1 or situation.count('die4') >= 2 or 
                situation.count('lowdie4')>= 2 or\
                (situation.count('die4')>=1 and situation.count('lowdie4')>=1) or (
                situation.count('die4') >= 1 and situation.count('alive3') >= 1) or (
                situation.count('die4') >= 1 and situation.count('tiao3') >= 1):
            return level_two1#1步必胜
        if (situation.count('lowdie4') >= 1 and situation.count('alive3') >= 1) or 
        (situation.count('lowdie4') >= 1 and situation.count('tiao3') >= 1):
            return level_two2#2步必胜
        if situation.count('alive3') >= 2:
            return level_three1#2步必胜
        if situation.count('alive3') >= 1 and situation.count('tiao3') >= 1:
            return level_three2#2步必胜
        if situation.count('tiao3') >= 2:
            return level_three2#2步必胜

        if situation.count('die3') >=1 and situation.count('die4')>=1:
            return level_four1
        if situation.count('die3') >= 1 and situation.count('alive3') >= 1:
            return level_four2
        if situation.count('die3') >= 1 and situation.count('tiao3') >= 1 :
            return level_four2
        if situation.count('alive3') >= 1 and situation.count('alive2') >=1 :
            return level_higher_five1
        if situation.count('tiao3') >= 1 and situation.count('alive2') >=1 :
            return level_higher_five2
        if situation.count('alive3') >= 1:
            return level_five
        if situation.count('tiao3') >= 1:
            return level_six
        if situation.count('die4') >= 1:
            return level_seven
        if situation.count('lowdie4') >= 1:
            return level_eight
        if situation.count('alive2') >= 2:
            return level_nine
        if situation.count('alive2') >= 1:
            return level_ten
        if situation.count('lowalive2') >= 1:
            return level_eleven
        if situation.count('die3') >= 1:
            return level_twelve
        if situation.count('die2') >= 1:
            return level_thirteen
        return level_fourteen


    # 判断是哪一种棋形
    def one_direction(self, flag, checking, color, ene_color):

        length = len(checking)
        count = 0
        track = []  # 连续棋子在checking中的index
        for i in range(0, 5):
            if (flag - i) >= 0 and checking[flag - i] == color:
                count = count + 1
                track.append(flag - i)
            else:
                break
        for i in range(1, 5):
            if (flag + i) < length and checking[flag + i] == color:
                count = count + 1
                track.append(flag + i)
            else:
                break

        track = np.sort(track)
        if count >= 5:
            return 'win5'
        if count == 4:
            if track[0] - 1 >= 0 and checking[track[0] - 1] == COLOR_NONE and track[-1] + 1 < length and checking[
                track[-1] + 1] == COLOR_NONE:
                return 'alive4'
            elif track[0] - 1 >= 0 and checking[track[0] - 1] == ene_color and track[-1] + 1 < length and checking[
                track[-1] + 1] == ene_color:
                return 'nothreat'
            elif track[0] - 1 < 0 and track[-1] + 1 < length and checking[track[-1] + 1] == ene_color:
                return 'nothreat'
            elif track[-1] + 1 >= length and track[0] - 1 >= 0 and checking[track[0] - 1] == ene_color:
                return 'nothreat'
            elif track[0] - 1 >= 0 and checking[track[0] - 1] == ene_color and track[-1] + 1 < length and checking[
                track[-1] + 1] == COLOR_NONE:
                return 'die4'
            elif track[0] - 1 >= 0 and checking[track[0] - 1] == COLOR_NONE and track[-1] + 1 < length and checking[
                track[-1] + 1] == ene_color:
                return 'die4'
            elif track[0] - 1 < 0 and track[-1] + 1 < length and checking[track[-1] + 1] == COLOR_NONE:
                return 'die4'
            elif track[-1] + 1 >= length and track[0] - 1 >= 0 and checking[track[0] - 1] == COLOR_NONE:
                return 'die4'

        if count == 3:
            # 连3两边均空
            if track[0] - 1 >= 0 and checking[track[0] - 1] == COLOR_NONE and track[-1] + 1 < length and checking[
                track[-1] + 1] == COLOR_NONE:
                if track[0] - 2 >= 0 and checking[track[0] - 2] == ene_color and track[-1] + 2 < length and checking[
                    track[-1] + 2] == ene_color:
                    return 'die3'
                elif track[0] - 2 < 0 and track[-1] + 2 < length and checking[track[-1] + 2] == ene_color:
                    return 'die3'
                elif track[0] - 2 >= 0 and checking[track[0] - 2] == ene_color and track[-1] + 2 >= length:
                    return 'die3'
                elif track[0] - 2 >= 0 and checking[track[0] - 2] == color:
                    return 'lowdie4'
                elif track[-1] + 2 < length and checking[track[-1] + 2] == color:
                    return 'lowdie4'
                elif track[0] - 2 >= 0 and checking[track[0] - 2] == COLOR_NONE:
                    return 'alive3'
                elif track[-1] + 2 < length and checking[track[-1] + 2] == COLOR_NONE:
                    return 'alive3'
            # 连3两边均非空
            elif track[0] - 1 >= 0 and checking[track[0] - 1] == ene_color and track[-1] + 1 < length and checking[
                track[-1] + 1] == ene_color:
                return 'nothreat'
            elif track[0] - 1 < 0 and track[-1] + 1 < length and checking[track[-1] + 1] == ene_color:
                return 'nothreat'
            elif track[0] - 1 >= 0 and checking[track[0] - 1] == ene_color and track[-1] + 1 >= length:
                return 'nothreat'
            # 连3两边只有一个为空
            # 右边被堵住：
            elif track[0] - 1 >= 0 and checking[track[0] - 1] == COLOR_NONE:
                if (track[0] - 2 >= 0 and checking[track[0] - 2] == ene_color) or track[0] - 2 < 0:
                    return 'nothreat'
                if track[0] - 2 >= 0 and checking[track[0] - 2] == COLOR_NONE:
                    return 'die3'
                if track[0] - 2 >= 0 and checking[track[0] - 2] == color:
                    return 'lowdie4'

            # 左边被堵住：
            elif track[-1] + 1 < length and checking[track[-1] + 1] == COLOR_NONE:
                if (track[-1] + 2 < length and checking[track[-1] + 2] == ene_color) or track[-1] + 2 >= length:
                    return 'nothreat'
                if track[-1] + 2 < length and checking[track[-1] + 2] == COLOR_NONE:
                    return 'die3'
                if track[-1] + 2 < length and checking[track[-1] + 2] == color:
                    return 'lowdie4'

        if count == 2:
            # 连2两边均空
            if track[0] - 1 >= 0 and checking[track[0] - 1] == COLOR_NONE and track[-1] + 1 < length and checking[
                track[-1] + 1] == COLOR_NONE:
                if track[0] - 3 >= 0 and checking[track[0] - 2] == COLOR_NONE and checking[track[0] - 3] == color:
                    return 'die3'
                if track[-1] + 3 < length and checking[track[-1] + 2] == COLOR_NONE and checking[
                    track[-1] + 3] == color:
                    return 'die3'
                if track[0] - 2 >= 0 and checking[track[0] - 2] == COLOR_NONE and track[-1] + 2 < length and checking[
                    track[-1] + 2] == COLOR_NONE:
                    return 'alive2'
                if track[0] - 3 >= 0 and checking[track[0] - 2] == color and  checking[
                    track[0] - 3] == ene_color:
                    return 'die3'
                if track[-1] + 3 < length and checking[track[-1] + 2] == color and checking[
                    track[-1] + 3] == ene_color:
                    return 'die3'
                if track[0] - 3 >= 0 and checking[track[0] - 2] == color and checking[
                    track[0] - 3] == color:
                    return 'lowdie4'
                if track[-1] + 3 < length and checking[track[-1] + 3] == color  and checking[
                    track[-1] + 2] == color:
                    return 'lowdie4'
                if track[0] - 3 >= 0 and checking[track[0] - 2] == color and checking[track[0] - 3] == COLOR_NONE:
                    return 'tiao3'
                if track[-1] +3 < length and checking[track[-1] + 3] == COLOR_NONE and  checking[
                    track[-1] + 2] == color:
                    return 'tiao3'
            # 连2两边均非空
            elif track[0] - 1 >= 0 and checking[track[0] - 1] == ene_color and track[-1] + 1 < length and checking[
                track[-1] + 1] == ene_color:
                return 'nothreat'
            elif track[0] - 1 >= 0 and checking[track[0] - 1] == ene_color and track[-1] + 1 >= length:
                return 'nothreat'
            elif track[-1] + 1 < length and checking[track[-1] + 1] == ene_color and track[0] - 1 < 0:
                return 'nothreat'

            # 连2两边只有一个为空
            # 右边被堵住
            elif track[0] - 1 >= 0 and checking[track[0] - 1] == COLOR_NONE:
                if track[0] - 2 >= 0 and checking[track[0] - 2] == ene_color:
                    return 'nothreat'
                elif track[0] - 3 >= 0 and checking[track[0] - 3] == ene_color:
                    return 'nothreat'
                elif track[0] - 3 >= 0 and checking[track[0] - 2] == COLOR_NONE and checking[
                    track[0] - 3] == COLOR_NONE:
                    return 'die2'
                elif track[0] - 3 >= 0 and checking[track[0] - 2] == color and checking[track[0] - 3] == color:
                    return 'lowdie4'
                elif track[0] - 3 >= 0 and checking[track[0] - 2] == color and checking[track[0] - 3] == COLOR_NONE:
                    return 'die3'
                elif track[0] - 3 >= 0 and checking[track[0] - 3] == color and checking[track[0] - 2] == COLOR_NONE:
                    return 'die3'
            # 左边被堵住
            elif track[-1] + 1 < length and checking[track[-1] + 1] == COLOR_NONE:
                if track[-1] + 2 < length and checking[track[-1] + 2] == ene_color:
                    return 'nothreat'
                elif track[-1] + 3 < length and checking[track[-1] + 3] == ene_color:
                    return 'nothreat'
                elif track[-1] + 3 < length and checking[track[-1] + 2] == COLOR_NONE and checking[
                    track[-1] + 3] == COLOR_NONE:
                    return 'die2'
                elif track[-1] + 3 < length and checking[track[-1] + 2] == color and checking[track[-1] + 3] == color:
                    return 'lowdie4'
                elif track[-1] + 3 < length and checking[track[-1] + 2] == color and checking[track[-1] + 3] == COLOR_NONE:
                    return 'die3'
                elif track[-1] + 3 < length and checking[track[-1] + 2] == COLOR_NONE and checking[track[-1] + 3] == color:
                    return 'die3'

        if count == 1:
            if track[0] - 4 >= 0 and checking[track[0] - 1] == COLOR_NONE and checking[track[0] - 2] == color and \
                    checking[track[0] - 3] == color and checking[track[0] - 4] == color:
                return 'lowdie4'
            if track[-1] + 4 < length and checking[track[-1] + 1] == COLOR_NONE and checking[track[-1] + 2] == color and \
                    checking[track[-1] + 3] == color and checking[track[-1] + 4] == color:
                return 'lowdie4'
            if track[0] - 4 >= 0 and track[-1] + 1 < length and checking[track[0] - 1] == COLOR_NONE and checking[
                track[0] - 2] == color and checking[track[0] - 3] == color and checking[track[0] - 4] == COLOR_NONE and \
                    checking[track[-1] + 1] == COLOR_NONE:
                return 'tiao3'
            if track[-1] + 4 < length and track[0] - 1 >= 0 and checking[track[-1] + 1] == COLOR_NONE and checking[
                track[-1] + 2] == color and checking[track[-1] + 3] == color and checking[
                track[-1] + 4] == COLOR_NONE and checking[track[0] - 1] == COLOR_NONE:
                return 'tiao3'
            if track[0] - 4 >= 0 and track[-1] + 1 < length and checking[track[0] - 1] == COLOR_NONE and checking[
                track[0] - 2] == color and checking[track[0] - 3] == color and checking[track[0] - 4] == ene_color and \
                    checking[track[-1] + 1] == COLOR_NONE:
                return 'die3'
            if track[-1] + 4 < length and track[0] - 1 >= 0 and checking[track[-1] + 1] == COLOR_NONE and checking[
                track[-1] + 2] == color and checking[track[-1] + 3] == color and checking[
                track[-1] + 4] == ene_color and checking[track[0] - 1] == COLOR_NONE:
                return 'die3'
            if track[0] - 4 >= 0 and checking[track[0] - 1] == COLOR_NONE and checking[track[0] - 2] == COLOR_NONE and \
                    checking[track[0] - 3] == color and checking[track[0] - 4] == color:
                return 'die3'
            if track[-1] + 4 < length and checking[track[-1] + 1] == COLOR_NONE and checking[
                track[-1] + 2] == COLOR_NONE and checking[track[-1] + 3] == color and checking[track[-1] + 4] == color:
                return 'die3'
            if track[0] - 4 >= 0 and checking[track[0] - 1] == COLOR_NONE and checking[track[0] - 2] == color and \
                    checking[track[0] - 3] == COLOR_NONE and checking[track[0] - 4] == color:
                return 'die3'
            if track[-1] + 4 < length and checking[track[-1] + 1] == COLOR_NONE and checking[track[-1] + 2] == color and \
                    checking[track[-1] + 3] == COLOR_NONE and checking[track[-1] + 4] == color:
                return 'die3'
            if track[0] - 4 >= 0 and track[-1] + 1 < length and checking[track[0] - 1] == COLOR_NONE and checking[
                track[0] - 2] == color and checking[track[0] - 3] == COLOR_NONE and checking[
                track[0] - 4] == COLOR_NONE and checking[track[-1] + 1] == COLOR_NONE:
                return 'lowalive2'
            if track[-1] + 4 < length and track[0] - 1 >= 0 and checking[track[-1] + 1] == COLOR_NONE and checking[
                track[-1] + 2] == color and checking[track[-1] + 3] == COLOR_NONE and checking[
                track[-1] + 4] == COLOR_NONE and checking[track[0] - 1] == COLOR_NONE:
                return 'lowalive2'
            if track[0] - 4 >= 0 and track[-1] + 1 < length and checking[track[0] - 1] == COLOR_NONE and checking[
                track[0] - 2] == COLOR_NONE and checking[track[0] - 3] == color and checking[
                track[0] - 4] == COLOR_NONE and checking[track[-1] + 1] == COLOR_NONE:
                return 'lowalive2'
            if track[-1] + 4 < length and track[0] - 1 >= 0 and checking[track[-1] + 1] == COLOR_NONE and checking[
                track[-1] + 2] == COLOR_NONE and checking[track[-1] + 3] == color and checking[
                track[-1] + 4] == COLOR_NONE and checking[track[0] - 1] == COLOR_NONE:
                return 'lowalive2'

        return 'nothreat'
