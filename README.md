## Analysis of Correct Answers Based on People's Opinions

This project analyzes the correct answer based on people's opinions about the responses given on Stack Overflow. The dataset consists of three main files: 

- `Question`: Contains the users' questions.
- `Comment`: Contains users' comments on each answer.
- `Answer`: Contains the best answer for each question.

These files are connected through `PostID`. 

## Data Preprocessing

Preprocessing is performed to prepare the data for analysis. The general preprocessing steps are as follows:

1. Remove the bodies of all `<pre>`, `<code>`, and `<blockquote>` tags.
2. Extract all text (excluding any HTML tags).
3. Replace every sequence of consecutive whitespace (spaces, tabs, line feeds) with a single space.
4. Remove all HTTP and HTTPS links.
5. Strip leading and trailing whitespace.

## Project Aim

The aim of this project is to study the correctness of answers based on people's opinions. The following steps are undertaken:

- Evaluate the answer achieved by the proposed algorithm.
- Compare it with the best answer obtained from Stack Overflow.
- Compare the results with the **Senti4SD** sentiment analysis algorithm.

  
* Open an issue on this repository for questions, feedback, and to reach out for data.

