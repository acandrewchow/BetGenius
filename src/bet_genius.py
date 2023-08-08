import random
import numpy as np
import json
import pandas as pd
import tensorflow as tf
from keras import Model

# Loads a CSV into a data frame
def load_data(file_path):
    return pd.read_csv(file_path)

def create_user_bets_matrix(data):
    # unique users and bets
    users = data["User"].unique()
    bets = data["Bet"].unique()

    # fill matrix with 0s
    user_bets_matrix = np.zeros((len(users), len(bets)), dtype=int)

    # user-bet-association
    for _, row in data.iterrows():
        user = row["User"]
        bet = row["Bet"]
        user_index = np.where(users == user)[0][0]
        bet_index = np.where(bets == bet)[0][0]
        user_bets_matrix[user_index, bet_index] = 1

    return user_bets_matrix


# Builds the model using collaborative-based filtering
def build_model(num_users, num_bets, input_length=8):
    user_input = tf.keras.layers.Input(shape=(1,))
    bet_input = tf.keras.layers.Input(shape=(1,))

    user_embedding = tf.keras.layers.Embedding(
        input_dim=num_users, output_dim=input_length
    )(user_input)
    bet_embedding = tf.keras.layers.Embedding(
        input_dim=num_bets, output_dim=input_length
    )(bet_input)

    user_vector = tf.keras.layers.Flatten()(user_embedding)
    bet_vector = tf.keras.layers.Flatten()(bet_embedding)

    dot_product = tf.keras.layers.Dot(axes=1)([user_vector, bet_vector])

    concat = tf.keras.layers.Concatenate()([user_vector, bet_vector, dot_product])
    output = tf.keras.layers.Dense(1, activation="relu")(concat)
   
    model = Model(inputs=[user_input, bet_input], outputs=output)
    model.compile(optimizer="adam", loss="mse") 

    return model


# Trains the models with the given number of users and bets
def train_model(num_users, num_bets):
    user_ids, bet_ids = np.meshgrid(np.arange(num_users), np.arange(num_bets))
    interactions = user_bets_matrix.flatten()

    model.fit([user_ids.flatten(), bet_ids.flatten()], interactions, epochs=25, batch_size=16)

# Converts a list of bets (bet_ids) to generate a betslip
def create_betslip(recommended_bets):
    betslip = ""
    for bet in recommended_bets:
        bet_info = bet_attributes[bet_attributes["Bet"] == bet].iloc[0]
        outcome = bet_info["Outcome"]
        if outcome == "W":
            betslip += f"{bet}\n"
            for col, value in bet_info.items():
                if col != "Bet":
                    betslip += f"{col}: {value}\n"
    return betslip

# Predicts bets for a specific user 
def predict_bets():
    user_to_recommend = 2 # user_id
    bets_to_recommend = np.arange(num_bets)
    recommendations = model.predict(
        [np.full(num_bets, user_to_recommend), bets_to_recommend]
    )
   
    sorted_recommendations = np.argsort(recommendations.flatten())[::-1]
    
    # retrieves bets in the recommendation bets 
    recommended_betslip = create_betslip(
        [bet_attributes.iloc[bet]["Bet"] for bet in sorted_recommendations]
    )

    return recommended_betslip

# Parses a bet slip and returns a list of bets
def parse_bet_slip(betslip):
    attributes = [
        bet.split(": ", 1)[1]
        for bet in betslip.split("\n")
        if bet.startswith(("Type:", "League:", "Team:", "Market_Type:"))
    ]
    
    list_of_bets = []

    for i in range(len(attributes)):
        if attributes[i] == "h2h":
            betslip = {
                "Bet Type": attributes[i - 3],
                "League": attributes[i - 2],
                "Team": attributes[i - 1],
                "Market Type": attributes[i],
            }
            list_of_bets.append(betslip)
    return list_of_bets


# Loads a JSON file filled with markets into a python dictionary
def load_markets():
    with open("markets.json", "r") as file:
        available_markets = json.load(file)
    return available_markets


# Returns the available market which contains the recommended league/team
def search_markets(league, team, market_type, available_markets):
    for market in available_markets:
        if market["winning_team"] == team and market["sport_title"] == league:
            return market

if __name__ == "__main__":
    user_data = load_data("test/users.csv")
    bet_attributes = load_data("test/bet_attributes.csv")
    # bet_attributes = load_data("test/users/seasonal_baseball_user.csv")
    
    user_bets_matrix  = create_user_bets_matrix(user_data)

    num_users = user_bets_matrix.shape[0]
    num_bets = user_bets_matrix.shape[1]

    # Encode data using one hot encoding
    encoded_user_data = pd.get_dummies(user_data, columns=["User", "Bet"])
    encoded_bet_attributes = pd.get_dummies(
        bet_attributes, columns=["Outcome", "Type", "Sport", "League", "Team", "Market_Type"]
    )
    
    # build the model
    model = build_model(num_users, num_bets)

    # train the model
    train_model(num_users, num_bets)

    betslip = predict_bets()

    list_of_bets = parse_bet_slip(betslip)
  
    available_markets = load_markets()

    betslips = []

    for bet in list_of_bets:
        betslip = search_markets(
            bet["League"], bet["Team"], bet["Market Type"], available_markets
        )
        if betslip != None:
            betslips.append(betslip)
    formatted_betslip = json.dumps(betslips, indent=4)

    print(formatted_betslip)
