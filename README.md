Brilliant-HungerGames-TestSuite
===============================

Testing Framework for the Hunger Games Themed Prisoner's Dilemma Competition from Brilliant.org

Instructions for Testing
===
1. Name file as [algorithm name].py and place it in the algorithms folder.
2. Adjust BrilliantTest.cfg with desired round minimum, and the desired amount of each algorithm to test with.
Make sure to use the same name as the algorithm file in the ```[algorithms]``` section of the config file.
3. Note: Some algorithms use scipy/numpy. Make sure that you run in an environment that has these installed.
4. Execute ```python BrilliantTest.py```