#include "minimax.hpp"
#include <bitset>

#define COORDS(result) (result.first)
#define SCORE(result) (result.second)
#define GET_BIT(bitset, index) (bitset[18 + index])


std::vector<t_coord> get_possible_coords(t_board &board, int player)
{
    std::vector<t_coord> coords;

    if (player == 1)
    {
        for (int i = 0; i <  board.size(); i++)
        {

        }
    }
    else
    {
        for (t_board::iterator row = board.begin(); it != board.end(); it++)
        {

        }
    }
    return coords;
}


t_board update_board(t_board &board, t_coord &coord, int player)
{
    t_board new_board;

    new_board = board;
    if (player == 1)
        new_board[coord.first].first.set(coord.second, 1);
    else
        new_board[coord.forst].second.set(coord.second, 1);
    return new_board;
}


std::pair<t_coord, int> maximize(int depth, t_board &board, int &alpha, int &beta, int player)
{
    std::pair<std::pair<int, int>, int> result;
    int best_index;
    int best_score;

    children = get_possible_coords(board);
    best_score = INT32_MIN;
    best_index = 0;

    for (int i = 0; i < children.size(); i++)
    {
        result = minimax(depth - 1, update_board(board, children[i]), alpha, beta, false);
        alpha = std::max(alpha, SCORE(result));
        if (beta <= alpha)
            break ;
        best_index = i;
        best_score = std::max(SCORE(result), best_score);
    }
    result.first = children[best_index];
    result.second = best_score;
    return result;
}


std::pair<t_coord, int> minimize(int depth, t_board &board, int &alpha, int &beta, int player)
{
    std::pair<t_coord, int> result;
    int best_index;
    int best_score;

    children = get_possible_coords(board, player);
    best_score = INT32_MAX;
    best_index = 0;

    for (int i = 0; i < children.size(); i++)
    {
        result = minimax(depth - 1, update_board(board, children[i]), alpha, beta, true);
        beta = std::min(beta, SCORE(result));
        if (beta <= alpha)
            break ;
        best_index = i;
        best_score = std::min(SCORE(result), best_score);
    }

    result.first = children[best_index];
    result.second = best_score;
    return result;
}


std::pair<t_coord, int> minimax(int depth, t_board &board, int &alpha, int &beta, int is_max, int player)
{
    if (depth == 0)
        return static_evaluation(board);
    if (is_max)
        return maximize(depth, board, alpha, beta, player);
    return minimize(depth, board, alpha, beta, player);
}
