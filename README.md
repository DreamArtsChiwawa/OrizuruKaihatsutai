# README

ドリーム・アーツ インターンシップ 2017@広島本社 おりづる開発隊のチームディレクトリ。


## 何がしたいのか

週報を用いた課題解決。

具体的には週報が知話輪（ビジネスチャット）にアップロードされた時に課題欄から解決しそうな人を提示することで、その人とのアナログなコミュニケーションを取り、解決の糸口ができる（かも）。

また、自分が抱えている課題を投稿するだけでも問題を解決できる。

## ディレクトリ構成

```
-OrizuruKaihatsutai
|- AI
|- BOT
```

- AIディレクトリにはAIに関するソースコードが入っています。
- BOTディレクトリには知話輪に投稿するためのコードと、AIから呼び出すためのコードが入っています。

## 使い方

### 学習

`./AI/train.py`を実行。`train.py`内の`INPUT_DOC_DIR`項目を学習させたいドキュメント（今回の場合は週報）に変更する。また、学習させたい内容を抽出するために、幾つかのキーワードを判断する要素にしています。そのあたりの調整もする必要があります。

※ 約60,000ファイルの学習を仮想4コア/RAM16GBのマシンで30分ぐらい。（30回学習）ファイル数が多いほど時間がかかる。

また、実行できない場合は学習回数を定義している`epoch`変数の値を変更することで実行することができます。

生成された`.model`と`.npy`拡張子のファイルをBOTディレクトリにコピーしておく。

### BOTサーバ起動

環境変数をexport後、BOTディレクトリ内の`main.py`を実行。

```
export CHIWAWA_API_TOKEN='API利用トークン'
export CHIWAWA_VALIDATION_TOKEN='検証トークン'
```

### BOTの使い方

- 週報のテキストアップロード（知話輪の本文に貼り付け）
- `/tell-me （本文）`のような形での課題投稿を行う

※ 添付ファイル（Attachment）は対応しておりません。
