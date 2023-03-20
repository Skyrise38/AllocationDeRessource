import pandas as pd

def classer_dataframe(df) :
    df = df.iloc[df.iloc[:, 0].argsort()]
    return df


X = pd.read_excel("attribution sujets.xlsx")

X.iloc[:, 1:] = X.iloc[:, 1:].where(X.iloc[:, 1:] == 1, other=10)
print(X)

##X= X.sample(frac=1)

#print (Y)
##df = classer_dataframe(Y)
#print(df)