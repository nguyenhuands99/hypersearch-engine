### Task 1

##### Description

In this stage, complete the following steps:

1.  Learn how to make context windows out of a dictionary with
    positions;
2.  Combine the first step with the features from the previous stages.
    The program should return windows, processed as in the previous
    stage.

##### Objectives

Your program is given a folder with files. The program processes them
and returns a dictionary with context windows. Then these windows should
be converted into a dictionary with combined and expanded windows with
their number adjusted by limit and offset.

In more detail, it should do the following:

1.  Take an input that consists of a dictionary, a query, a window size,
    a limit, and an offset:
    `input_dictionary,query='man', window_size=1, limit=1, offset=0`.
2.  A dictionary can look like this:
    `{'filename.txt': [first_position, second_position, ...]}` , it is
    the result of the search. Note that the context window size remains
    constant;
3.  Iterate over all positions in each file;
4.  Create a context window from each position;
5.  Save context windows in a corresponding dictionary:
    `{'filename.txt': [window1, window2, ...]}`;
6.  Extend all windows to match sentences;
7.  Test whether the windows overlap. If so, merge them into one and
    save only the result of merging. Note that before this step you
    worked only with two windows that either overlapped or not. Now, you
    have a dictionary with a lot of windows, so you should iterate over
    the dictionary, taking two consecutive windows each time to check
    whether they overlap or not. If they do not overlap, take the next
    two consecutive windows and repeat the action;
8.  Save the results in the output dictionary:
    `{'filename.txt': [window1, window2, ...]}`. Do not forget that you
    need to save as many files with their context window lists as
    indicated in the limit. Start from the index of the result that is
    indicated in the offset; see the example below;
9.  Sort the dictionary in ascending order and print the result in the
    following format:
    `filename_1: list with windows_1\nfilename_2: list with windows_2`
10. Clear the database after indexing

##### Examples

The greater-than symbol followed by a space (`> `) represents the user
input. Note that it's not part of the input.

During tests, you are given a test folder. Input is a folder path, where
you need to find and process all text files. Your program should take
this path and iterate over files. Clear your database after each test.

**Example 1**:

Folder contents: *testfile1.txt, testfile2.txt.*

*testfile1.txt* contents:  
`It seemed a delightful prospect. This man evidently understands my complaint.`

*testfile2.txt* contents:  
`Every possible situation man could imagine has been spoilt.`

Output:

    > tests/stage6/ex1
    > 'man',1,1,0
    testfile1.txt: ['It seemed a delightful prospect. This man evidently understands my complaint.|[[0, 38, 41]]|33|78']

**Example 2**:

Folder contents: *testfile3.txt*.

*testfile3.txt* contents:

    There’s enough water to see, right?
    To tell the truth, it was water from the river, too.

Output:

    > tests/stage6/ex2
    > 'water',1,2,0
    testfile3.txt: ['There’s enough water to see, right?|[[0, 15, 20]]|0|36', 'To tell the truth, it was water from the river, too.|[[1, 26, 31]]|0|53']

### Task 2

##### Description

In this stage, you will create a database that stores unique tokens and
their positions in the text. Imagine a document contains only one line:
`John is a 4th-year student`, so the resulting <span
style="background-color: transparent; color: #000000; font-size: 11pt; font-variant: normal;">`("student", 19, "alpha")`
</span>token is stored in line no. 0 (remember, enumeration starts from
zero!). The token starts at 19, which is already known from the previous
step, and ends at 19 + 7 = 26 as there are seven letters in the word
`student`. The indexer should take tokens as <span
style="background-color: transparent; color: #000000; font-size: 11pt; font-variant: normal;">`("student", 19, "alpha")`
</span>and generate their positions, for example <span
style="background-color: transparent; color: #000000; font-size: 11pt; font-variant: normal;">`("student", 0, 19, 26)`.</span>
The indexer works the same way as the tokenizer: it does not store
anything in memory, it generates and outputs the results for each token.
It should work when the file is empty. In this case, the program should
output `None`.

##### Objectives

In this stage, you need to write an indexer that assigns a search index
(a list of positions) to tokens and creates a structure that will store
the information about these indexes. Please note that:

-   The input is a path to the folder with files; the indexer should
    take their names one by one and implement indexing for each file;
    the output is a database, which looks like this:
    `{'word': {'filename.txt': [position1, position2, ...]}, 'word2': ...}`.
-   The positions of tokens (the `[position1, position2, ...]` list)
    should be stored in ascending order, line by line, from the very
    first line in the file to the very end of the very last line in the
    same file.
-   The ascending order is based on how many lines a file contains, and
    what the starting and ending indexes are. For example, a position
    instance found in the first line of the file will be placed before
    the position found in the second line of the file. If both positions
    are found in the same line, the position with a smaller starting
    index will be placed first. If both positions are found in the same
    line and have the same starting index, the position with a smaller
    ending index will be placed first.

Don't<span style="color: #ff4363;"> </span>forget to print the resulting
dictionary.

You may want to write your own test programs that will check your code.
Check whether it takes the right input format, that it can work with any
number of files, and saves the positions of each token. Note that when
writing tests, you need to create your own text files, tokenize and
index them, and build a small test base using the indexer.

At the end of the day, your indexer should:

1.  Take a directory path as input, find all *.txt* files, and start
    processing them one by one,
2.  Read each file line by line,
3.  Implement tokenization from the previous step,
4.  Produce token pairs and their indexes (positions),
5.  Add these pairs to the database.

Do not create a new database each time you add a new file, just add new
tokens and positions to the same database. Bear in mind that the
database should be closed after use.

##### Examples

The greater-than symbol followed by a space (`> `) represents the user
input. Note that it's not part of the input.

During tests, you are given a test directory. Input is a folder path,
where you need to find and process all text files. Your program should
take this path and iterate over files. Clear your database after each
test.

**Example 1**: *One file with one word in it*

Folder contents: *testfile1.txt*

File contents<span
style="background-color: transparent; color: #000000; font-size: 11pt; font-variant: normal;">:
</span>`student`

    > tests/stage2/ex1
    {
        'student': {'testfile1.txt': [[0, 0, 7]]}
    }

**Example 2**: *Two files with strings*

Folder contents: *testfile2.txt*`,`*testfile3.txt*

*testfile2.txt* contents: `John is @ student`

The output of *testfile2.txt*:

    {
        'John': {'testfile2.txt': [[0, 0, 4]]},
        'is': {'testfile2.txt': [[0, 5, 7]]},
        'student': {'testfile2.txt': [[0, 10, 17]]}
    }

*testfile3.txt c*ontents: `Mary loves John`

The output of *testfile3.txt:*

    > tests/stage2/ex2
    {
        'John': {'testfile2.txt': [[0, 0, 4]],
        'testfile3.txt': [[0, 11, 15]]},
        'is': {'testfile2.txt': [[0, 5, 7]]},
        'student': {'testfile2.txt': [[0, 10, 17]]},
        'Mary': {'testfile3.txt': [[0, 0, 4]]},
        'loves': {'testfile3.txt': [[0, 5, 10]]},
    }

**Example 3:** *One file with two strings*

Folder contents: *testfile4.txt*

*testfile4.txt* contents:
`Her true self was poorly concealed \n Her eyes were her own.`

Output: one database containing pairs from the file

    > tests/stage2/ex3
    {
        Her: {'testfile4.txt': [[0, 0, 3], [0, 36, 39]]};
        true: {'testfile4.txt': [[0, 4, 8]]};
        self: {'testfile4.txt': [[0, 9, 13]]};
        was: {'testfile4.txt': [[0, 14, 17]]};
        poorly: {'testfile4.txt': [[0, 18, 24]]};
        concealed: {'testfile4.txt': [[0, 25, 34]]};
        eyes: {'testfile4.txt': [[0, 40, 44]]};
        were: {'testfile4.txt': [[0, 45, 49]]};
        her: {'testfile4.txt': [[0, 50, 53]]};
        own: {'testfile4.txt': [[0, 54, 57]]}
    }

**Example 4**: *An empty file*

Folder content: *testfile5.txt*

File contents: empty

    > tests/stage2/ex4

### Task 3

##### Description

In this stage, you will create a simple search program. Let's start! A
search engine looks for token coordinates in the database that you have
created. Once the texts are tokenized and indexed, you will be able to
get a list of all token positions. A good engine should process and find
several tokens in one string. A good engine also should be able to
process a set of documents. Even though you are not making a browser
version of the search engine in this project, it may be a good idea to
think about how to display the results, as there may be too many search
results. Imagine you went through 10 documents and found a certain
number of positions in each of them. Maybe you do not want to look
through all the documents, as the first three are enough. You need to
think about some kind of a limiter to output (also known as **limit**)
only the necessary documents. A limit is a number that controls how many
search results to display. If there are 10 documents, and you need to
display only 3 of them, then the limit will be 3, and only three
documents will be displayed as a search result. We also have a parameter
called **offset.** An offset is also a number, but it stands for the
sequential number of the document that you want to show. For example,
you still want to see three documents, and you want to start not from
the first, but from the fifth document. Then the result will show three
documents that come under the numbers five, six, and seven in the
original search array.

##### Objectives

To successfully complete this stage your program should:

1.  Take a directory from the input.
2.  Tokenize and index each file from the directory and create a
    database (as in the previous step).
3.  Take a query (a line of words), the limit, and the offset.
4.  Tokenize it and remember the words.
5.  Find each token in the database with its filename and positions.
6.  Get the names of the files containing all tokens; if you have
    several text files in the database and want to find two words there,
    then you only need those files where both of these words are
    encountered. The distance between these tokens in one file is not
    relevant.
7.  Sort by filenames and shorten the results by limit and offset; note
    that the offset should be more than 0; if it is a negative number,
    set the offset to 0 automatically. If the limit is bigger than the
    total amount of files, the limit should be set at this exact amount
    (beware, the limit can be 0; in this case, no results should be
    displayed).
8.  Return the data from the database; one or several filenames and all
    corresponding token positions for query tokens
    —`{'filename.txt': [[first_position], [second_position]]}`;
9.  Print the results in the following format:
    `<filename_1>: a list of positions; <filename_2>: a list of positions`
    so that they can be checked.

Sort the word positions in ascending order. It means that if you are
looking for two words in a file, the first position in the list should
be that of a token that occurred the first.

If a word is not found in the database, output an empty dictionary. If
several words are given in a query, and at least one of them is missing,
output an empty dictionary as well.

Do not forget to test your code. You need to create text files, index
them, and build a small test base using the indexer. This time, check
whether your program works when:

-   There is one file,
-   There are a lot of files,
-   Some or all words in the query cannot be found in the database.

Clear the database after indexing.

##### Examples

The greater-than symbol followed by a space (`> `) represents the user
input. Note that it's not part of the input.

During tests, you are given a test directory. Input is a folder path,
where you need to find and process all text files. Your program should
take this path and iterate over files. Clear your database after each
test.

**Example 1:** *You are looking for one word and need only one file*

Folder contents: *testfile1.txt*, *testfile2.txt*, *testfile3.txt*

*testfile1.txt* contents:  
`Scarlett made a mouth of bored impatience.`

*testfile2.txt* contents:  
`Look, Scarlett. About tomorrow`

*testfile3.txt* contents:  
`Hello, world!!!`

Output:

    > tests/stage3/ex1
    > 'Scarlett',1,0
    testfile1.txt: [[0, 0, 8]]

**Example 2**: *You have three files, you are looking look for several
words and need two files starting from the second one*

Folder contents: *testfile4.txt, testfile5.txt, testfile6.txt*

*testfile4.txt* contents:  
`Seated with Stuart and Brent Tarleton, she made a pretty picture.`

*testfile5.txt* contents:  
`Stuart and Brent considered their latest expulsion a fine joke.`

*testfile6.txt* contents:  
`It was for this precise reason that Stuart and Brent were idling on the porch of Tara this April afternoon.`

Output:

    > tests/stage3/ex2
    > 'Stuart and Brent',5,1
    testfile5.txt: [[0, 0, 6], [0, 7, 10], [0, 11, 16]]; testfile6.txt: [[0, 36, 42], [0, 43, 46], [0, 47, 52]]

**Example 3**: *No such words in files*

Folder contents: *testfile7.txt*, *testfile8.txt*

*testfile7.txt* contents:  
`Although born to the ease of plantation life, the faces of the three  were neither slack nor soft.`

*testfile8.txt* contents:  
`Scarlett O’Hara was not beautiful, but men seldom realized it `

Output:

    > tests/stage3/ex3
    > 'Natasha Rostova',1,1

**Example 4**: *Limit is zero*

Folder contents: *testfile9.txt*, *testfile10.txt*

*testfile9.txt* contents:  
`The war, goose! The war’s going to start any day.`

*testfile10.txt* contents:  
`You know there isn’t going to be any war, It’s all just talk.`

Output:

    > tests/stage3/ex4
    > 'war',0,0

### Task 4

##### Description

In this stage, we will focus on how to display what you have found to a
user in a readable form. We need to create a context window for any
token for this. A context window is the token's environment, in other
words, other tokens on the left and right. There can be a lot of them —
two or ten. The goal is to immediately show a context window for each
position in the list. For example, we have a line:
`John and Mary are students and they live in London`. You want to create
a context window for `in` with one token on the left and right. The
result is a context window that has:

-   The `John and Mary are students and they live in London` line. It is
    important to include the whole line for the next steps, where you
    will extend the borders of the window to match the sentence's
    borders. If the token is the first/last in the file, there is no
    need to move to the next/previous line to fill the context window;
-   The position of the token, for example, `0, 41, 43`;
-   The indexes of the context window borders, where the first index is
    the start of the first token in the window, `live` in our case and
    the end of the last token in the window, `London`.

The context window may include more than one sentence; if the word was
the last in the sentence with the window size of 4, then include a part
of the next sentence.

##### Objectives

Write a program that creates a context window for a token. Later, you
will be able to run this function several times for each token that
needs a window. For now, the program should:

1.  Take a folder with files as an input, iterate over it, read the data
    from the input about the position of a token and the size of the
    window for each file; the filenames, the positions of the tokens,
    and the window sizes are placed in one input string and are
    separated by semicolumns, for example, `testfile1.txt;0,0,6;2`. Note
    that if the window size is 0, the program should return an empty
    string.
2.  Find the line with the token and tokenize the line from left to
    right and vise versa. It is done to find the positions of the
    neighboring tokens, depending on the window size.
3.  Remember the beginning and the end of the window.
4.  Write down the positions in the nested list, for example,
    `[[0, 0, 6]]`. There can be several tokens in the context window if
    the request consists of more than one word. It will also be required
    for the next stages.
5.  Print the context window as a string, where all attributes of the
    window are separated from each other by the `|` symbol; see more
    examples below.

Don't forget to test your program. Check whether your program works
when:

-   The token is the first/last in a line;
-   There are empty lines in the file;
-   There is no such token in the file.

Clear the database immediately after indexing.

##### Examples

The greater-than symbol followed by a space (`> `) represents the user
input. Note that it's not part of the input.

During tests, you are given a test directory. Input is a folder path,
where you need to find and process all text files. Your program should
take this path and iterate over files. Clear your database after each
test.

**Example 1**: *The token is first, the window size is two*

Folder contents: *testfile1.txt*

*testfile1.txt* contents:  
`Spring had come early that year.`

Output:

    > tests/stage4/ex1
    > testfile1.txt;0,0,6;2
    Spring had come early that year.|[[0, 0, 6]]|0|15

**Example 2**: *The token is in the middle of the string, the window
size is one*

Folder contents: *testfile2.txt*

*testfile2.txt* contents:

    Spring had come early that year.
    He had come on tuesday night.

Output:

    > ex2
    > testfile2.txt;1,7,11;1
    He had come on tuesday night.|[[1, 7, 11]]|3|14

**Example 3**: *The token is the last in the string, the window size is
three*

Folder contents: *testfile3.txt*

*testfile3.txt* contents:  
`Spring had come early that year.`

Output:

    > ex3
    > testfile3.txt;0,27,31;3
    Spring had come early that year.|[[0, 27, 31]]|11|31

**Example 4**: *The window size is zero*

Folder contents: *testfile4.txt*

*testfile4.txt* contents:  
`You can always tell weather by sunsets.`

Output:

    > ex4
    > testfile4.txt;0,15,19;0

### Task 5

##### Description

Work with context windows to make them pretty and convenient. You should
highlight the words from the query, merge several windows into one if
they are overlapping, and extend the borders of the windows so that they
can match a whole sentence.

First, you need to check the windows for overlapping. It happens when
two windows (A and B) are in the same line, but the ending index of A is
less than (or equal to) the starting index of B, or the ending index of
A is bigger (or equal to) than the starting index of B. The windows also
overlap when their borders coincide.

If the windows do overlap, combine them into one. You need to find their
joint starting and ending index and then assign this new index as new.
The resulting list should include both positions (see the examples
below).

Further, you need to extend the window's borders to match a sentence.
For example, you have a window size of 2, and the following line:
`Spring had come early that year`. The token position is `[0,0,6]` , the
window borders are 0 and 15. Now you need to find the end of this
sentence and assign new window borders — 0 and 31.

One more example of overlapping windows. You have a small sentence:
`Mary and Lisa went shopping in town`. There are two context windows for
the query we are looking for: `Mary and Lisa` and `Lisa went shopping`.
The `Lisa` token is overlapping, so they should be combined into
`Mary and Lisa went shopping`. However, this is not the whole sentence,
so extended to the very end of the sentence.

The sentence boundaries may be obscure as there are all sorts of
abbreviations, initials, and other stuff. Punctuation marks can help you
with that, you can use [ready-made
patterns](https://docs.python.org/3/library/re.html) with `re`:

    PATTERN = re.compile(r’[\.!?]+')

The last feature should highlight the words from the query. It uses tags
`<b>` and `</b>` and inserts them at the begging and to the end of a
token to make it bold. For example, you have the following context
window: `Spring had come early that year.` for a `Spring` query, the
pattern would highlight the word:
`<b>Spring</b> had come early that year.` If there is more than one word
in a query, then each of them would be highlighted. These tags work with
the HTML markup. It can be important if you want to write a search
interface after completing a project.

##### Objectives

During testing, you will get two context windows as input (strings).
Your output should either consist of two independent windows with
extended boundaries and query words highlighted or of one combined
window in case the given windows overlap, also with extended boundaries
and words highlighted. So your program should do the following:

1.  If there are two windows, check whether they overlap.
2.  If they overlap, combine them into one.
3.  If you have one window, take it as input and expand its boundaries.
4.  Attach tags `<b>` and `</b>` to the start and the end of the main
    tokens.

Let's break it down. The first window is a
`Spring had come early that year.` line, the token position is
`[0,0,6]`, window borders are 0 and 15. The second window is a
`Spring had come early that year.` line, the token position is
`[0,11,15]`, window borders 7 and 21. `Spring had come` is overlapping
the second window `had come early`. Combine them to get a new
`Spring had come early` window, the window borders are 0 and 21, the
positions are `[[0,0,6], [0,11,15]]`. Extend the window to
`<b>Spring</b> had <b>come</b> early that year.`, the borders are 0 and
31, the positions are represented as a `[[0,0,6], [0,11,15]]` list .

Note that the output should contain one window, printed like in the
previous stage if the given windows are overlapping, and two windows,
printed one after another if the windows do not overlap.

##### Examples

The greater-than symbol followed by a space (`> `) represents the user
input. Note that it's not part of the input.

**Example 1**: *Windows are overlapping*

Input: two windows, the window size is two.

Output: one window (since the first window goes to the second sentence
and merges with the second window); the line consists of two sentences

    > I feel sure she loves lilies. And they are so appropriate to a bride.|[[0, 22, 28]]|12|38
    > I feel sure she loves lilies. And they are so appropriate to a bride.|[[0, 34, 38]]|22|45
    I feel sure she loves <b>lilies</b>. And <b>they</b> are so appropriate to a bride.|[[0, 22, 28], [0, 34, 38]]|0|69

**Example 2**: *Windows are overlapping within one sentence*

Input: two windows, the window size is 1

Output: one window

    > You know you promised to obey.|[[0, 9, 12]]|4|21
    > You know you promised to obey.|[[0, 13, 21]]|9|24
    You know <b>you</b> <b>promised</b> to obey.|[[0, 9, 12], [0, 13, 21]]|0|30

**Example 3**: *Windows are not overlapping*

Input: two windows, the window size is one

Output: two windows

    > Oh, by the by, dear, I shan’t be able to go with you today. I’ve rather a headache.|[[0, 53, 58]]|49|58
    > Oh, by the by, dear, I shan’t be able to go with you today. I’ve rather a headache.|[[0, 74, 82]]|72|82
    Oh, by the by, dear, I shan’t be able to go with you <b>today</b>.|[[0, 53, 58]]|0|59
    I’ve rather a <b>headache</b>.|[[0, 74, 82]]|60|83

**Example 4**: *Windows are not overlapping within one sentence*

Input: two windows, the window size is one

Output: there will be two windows with the same line

    > Yes, she must be clever to have obtained the position that she has.|[[0, 5, 8]]|0|13
    > Yes, she must be clever to have obtained the position that she has.|[[0, 45, 53]]|41|58
    Yes, <b>she</b> must be clever to have obtained the position that she has.|[[0, 5, 8]]|0|67
    Yes, she must be clever to have obtained the <b>position</b> that she has.|[[0, 45, 53]]|0|67

### Task 6

##### Description

In this stage, complete the following steps:

1.  Learn how to make context windows out of a dictionary with
    positions;
2.  Combine the first step with the features from the previous stages.
    The program should return windows, processed as in the previous
    stage.

##### Objectives

Your program is given a folder with files. The program processes them
and returns a dictionary with context windows. Then these windows should
be converted into a dictionary with combined and expanded windows with
their number adjusted by limit and offset.

In more detail, it should do the following:

1.  Take an input that consists of a dictionary, a query, a window size,
    a limit, and an offset:
    `input_dictionary,query='man', window_size=1, limit=1, offset=0`.
2.  A dictionary can look like this:
    `{'filename.txt': [first_position, second_position, ...]}` , it is
    the result of the search. Note that the context window size remains
    constant;
3.  Iterate over all positions in each file;
4.  Create a context window from each position;
5.  Save context windows in a corresponding dictionary:
    `{'filename.txt': [window1, window2, ...]}`;
6.  Extend all windows to match sentences;
7.  Test whether the windows overlap. If so, merge them into one and
    save only the result of merging. Note that before this step you
    worked only with two windows that either overlapped or not. Now, you
    have a dictionary with a lot of windows, so you should iterate over
    the dictionary, taking two consecutive windows each time to check
    whether they overlap or not. If they do not overlap, take the next
    two consecutive windows and repeat the action;
8.  Save the results in the output dictionary:
    `{'filename.txt': [window1, window2, ...]}`. Do not forget that you
    need to save as many files with their context window lists as
    indicated in the limit. Start from the index of the result that is
    indicated in the offset; see the example below;
9.  Sort the dictionary in ascending order and print the result in the
    following format:
    `filename_1: list with windows_1\nfilename_2: list with windows_2`
10. Clear the database after indexing

##### Examples

The greater-than symbol followed by a space (`> `) represents the user
input. Note that it's not part of the input.

During tests, you are given a test folder. Input is a folder path, where
you need to find and process all text files. Your program should take
this path and iterate over files. Clear your database after each test.

**Example 1**:

Folder contents: *testfile1.txt, testfile2.txt.*

*testfile1.txt* contents:  
`It seemed a delightful prospect. This man evidently understands my complaint.`

*testfile2.txt* contents:  
`Every possible situation man could imagine has been spoilt.`

Output:

    > tests/stage6/ex1
    > 'man',1,1,0
    testfile1.txt: ['It seemed a delightful prospect. This man evidently understands my complaint.|[[0, 38, 41]]|33|78']

**Example 2**:

Folder contents: *testfile3.txt*.

*testfile3.txt* contents:

    There’s enough water to see, right?
    To tell the truth, it was water from the river, too.

Output:

    > tests/stage6/ex2
    > 'water',1,2,0
    testfile3.txt: ['There’s enough water to see, right?|[[0, 15, 20]]|0|36', 'To tell the truth, it was water from the river, too.|[[1, 26, 31]]|0|53']

### Task 7

##### Description

Welcome to the final stage of the project!

You need to take the attached
[folder](https://stepik.org/media/attachments/lesson/383392/tests.rar)
and make a new database. In previous stages, the files and databases you
created were for educational purposes, they served only to check your
program. Now, it's time to create a real search engine with real-world
text files. In this case, you will work with short stories of Jerome
Klapka Jerome. Note that indexing the database may take a while because
the files are much bigger than in all previous stages.

In this stage, perform a search in this new database. Also, you need a
function that searches for a query in the database and returns the pairs
— `filename: contexts with the query words` in string format. You
already know how to adjust the number of documents using limit and
offset, now you need to do the same with **quotes** in the files. By
quotes, we understand sentences from the indexed files that contain the
query words.

As a result, your search should return a limited number of documents
starting from the document offset, and also a limited number of quotes,
starting from the quotes offset. Note that limits and offsets for
documents and quotes are different!

##### Objectives

Your search at this stage should:

1.  Take a query, a window size, a limit, and an offset, and a list of
    pairs (a limit, an offset) for quotes in documents as input; for
    example, you want to find the word `'man'` , with limit=3, offset=0.
    You want three quotes starting from the first and the window size is
    one, so the input would look like this:
    `query='man', window_size=1, limit=3, offset=0, pairs=[(3,0),(3,0),(3,0)]`;

2.  Implement the second function from the previous stage and get a
    dictionary with context windows;

3.  Take the corresponding pair (limit, offset) from the list for each
    file, and if the pair is missing, use the default values — limit=3,
    offset=0. Once the interface is done, users will be able to use them
    as default values if they do not want to set their own.

4.  Take the required number of quotes from the document according to
    the limit and offset. Be careful, the offset should be more or equal
    to 0! Otherwise, set the offset to 0 automatically. If the limit is
    bigger than the total amount of files you have, set the limit to the
    number of documents. At the same time, if the limit is 0, no results
    should be displayed,

5.  Highlight the keywords in bold for each quote,

6.  Return the resulting dictionary, which will look like this
    `{'filename_one.txt': [quote0, quote1, quote2, ...], 'filename_two.txt': [quote0, quote1, quote2], 'filename_three.txt': ..., ...}`.

7.  Print the results in the following manner:

        filename 1
         1.Line 1
         2.Line 2
         3.Line 3

        filename 2
         1.Line 1
         2.Line 2
         3.Line 3

##### Examples

The greater-than symbol followed by a space (`> `) represents the user
input. Note that it's not part of the input.

You are working with large texts, so we show only the inputs and
outputs.

During tests, you are given a folder; there are 4 files with a story in
each.

Folder contents: *story\_one.txt*, *story\_two.txt*, *story\_three.txt*,
*story\_four.txt*.

**Example 1**: *The limit is bigger than the total amount of files in
the database*

    > ex
    > 'George';1;3;0;1,0;1,0;2,0
    story_one.txt
    1. We found ourselves short of water at Hambledon Lock; so we took our jar and went up to the lock-keeper’s house to beg for some. <b>George</b> was our spokesman.
    story_three.txt
    1. <b>George</b> raised his hat, and said “Good-morning.” He hoped, in answer to his politeness, to hear the polite “Welcome to our shop,” as this was the answer in the conversation book.
    story_two.txt
    1. We had made the tea, and were just settling down comfortably to drink it, when <b>George</b>, with his cup half-way to his lips, paused and exclaimed: “What’s that?”
    2. “Why that!” said <b>George</b>, looking westward.

**Example 2**: *Different limits and offsets for each document*

This example demonstrates the functionality of limits: you would have
printed the results for all four files, but since the limit is set to 3,
you need only three first outputs.

    > ex
    > 'Hambledon Lock';2;3;0;1,0;2,0;1,0
    story_one.txt
    1. We found ourselves short of water at <b>Hambledon</b> <b>Lock</b>; so we took our jar and went up to the lock-keeper’s house to beg for some.

**Example 3**: *One result in one file*

    > ex
    > 'water';3;4;0;3,0;1,0;2,0;4,0
    story_four.txt
    1. I drank them neat for six consecutive days, and they nearly killed me; but after then I adopted the plan of taking a stiff glass of brandy-and-<b>water</b> immediately on the top of them, and found much relief thereby.
    2. I have been informed since, by various eminent medical gentlemen, that the alcohol must have entirely counteracted the effects of the chalybeate properties contained in the <b>water</b>. I am glad I was lucky enough to hit upon the right thing.
    story_one.txt
    1. We found ourselves short of <b>water</b> at Hambledon Lock; so we took our jar and went up to the lock-keeper’s house to beg for some.
    story_two.txt
    1. We tried river <b>water</b> once, later on in the season, but it was not a success.
    2. Our jar was empty, and it was a case of going without our tea or taking <b>water</b> from the river.

**Example 4**: *The word does not exist*

    > ex
    > 'Count Dracula';2;4;1;2,0;2,0;3,0;1,0

**Example 5**: *The limit is zero*

    > ex
    > 'Scarlett';4;0;0;1,0;5,0;3,0;1,0
