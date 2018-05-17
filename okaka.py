import twitter
import os
import os.path
from importlib import import_module

class Okaka:

    # 該当拡張子のコンフィグファイルを読み込む（仕様により名無しファイル（拡張子だけ）は読まない）
    def load_secret_config():
        self.config = {}

        config_ext = [".config", ".config_secret"] #コンフィグファイル用拡張子一覧

        for filename in os.listdir():
            # 拡張子から該当ファイルがコンフィグファイルであるか判別
            if os.path.splitext(filename)[1] in config_ext:
                file = open(filename, "r")
                lines = file.readlines()
                for line in lines:
                    token = line.split()
                    if len(token) == 0 : continue #空白列
                    if token[0][0] == "#" : continue  #コメント
                    if len(token) == 2:
                        self.config[token[0]] = token[1]
                    else:
                        print("Can"t read config [{}] . Be sure format is correct.".format(token[0]))
    
    # Twitterへのアクセサの作成
    def load_twitter():
        # OAuthトークンの存在を確認
        if  "twitter_api_key" not in self.config || 
            "twitter_api_secret" not in self.config ||
            "twitter_access_token" not in self.config ||
            "twitter_access_secret" not in self.config:
            print("Twitter tokens missed. Be sure config exists.")
            return 1

        # OAuth認証
        auth = twitter.OAuth(
            consumer_key=_config["twitter_api_key"],
            consumer_secret=_config["twitter_api_secret"],
            token=_config["twitter_access_token"],
            token_secret=_config["twitter_access_secret"])
        
        self.t = twitter.Twitter(auth=auth)

    if __name__ == "__main__":
        # コンフィグ読み込み
        load_secret_config()

        # Twitter認証
        load_twitter()