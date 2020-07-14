import twint
import database
import pandas as pd

class Twint:
    def __init__(self):
        self.c = twint.Config()
        self.db = database.DataBase()
        self.c.Hide_output = True
        self.c.Pandas = True

    def following(self, name):
        try:
            list_of_followers = []
            self.c.Username = name
            twint.run.Following(self.c)
            Followers_df = twint.storage.panda.Follow_df
            list_of_followers = Followers_df['following'][name]

        except:
            print('Exception encountered:')
        finally:
            return list_of_followers
    def followers(self, name):
        self.c.Username = name
        twint.run.Followers(self.c)
        df = twint.storage.panda.Follow_df['Followers'][name]
        df['target'] = name
        return df
    def pull_following(self, name=None):
        if name is None:
            name = input('\nEnter name of target account: ')
        
        df = pd.DataFrame({'followers':self.following(name)})
        if len(df) != 0:
            df['name'] = name
            df = df.to_records(index=False).tolist()
            self.db.store_data(df)