<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#demo">Demo</a></li>
  </ol>
</details>

## About The Project

BetGenius is an application that utilizes a [collaborative based filtering](https://developers.google.com/machine-learning/recommendation/collaborative/basics) recommendation system to suggest bets. The program receives a list of available markets which is used to generate a user's betting history. As such, we are able to generate users and bets to create a user-to-bet association where we can find similarities and generate bets


### Built With

* [![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
* [![tensorflow](https://img.shields.io/badge/TensorFlow-1.12-FF6F00.svg?style=flat&logo=tensorflow)](https://www.tensorflow.org)


## Getting Started

### Prerequisites

Install Python

1. Homebrew
  ```sh
  brew install python3
  ```
2. Linux
  ```
  sudo apt install python3
  ```

### Installation

1. Get a free API Key at [https:https://the-odds-api.com/](https://https://the-odds-api.com/)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install Python packages
   ```sh
   pip install tensorflow
   pip install pandas
   pip install numpy
   pip install dotenv
   ```
3. Create a .env file
    ```
    touch .env
    ```
4. Enter your API in `.env`
   ```js
   API_KEY = 'ENTER YOUR API KEY';
   ```

## Demo

1. Generate Data

```
python3 factory.py (# of records)
```

2. Fetch available markets
```
python3 client.py > markets.json
```

3. Recommend Bets
```
python3 bet_genius.py
```
