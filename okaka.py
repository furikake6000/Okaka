import twitter
import os
import os.path

_config = {}

# 該当拡張子のコンフィグファイルを読み込む（仕様により名無しファイル（拡張子だけ）は読まない）
def load_secret_config():
  config_ext = ['.config', '.config_secret']  #コンフィグファイル用拡張子一覧

  for filename in os.listdir():
    # 拡張子から該当ファイルがコンフィグファイルであるか判別
    if os.path.splitext(filename)[1] in config_ext:
      file = open(filename, 'r')
      lines = file.readlines()
      for line in lines:
        token = line.split()
        if len(token) == 0 : continue #空白列
        if token[0][0] == '#' : continue  #コメント
        if len(token) == 2:
          _config[token[0]] = token[1]
        else:
          print("Can't read config [" + token[0] + "] . Be sure format is correct.")

if __name__ == '__main__':
  #コンフィグ読み込み
  load_secret_config()
  
  #OAuth認証
  auth = twitter.OAuth(
    consumer_key=_config['twitter_api_key'],
    consumer_secret=_config['twitter_api_secret'],
    token=_config['twitter_access_token'],
    token_secret=_config['twitter_access_secret'])

  #アクセサ作成
  t = twitter.Twitter(auth=auth)
  t_stream = twitter.TwitterStream(auth=auth, domain='userstream.twitter.com')

  #TLに流れてくるたびに反応
  for msg in t_stream.user():
    if 'in_reply_to_screen_name' in msg and msg['in_reply_to_screen_name'] == _config['twitter_account']:
      #リプライ
      if msg['user']['id_str'] == _config['admin_id']:
        #管理者からのリプライ
        tweet = "@"+msg['user']['screen_name']+" "+"こんにちは、管理者さん。"
        t.statuses.update(status=tweet, in_reply_to_status_id=msg['id_str'])
      else:
        #管理者以外からのリプライ
        tweet = "@"+msg['user']['screen_name']+" "+"こんにちは、" + msg['user']['name'] + "さん。"
        t.statuses.update(status=tweet, in_reply_to_status_id=msg['id_str'])