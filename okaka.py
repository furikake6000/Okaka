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
  print(_config)