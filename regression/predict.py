import pandas

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
    
    # Read in the Y data
    y_data = pandas.read_csv("../data/2012_pres.csv", sep=';')
    y_data = y_data[y_data["PARTY"] == "R"]
    y_data = y_data[pandas.notnull(y_data["GENERAL %"])]
    y_data["GENERAL %"] = [float(x.replace(",", ".").replace("%", ""))
                           for x in y_data["GENERAL %"]]
    y_data["STATE"] = y_data["STATE ABBREVIATION"]


    # split between testing and training
    train_x = last_poll(all_data[all_data["TOPIC"] == '2012-president'])
    test_x = last_poll(all_data[all_data["TOPIC"] == '2016-president'])
    print(train_x.sort("STATE").head(5))

    # format the data for regression
    


    # fit the regression
    

    # Write the predictions
