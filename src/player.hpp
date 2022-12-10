#ifndef _PLAYER_
#define _PLAYER_

#include <iostream>
#include <vector>

typedef std::vector<std::vector<int> > t_board;
typedef std::pair<int, int> t_cords;

class Player
{
    private:
    t_board _board;
    int     _alpha;
    int     _beta;
    bool    _player;
    public:
    Player(bool player);
    ~Player(void);

    t_cords makeMove(t_board &board);
};

#endif