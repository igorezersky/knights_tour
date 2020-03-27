import argparse
import json
import locale
import copy
import string
import random
from pathlib import Path
from typing import Dict, Tuple, List


class KnightTour:
    def __init__(self, moves: List, board_size: int = 8):
        self.board_size = board_size
        self.moves = moves

    @property
    def legend(self) -> str:
        return string.ascii_uppercase[:self.board_size]

    def print_legend(self):
        print(f'\n\t{" ".join(f" {el}" for el in self.legend)}')

    def print_board(self):
        self.print_legend()
        r = range(self.board_size)
        lines = ''
        for y in r:
            line_num = self.board_size - y
            lines += f'\n{line_num}\t'
            lines += ' '.join(f'{self.board[(x, y)]:2}' for x in r)
            lines += f'\t\t{line_num}'
        print(lines)
        self.print_legend()

    def __call__(self, start_x: str, start_y: int):
        start_x = ord(start_x.lower()) - ord('a')
        self.board = {(x, y): 0 for x in range(self.board_size) for y in range(self.board_size)}
        move = 1
        p = (start_x, self.board_size - int(start_y))
        self.board[p] = move
        move += 1
        while move <= len(self.board):
            p = min(self.accessibility(p))[1]
            self.board[p] = move
            move += 1

    def accessibility(self, p: Tuple[int, int]) -> List:
        access = []
        brd = copy.deepcopy(self.board)
        for pos in self.knight_moves(self.board, p):
            brd[pos] = -1
            access.append((len(self.knight_moves(brd, pos)), pos))
            brd[pos] = 0
        return access

    def knight_moves(self, board: Dict, p: Tuple[int, int]) -> set:
        px, py = p
        return set(
            (x, y) for x, y in set((px + x, py + y) for x, y in self.moves)
            if 0 <= x < self.board_size and 0 <= y < self.board_size and not board[(x, y)]
        )

def load_json_file(path: str, encoding: str = 'utf-8') -> Dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f'{path}')
    with open(path, 'r', encoding=encoding) as fp:
        return json.load(fp)


def create_parser(lang: str, trans: Dict):
    parser = argparse.ArgumentParser(trans['description'][lang])
    parser.add_argument('--color', type=str, help=trans['color']['help'][lang],
                        choices=trans['color']['choices'][lang], default='')
    parser.add_argument('--position', type=str, help=trans['position']['help'][lang],
                        choices=trans['position']['choices'][lang], default='')
    return parser


if __name__ == '__main__':
    ui_lang = locale.getlocale()[0][:2]
    translations = load_json_file('translations.json')
    settings = load_json_file('settings.json')
    if ui_lang not in settings['supported_langs']:
        ui_lang = 'en'

    args = create_parser(lang=ui_lang, trans=translations).parse_args()
    if args.color and args.position:
        start_file, start_rank = settings['knight_start_positions'][args.color][args.position]
    elif args.color:
        start_file, start_rank = random.choice(list(settings['knight_start_positions'][args.color].values()))
    elif args.position:
        start_file, start_rank = random.choice([
            settings['knight_start_positions']['black'][args.position],
            settings['knight_start_positions']['white'][args.position]
        ])
    else:
        start_file, start_rank = random.choice(string.ascii_uppercase[:settings['board_size']]), \
                                 random.choice(range(1, settings['board_size'] + 1))

    print(translations['header'][ui_lang].format(x=start_file, y=start_rank))
    try:
        knights_tour = KnightTour(moves=settings['moves'], board_size=settings['board_size'])
        knights_tour(start_x=start_file, start_y=start_rank)
        knights_tour.print_board()
    except ValueError:
        print(translations['invalid_tour'][ui_lang])
