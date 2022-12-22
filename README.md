# sd_merge_numa
batch for sdweb-merge-block-weighted-gui

- SSDのバックアップは忘れずに

## これは何？

- マージする
- 画像出す
- (マージしたモデルを消す)

を指定された分だけ繰り返すバッチスクリプトやで

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
7. ストレージ容量に自信があるなら Delete Merged Model each time をオフにすればモデルが全部残る
8. txt2imgの Generate ボタンを押す
9. 寝る

## 生成画像の比較

あとからX/Y plot画像を作るのはこれが便利

Fake X/Y plot
https://github.com/aka7774/sd_fake_xyplot

### 生成画像の確認

- どの画像がどの設定だったかは PNG Info で確認することができます

## History Formatの編集

- Googleスプレッドシートを使うと便利だと思う

## モデルの選択

- ファイル名に一致するモデルを使用します
  - ハッシュは無視します

同じハッシュのモデルばかりで困ったときは

Filer
https://github.com/aka7774/sd_filer

- sha256が計算できる

Infotext Ex
https://github.com/aka7774/sd_infotext_ex

- PNG Infoにsha256を残せる

Infotexts
https://github.com/aka7774/sd_infotexts

- PNG Infoに残ったsha256を使って画像を生成できる
