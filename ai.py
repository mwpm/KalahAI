import time
import random 
import io


class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

TOTAL_STONES = 72
PLAYER_HOLES = 6
PLAYER_SCORE_HOLE = 7

class ai:
    evaluation_value_list = []

    def __init__(self):
        pass

    class State(object):
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately 
    def move(self, a, b, a_fin, b_fin, t):
        t_start = time.time()
        move = self.minimax(9, self.State(a, b, a_fin, b_fin))
        #print(str(time.time()-t_start))
        return move

    # calling function
    def minimax(self, depth, current_state):
        # Setup:
        alpha = -1000    # Highest Value on path
        beta = "inf"     # Lowest Value on path

        # Get best move:
        best_evaluation = self.max_val(depth, current_state, alpha, beta)
        #print(best_evaluation)
        #print(self.evaluation_value_list)
        for index in range(len(self.evaluation_value_list)):
            if self.evaluation_value_list[index] == best_evaluation:
                return index

    # Returns the largest utility value of a given state
    def max_val(self, depth, current_state, alpha, beta):
        if self.is_game_over(depth, current_state):
            final_evaluation_value = self.evaluate_state(current_state)
            return final_evaluation_value

        eval_list = []

        min_value = -1000
        evaluation_value = -1000
        for index in range(len(current_state.a)):
            if current_state.a[index] > 0:
                next_state, extra_turn = self.calculate_move(index, current_state)
                if extra_turn:
                    max_value = self.max_val(depth - 1, next_state, alpha, beta)
                    evaluation_value = max(evaluation_value, max_value)
                else:
                    min_value = self.min_val(depth - 1, next_state, alpha, beta)
                    evaluation_value = max(evaluation_value, min_value)
                eval_list.append(evaluation_value)

                # Check cutoff
                if evaluation_value >= beta:
                    return evaluation_value
                alpha = max(alpha, evaluation_value)

            else:
                eval_list.append(-1000)

        self.evaluation_value_list = eval_list
        return evaluation_value

    # Returns the smallest utility value possible for the given state
    def min_val(self, depth, current_state, alpha, beta):
        if self.is_game_over(depth, current_state):
            final_evaluation_value = self.evaluate_state(current_state)
            return final_evaluation_value

        evaluation_value = "inf"
        max_value = "inf"
        for index in range(len(current_state.a)):
            if depth != 0 and current_state.a[index] > 0:
                next_state, extra_turn = self.calculate_move(index, current_state)
                if extra_turn:
                    min_value = self.min_val(depth - 1, next_state, alpha, beta)
                    evaluation_value = min(evaluation_value, min_value)
                else:
                    max_value = self.max_val(depth - 1, next_state, alpha, beta)
                    evaluation_value = min(evaluation_value, max_value)

                # Check cutoff
                if evaluation_value <= alpha:
                    return evaluation_value
                beta = min(beta, evaluation_value)

        return evaluation_value

    # Evaluates the given state using a heuristic evaluation function and returns the evaluation value of the function
    @staticmethod
    def evaluate_state(state):
        # Compare current scores of each player
        evaluation_value = state.a_fin - state.b_fin
        defensive_scalar = 1
        offensive_scalar = 1
        if state.b_fin > 36 - 5:
            defensive_scalar = state.b_fin - 31

        if state.a_fin > 36 - 5:
            offensive_scalar = state.a_fin - 31

        # Calculate how many stones are available:
        available_stones = TOTAL_STONES - state.a_fin - state.b_fin

        for index in range(len(state.b)):
            # Evaluate empty holes
            # Defensive:
            if state.b[index] == 0:
                evaluation_value -= state.a[5 - index]

                for inside in range(len(state.b)):
                    value = state.b[inside]
                    if value == 13 - inside and inside > index or value == index - inside:
                        evaluation_value -= (state.a[5 - index] + 1) * defensive_scalar

            # Better score if you can get another turn
            if (state.a[index] % 13) == 6 - index:
                evaluation_value += 10 * defensive_scalar
        return evaluation_value

    # Returns True if the game is over or the tree has reached the max depth, else False
    def is_game_over(self, depth, state):
        if depth <= 0 or (not self.available_moves(state)):
            return True
        else:
            return False

    # Returns true if the player has available moves
    @staticmethod
    def available_moves(state):
        for value in state.a:
            if value > 0:
                return True
        return False

    # Returns a new state based on the move passed.
    def calculate_move(self, index, current_state):
        count = current_state.a[index]
        extra_turn = False

        combined = current_state.a + [current_state.a_fin]
        combined += current_state.b

        # Update Board
        combined[index] = 0
        while count != 0:
            count -= 1
            index += 1
            if index > 12:
                index = 0
            combined[index] += 1

        # Check end case:
        # Empty Spot:
        if index < 6 and combined[index] == 1:
            combined[6] += combined[12 - index]
            combined[12 - index] = 0
        # Extra Turn:
        elif index == 6:
            extra_turn = True

        new_state = self.State(combined[0:6], combined[7:13], combined[6], current_state.b_fin)

        return new_state, extra_turn







