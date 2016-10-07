import pandas
from sklearn import linear_model, feature_extraction

def categorical_features(row):
    d = {}
    d["STATE"] = row[1]["STATE"]
    return d

def last_poll(full_data):
    """
    Create feature from last poll in each state
    """
    
    # Only care about republicans
    repub = full_data[full_data["PARTY"] == "Rep"]

    # Sort by date
    chron = repub.sort_values(by="DATE", ascending=True)

    # Only keep the last one
    dedupe = chron.drop_duplicates(subset="STATE", keep="last")

    return dedupe
    
if __name__ == "__main__":
    # Read in the X data
    all_data = pandas.read_csv("data.csv")

    # Remove non-states
    all_data = all_data[pandas.notnull(all_data["STATE"])]

    # split between testing and training
    train_x = last_poll(all_data[all_data["TOPIC"] == '2012-president'])
    train_x.set_index("STATE")
    test_x = last_poll(all_data[all_data["TOPIC"] == '2016-president'])
    print(train_x.sort("STATE").head(5))
    test_x.set_index("STATE")
    
    # Read in the Y data
    y_data = pandas.read_csv("../data/2012_pres.csv", sep=';')
    y_data = y_data[y_data["PARTY"] == "R"]
    y_data = y_data[pandas.notnull(y_data["GENERAL %"])]
    y_data["GENERAL %"] = [float(x.replace(",", ".").replace("%", ""))
                           for x in y_data["GENERAL %"]]
    y_data["STATE"] = y_data["STATE ABBREVIATION"]
    y_data.set_index("STATE")

    train_x = y_data.merge(train_x, on="STATE",how='left')
    
    # format the data for regression
    encoder = feature_extraction.DictVectorizer()
    state_names_train = encoder.fit([{"STATE": x["STATE"]} for x in train_x.iterrows()])
    train_x = pd.concat([state_names_train, train_x], axis=1)

    state_names_test = encoder.fit([{"STATE": x["STATE"]} for x in test_x.iterrows()])
    test_x = pd.concat([state_names_text, test_x], axis=1)
    
    # fit the regression
    features = list(encoder.get_feature_names())
    features.append("VALUE")

    mod = linear_model.LinearRegression()
    mod.fit(train[features], train["GENERAL %"])

    # Write the predictions
    
