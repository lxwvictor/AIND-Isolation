"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    """
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 3*opp_moves)
    """
    nboffsets=[(i,j) for i in range(-2,3) for j in range(-2,3) if abs(i) + abs(j) != 0]
    curloc = game.__last_player_move__[player]
    curopploc = game.__last_player_move__[game.get_opponent(player)]
    emptynb_count = 0
    emptyoppnb_count = 0
    for offset in nboffsets:
        if player.time_left() < player.TIMER_THRESHOLD:
            raise Timeout()
        nb = tuple(map(lambda x, y: x + y, offset, curloc))
        oppnb = tuple(map(lambda x, y: x + y, offset, curopploc))
        if 0 <= nb[0] < game.height and \
            0 <= nb[1] < game.width and \
            nb in game.get_blank_spaces():
                emptynb_count += 1

        if 0 <= oppnb[0] < game.height and \
            0 <= oppnb[1] < game.width and \
            oppnb in game.get_blank_spaces():
                emptyoppnb_count += 1

    return float(emptynb_count - emptyoppnb_count)
    """
    nboffsets=[(i,j) for i in range(-2,3) for j in range(-2,3) if abs(i) + abs(j) != 0]
    curloc = game.__last_player_move__[player]
    emptynb_count = 0
    for offset in nboffsets:
        if player.time_left() < player.TIMER_THRESHOLD:
            raise Timeout()
        nb = tuple(map(lambda x, y: x + y, offset, curloc))
        if 0 <= nb[0] < game.height and \
            0 <= nb[1] < game.width and \
            nb in game.get_blank_spaces():
                emptynb_count += 1

    return float(emptynb_count)
    """
    raise NotImplementedError


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=15.):
        # timeout of 10 should be enough to allow the program to abort and 
        # raise the Timeout event. Current state will be aborted and return the
        # last known state/move to the calling function. Thus in both the
        # max_search() and min_search() functions there is a timeout check.
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        # The self.time_left is a function, use self.time_left() to know how many
        # miliseconds left, the initial value was passed from the calling
        # function which made the player to start move. 150 from tounament.py.
        # 99 from agent_test.py
        self.time_left = time_left
        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        if (not legal_moves) or self.search_depth == 0:
            return (-1,1)
        best_value = None
        best_move = None
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.method == "minimax":
                if self.iterative == True:
                    depth = 0
                    while True:
                        depth += 1
                        best_value, best_move = self.minimax(game, depth)
                        pass
                else:
                    best_value, best_move = self.minimax(game, self.search_depth)
                return best_move
            elif self.method == "alphabeta":
                if self.iterative == True:
                    depth = 0
                    while True:
                        depth += 1
                        best_value, best_move = self.alphabeta(game, depth)
                        pass
                else:
                    best_value, best_move = self.alphabeta(game, self.search_depth)
                return best_move

            pass

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move
            pass

        raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if (not game.get_legal_moves()) or self.search_depth == 0:
            return (-1,-1)

        def max_search(self, game, depth, cur_depth):
            """ Implemente the max search algorithm. Need to be clear about
                the terminal state and recursion state.

            Parameters
            ----------
            game : isolation.Board
            depth: int
            cur_depth: int
                The current depth of the node, starting from 0

            Returns
            -------
            float: the score
            tuple(int, int): The best move of the branch

            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            cur_depth += 1
            legal_moves = game.get_legal_moves()

            # If we can judge the winner at the current state, then just return
            # the score and active player's current position
            if game.is_loser(self):
                return float("-inf"), game.get_player_location(game.active_player)

            if game.is_winner(self):
                return float("inf"), game.get_player_location(game.active_player)

            # Get the max from all the min nodes. The score value is initialized
            # as negative infinity. Then for each possible move m, get the
            # return value (the first element of the tuple) and compare with
            # the current value until all child nodes searched and the max,
            # together with the move will be returned.
            # 
            # Below is another way to implement, but the readiably is really
            # lousy!
            # 
            # #(value, _), move = max([(min_search(self, game.forecast_move(m), depth, cur_depth), m)
            #    for m in legal_moves])
            value = float("-inf")
            move = (-1,-1)

            for m in legal_moves:
                if cur_depth == depth: 
                    # This is the terminal state when current depth is the
                    # defined depth
                    score_value = self.score(game.forecast_move(m), self)
                else:
                    # Go to min branch if not in leaf node
                    score_value = min_search(self, game.forecast_move(m),
                        depth, cur_depth)[0]

                # Find the max value
                if score_value > value:
                        value = score_value
                        move = m

            return value, move

        def min_search(self, game, depth, cur_depth):
            """ Implemente the min search algorithm. Need to be clear about
                the terminal state and recursion state.

            Parameters
            ----------
            game : isolation.Board
            depth: int
            cur_depth: int
                The current depth of the node, starting from 0

            Returns
            -------
            float: the score
            tuple(int, int): The best move of the branch

            """

            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            cur_depth += 1
            legal_moves = game.get_legal_moves()

            # If we can judge the winner at the current state, then just return
            # the score and active player's current position
            if game.is_loser(self):
                return float("-inf"), game.get_player_location(game.active_player)

            if game.is_winner(self):
                return float("inf"), game.get_player_location(game.active_player)

            # Get the min from all the max nodes. The score value is initialized
            # as positive infinity. Then for each possible move m, get the
            # return value (the first element of the tuple) and compare with
            # the current value until all child nodes searched and the min,
            # together with the move will be returned.
            # 
            # Below is another way to implement, but the readiably is really
            # lousy!
            # 
            #(value, _), move = min([(max_search(self, game.forecast_move(m), depth, cur_depth), m)
            #    for m in legal_moves])
            value = float("inf")
            move = (-1,-1)

            for m in legal_moves:
                if cur_depth == depth:
                    # This is the terminal state when current depth is the
                    # defined depth
                    score_value = self.score(game.forecast_move(m), self)
                else:
                    # Go to max branch if not in leaf node
                    score_value = max_search(self, game.forecast_move(m), 
                        depth, cur_depth)[0]

                # Find the min value
                if score_value < value:
                        value = score_value
                        move = m

            return value, move

        # TODO: finish this function!
        if maximizing_player:
            return max_search(self, game, depth, 0)
        else:
            return min_search(self, game, depth, 0)
        raise NotImplementedError

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        if (not game.get_legal_moves()) or self.search_depth == 0:
            return (-1,-1)

        def max_search(self, game, depth, cur_depth, myalpha, mybeta):
            """ Implemente the max search algorithm. Need to be clear about
                the terminal state and recursion state.

            Parameters
            ----------
            game : isolation.Board
            depth: int
            cur_depth: int
                The current depth of the node, starting from 0

            Returns
            -------
            float: the score
            tuple(int, int): The best move of the branch

            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            cur_depth += 1
            legal_moves = game.get_legal_moves()

            # If we can judge the winner at the current state, then just return
            # the score and active player's current position
            if game.is_loser(self):
                return float("-inf"), game.get_player_location(game.active_player)

            if game.is_winner(self):
                return float("inf"), game.get_player_location(game.active_player)

            # Get the max from all the min nodes. The score value is initialized
            # as negative infinity. Then for each possible move m, get the
            # return value (the first element of the tuple) and compare with
            # the current value until all child nodes searched and the max,
            # together with the move will be returned.
            # 
            # Below is another way to implement, but the readiably is really
            # lousy!
            # 
            # #(value, _), move = max([(min_search(self, game.forecast_move(m), depth, cur_depth), m)
            #    for m in legal_moves])
            value = float("-inf")
            move = (-1,-1)
            
            for m in legal_moves:
                if cur_depth == depth:
                    # This is the terminal state when current depth is the
                    # defined depth
                    score_value = self.score(game.forecast_move(m), self)
                else:
                    # Go to min branch if not in leaf node
                    score_value = min_search(self, game.forecast_move(m),
                        depth, cur_depth, myalpha, mybeta)[0]

                # Find the max value
                if score_value > value:
                        value = score_value
                        move = m
                # Perform pruning
                if value >= mybeta:
                    return value, move
                if value > myalpha:
                    myalpha = value

            return value, move

        def min_search(self, game, depth, cur_depth, myalpha, mybeta):
            """ Implemente the min search algorithm. Need to be clear about
                the terminal state and recursion state.

            Parameters
            ----------
            game : isolation.Board
            depth: int
            cur_depth: int
                The current depth of the node, starting from 0

            Returns
            -------
            float: the score
            tuple(int, int): The best move of the branch

            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            cur_depth += 1
            legal_moves = game.get_legal_moves()

            # If we can judge the winner at the current state, then just return
            # the score and active player's current position
            if game.is_loser(self):
                return float("-inf"), game.get_player_location(game.active_player)

            if game.is_winner(self):
                return float("inf"), game.get_player_location(game.active_player)

            # Get the min from all the max nodes. The score value is initialized
            # as positive infinity. Then for each possible move m, get the
            # return value (the first element of the tuple) and compare with
            # the current value until all child nodes searched and the min,
            # together with the move will be returned.
            # 
            # Below is another way to implement, but the readiably is really
            # lousy!
            # 
            #(value, _), move = min([(max_search(self, game.forecast_move(m), depth, cur_depth), m)
            #    for m in legal_moves])
            value = float("inf")
            move = (-1,-1)

            for m in legal_moves:
                if cur_depth == depth:
                    # This is the terminal state when current depth is the
                    # defined depth
                    score_value = self.score(game.forecast_move(m), self)
                else:
                    # Go to max branch if not in leaf node
                    score_value = max_search(self, game.forecast_move(m), 
                        depth, cur_depth, myalpha, mybeta)[0]

                # Find the min value
                if score_value < value:
                        value = score_value
                        move = m

                # Perform pruning
                if value <= myalpha:
                    return value, move
                if value < mybeta:
                    mybeta = value

            return value, move

        # TODO: finish this function!
        if maximizing_player:
            return max_search(self, game, depth, 0, alpha, beta)
        else:
            return min_search(self, game, depth, 0, alpha, beta)
        raise NotImplementedError
