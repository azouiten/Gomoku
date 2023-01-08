#ifndef __TYPES__
#define __TYPES__

#include <vector>
#include <bits/stdc++.h>

// Bit maps of each color in the board
typedef std::vector<std::pair<std::bitset<19>, std::bitset<19>> > t_board;

// A vector containing the superposition of the bit masks
typedef std::vector<int> t_superposition;

// A pair representing the coordinants of a board position
typedef std::pair<int, int> t_coord;

// A vector of children generated form a board
typedef std::vector<std::pair<int, int> > t_children;

#endif