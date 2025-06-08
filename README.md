# Wordle Solver
*Wordle* is a word riddle game where you are tasked to find a secret five letter word by trying out different words and getting information after each guess. If a letter is in the word it getts colored green, if it appears in the word, but in different position it will be colored yellow and if the word doesnt contain the letter at all, it will appear black. This repository contains files to solve the riddle using information theory. The basic idea is to calculate a local optimal word that would give you the maximum expected informationgain. If you want to learn more about the math behind this i recommend to watch 3 blue 1 browns YouTube video on this toppic: https://www.youtube.com/watch?v=v68zYyaEmEA 
# How to use
1. Clone the repository
   ```bash
   git clone https://github.com/Kolja-05/Wordle_solver.git

2. Execute the pythonscript
   ```bash
   python3 solver.py

3. The scirpt will give you the best guess, you should enter it on the wordle site and provide the programm with the colorfeedback as a 5 letter string with B, Y and G
