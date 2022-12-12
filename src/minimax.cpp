#include "minimax.hpp"

#define COORDS(result) (result.first)
#define SCORE(result) (result.second)


/* Combine two bit masks into one */
t_super superpose(t_board &board)
{
    t_super superposition;

    for (t_super::iterator it = board.begin(); it != it.end(); it++)
    {
        superposition.push_back((*it).first | (*it).second);
    }
    return superposition;
}


std::vector<t_coord> get_possible_coords(t_board)
{
    
}


t_board update_board(t_board &board, t_coord coord, int turn)
{
    t_board new_board;
    std::bitset<19> &mask;

    new_board = board;
    mask = turn ? new_board[coord.first].first : new_board[coord.first].second;
    mask.set(coord.second, 1);
    return new_board;
}


std::pair<t_coord, int> maximize(int depth, t_board &board, int &alpha, int &beta, int turn)
{
    std::pair<std::pair<int, int>, int> result;
    int best_index;
    int best_score;

    children = get_possible_coords(board);
    best_score = INT32_MIN;
    best_index = 0;

    for (int i = 0; i < children.size(); i++)
    {
        // run minimax on the current child as a minimizer
        result = minimax(depth - 1, children[i], alpha, beta, false);

        // proun the rest of the children
        alpha = std::max(alpha, SCORE(result));
        if (beta <= alpha)
            break ;

        // update index and score of the best
        best_index = i;
        best_score = std::max(SCORE(result), best_score);
    }

    // return the best coordinates and score
    result.first = children[best_index];
    result.second = best_score;
    return result;
}




std::pair<std::pair<int, int>, int> minimize(int depth, t_board &board, int &alpha, int &beta, int turn)
{
    std::pair<std::pair<int, int>, int> result;
    int best_index;
    int best_score;

    children = get_possible_coords(board);
    best_score = INT32_MAX;
    best_index = 0;

    for (int i = 0; i < children.size(); i++)
    {
        // run minimax on the current child as a minimizer
        result = minimax(depth - 1, children[i], alpha, beta, true);

        // proun the rest of the children
        beta = std::min(beta, SCORE(result));
        if (beta <= alpha)
            break ;

        // update index and score of the best
        best_index = i;
        best_score = std::min(SCORE(result), best_score);
    }

    // return the best coordinates and score
    result.first = children[best_index];
    result.second = best_score;
    return result;
}


std::pair<std::pair<int, int>, int> minimax(int depth, t_board &board, int &alpha, int &beta, int is_max, int turn)
{
    if (depth == 0)
        return static_evaluation(board);

    if (is_max)
        return maximize(depth, board, alpha, beta);
    int i = 0;
    return minimize(depth, board, alpha, beta);
}