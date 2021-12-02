import os
import re
import shelve
from collections import namedtuple
from typing import List

Token = namedtuple('Token', ('word', 'type', 'start'))
Index = namedtuple('Index', ('filename', 'line', 'start', 'end'))
Window = namedtuple('Window', ('main_tk_idx', 'start', 'end'))


class Tokenizer:
    def __init__(self, dir_path: str, query: str, db_path='hypersearch.db'):
        def process_query(query: str) -> tuple:
            components = (None, None, None, None, None)
            try:
                content, win_size, limit, offset, *pairs_str = query.split(';')
                content = content[1:-1]  # remove quotation marks in string
                win_size, limit, offset = int(win_size), int(limit), int(offset)
                pairs: List[tuple] = []
                for pair in pairs_str:
                    lim, off = map(int, pair.split(','))
                    pairs.append((lim, off))
            except ValueError:
                print(f"{query} is not in the right format!")
            else:
                tokens = Tokenizer.tokenizing(content)
                components = (tokens, win_size, limit, offset, pairs)
            finally:
                return components

        self._dir_path = dir_path
        self._tokens: List[Token] = []
        self._indices: List[Index] = []
        self._db_path = db_path
        self._qr_components = process_query(query)

    @staticmethod
    def tokenizing(text: str):
        tokens = []
        for obj in re.finditer(r'[a-zA-Z]+|[0-9]+', text):
            word = obj.group(0)
            word_type = 'alpha' if word.isalpha() else 'digit'
            start = obj.start()
            tokens.append(Token(word=word, type=word_type, start=start))
        return tokens

    @property
    def _dir_filenames(self) -> list:
        return [filename for filename in sorted(os.listdir(self._dir_path)) if filename.endswith('.txt')]

    def file_tokenizing(self, filename: str) -> None:
        with open(os.path.join(self._dir_path, filename)) as file:
            for line_num, line_text in enumerate(file):
                for obj in re.finditer(r'[a-zA-Z]+|[0-9]+', line_text):
                    word = obj.group(0)
                    word_type = 'alpha' if word.isalpha() else 'digit'
                    start = obj.start()
                    end = obj.end()
                    token = Token(word=word, type=word_type, start=start)
                    index = Index(filename=filename, line=line_num, start=start, end=end)
                    self._tokens.append(token)
                    self._indices.append(index)

    def dir_tokenizing(self):
        if not os.access(self._dir_path, os.F_OK):
            return None
        for filename in self._dir_filenames:
            self.file_tokenizing(filename)

    def save_database(self):
        result_dict = {}
        for token, index in zip(self._tokens, self._indices):
            result_dict.setdefault(token.word, {}).setdefault(index.filename, []) \
                .append([index.line, index.start, index.end])
        with shelve.open(self._db_path, writeback=True) as db:
            for key, value in result_dict.items():
                db[key] = value

    def searching_positions(self) -> dict:
        tokens, limit, offset = self._qr_components[0], self._qr_components[2], self._qr_components[3]
        with shelve.open(self._db_path) as db:
            res_dict = {}
            for filename in self._dir_filenames[offset:][:limit + 1]:
                inner_idxs = []
                for token in tokens:
                    try:
                        inner_idxs.extend(db[token.word][filename])
                    except KeyError:
                        break
                    else:
                        res_dict[filename] = sorted(inner_idxs)
        return res_dict

    def creating_context(self, idx: Index) -> Window:
        win_size = self._qr_components[1]
        if win_size == 0:
            return Window(main_tk_idx=None, start=None, end=None)
        # find all indices in the same line
        i_inline = [i for i in self._indices if i.filename == idx.filename and i.line == idx.line]
        left_context = i_inline[max(i_inline.index(idx) - win_size, 0)]
        right_context = i_inline[min(i_inline.index(idx) + win_size, len(i_inline) - 1)]
        return Window(main_tk_idx=[idx], start=left_context.start, end=right_context.end)

    def finding_windows(self, pos_dict: dict) -> dict:
        win_dict = {}
        for filename, pos_list in pos_dict.items():
            for pos in pos_list:
                win = self.creating_context(Index(filename=filename, line=pos[0], start=pos[1], end=pos[2]))
                win_dict.setdefault(filename, []).append(win)
        return win_dict

    def extending_windows(self, win_dict: Window) -> dict:
        def overlapped(window_left, window_right) -> bool:
            if window_left.main_tk_idx[0].line != window_right.main_tk_idx[0].line:
                return False
            elif window_left.start <= window_right.start <= window_left.end:
                return True
            return False

        def extending(window) -> Window:
            win_start = window.start
            win_end = window.end
            # now extend the border of merged window to punctuation/ end of line/ start of line
            with open(os.path.join(self._dir_path, filename)) as file:
                line = file.readlines()[window.main_tk_idx[0].line]
                line_left = 0
                line_right = len(line) + 1
                frase_ends = []
                for matchobj in re.finditer(r'[.!?]+', line):  # find all punctuations in line
                    frase_ends.append(matchobj.end())  # their end position
                for frase_end in frase_ends:
                    if frase_end < win_start:  # punctuation before the left-border
                        if line[frase_end] == ' ':  # that means right after the punctuation has a space
                            # extend to the left to the beginning of line
                            line_left = frase_end + len(re.match(r'[ ]+', line[frase_end:])[0])
                    elif win_end <= frase_end <= line_right and line[frase_end] == ' ':
                        line_right = frase_end
                        break
            return Window(main_tk_idx=win.main_tk_idx, start=line_left, end=line_right)

        def merging(window_left, window_right) -> Window:
            merged_win_start = min(window_left.start, window_right.start)
            merged_win_end = max(window_right.end, window_left.end)
            # now extend the border of merged window to punctuation/ end of line/ start of line
            with open(os.path.join(self._dir_path, filename)) as file:
                line = file.readlines()[window_left.main_tk_idx[0].line]
                line_left = 0
                line_right = len(line)
                frase_ends = []
                for matchobj in re.finditer(r'[.!?]+', line):  # find all punctuations in line
                    frase_ends.append(matchobj.end())  # their end position
                for frase_end in frase_ends:
                    if frase_end < merged_win_start:  # punctuation before the left-border
                        if line[frase_end] == ' ':  # that means right after the punctuation has a space
                            # extend to the left to the beginning of line
                            line_left = frase_end + len(re.match(r'[ ]+', line[frase_end:])[0])
                    elif merged_win_end <= frase_end <= line_right and line[frase_end] == ' ':
                        line_right = frase_end
                        break
            return Window(main_tk_idx=window_left.main_tk_idx + window_right.main_tk_idx, start=line_left,
                          end=line_right)

        ext_win_dict = {}
        for filename, wins in win_dict.items():
            ext_wins = []
            for i, win in enumerate(wins):
                if len(ext_wins) == 0:
                    ext_wins.append(extending(win))
                else:
                    last_win = ext_wins.pop()
                    if overlapped(last_win, win) is True:
                        ext_wins.append(merging(last_win, win))
                    else:
                        ext_wins.append(last_win)  # put it back
                        ext_wins.append(extending(win))  # put new one
            ext_win_dict[filename] = ext_wins
        return ext_win_dict

    def stage_7(self):
        def print_window(win: Window) -> str:
            with open(os.path.join(self._dir_path, win.main_tk_idx[0].filename)) as file:
                line = file.readlines()[win.main_tk_idx[0].line][:-1]
                for idx in win.main_tk_idx[::-1]:
                    line = line[:idx.end] + '</b>' + line[idx.end:]
                    line = line[:idx.start] + '<b>' + line[idx.start:]
            return line[win.start:(win.end + 7 * len(win.main_tk_idx) + 1)]

        self.dir_tokenizing()
        self.save_database()
        pos_result_dict = self.searching_positions()
        win_result_dict = self.finding_windows(pos_result_dict)
        ext_win_result_dict = self.extending_windows(win_result_dict)
        for i, (filename, wins) in enumerate(ext_win_result_dict.items()):
            print(os.path.join(self._dir_path, filename))
            limit, offset = self._qr_components[4][i]
            for k, win in enumerate(wins[offset:][:limit]):
                print(f"{k + 1}. {print_window(win)}".strip())


if __name__ == '__main__':
    my_tokenizer = Tokenizer(dir_path=input(), query=input())
    my_tokenizer.stage_7()
