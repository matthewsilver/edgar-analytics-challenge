# edgar-analytics-challenge
Personal submission for Insight's Edgar Analytics coding challenge

### Overview

See https://github.com/InsightDataScience/edgar-analytics for more details on the coding challenge, including requirements for the answer and high-level implementation strategy.

### Strategy

Keeping track of user sessions led to me creating a dictionary structure, where the key was a user's ip address and the values the count and timestamp of documents requested. Since a user could have multiple sessions, I needed a dictionary keeping track of only active sessions, and whenever someone's session ended, I moved their entry to a dictionary keeping track of ended sessions. As an edge case, if there were still active sessions at the end of the file read in, I moved all of those entries to another session.

In order to prevent anticipated scaling issues, I read in data one line at a time rather than reading in entire files at once. While this has not been officially tested on a large dataset, based on previous work of similar nature this strategy should be successful.

### Running the program

The code that computes the metrics and runs unit tests runs in Python3. To run the program, first put the desired inactivity_period.txt and log.csv files in the top-level input folder, as described in the assignment. Then run the command *run.sh* which will execute the command
> python3 ./src/sessionization.py ./input/inactivity_period.txt ./input/log.csv ./output/sessionization.txt

If you would like to run the test cases on the selected input and output data, go to *insight_testsuite* and run *run_tests.sh* in the same way the original instructions stated.

To run the unit tests, navigate to the *src* directory and run the following line:

> python3 unit_tests.py ../input/sessionization.txt ../input/log.csv ../output/sessionization.txt

### Notes

Currently, the unit tests and test cases are not functioning. It is not recommended to run them until they are fully functional.


