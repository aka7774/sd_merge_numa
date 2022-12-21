# sd_merge_numa
batch for sdweb-merge-block-weighted-gui

- SSDのバックアップは忘れずに

## あそびかた

1. まず sdweb-merge-block-weighted-gui を入れる
  - https://github.com/bbc-mc/sdweb-merge-block-weighted-gui
2. マージをするとhistoryファイルを出力する
  - extensions\sdweb-merge-block-weighted-gui\csv\history.tsv
3. 次にこのExtensionを入れる
4. txt2imgタブでテスト出力したい画像の設定をする
  - Seedは固定すると良い
  - VAE, Hypernetをはじめすべての設定を使うので不要なものはオフに
5. Scriptドロップダウンで Merge Numa を選択
6. history.tsv と同じ形式でマージしたい内容を記述する
7. txt2imgの Generate ボタンを押す
8. 寝る

## 生成画像の比較

- 残念ながら X/Y Plotを使うにはモデルを削除しないで残す必要があります
  - weights 25個を1つずつ調べるだけでも25*4GBくらい必要になる
  - 余裕があるなら Delete Merged Model each time をオフにすれば残ります
- どの画像がどの設定だったかは PNG Info で確認することができます

## モデルの選択

- ファイル名に一致するモデルを使用します
  - ハッシュは無視します
