## 知話輪ボット

created by Team OrizuruKaihatutai

### 概要

知話輪とAI部分をつなぐためのシステム

### 使い方

環境変数をセットして起動

```shell
$ export CHIWAWA_VALIDATION_TOKEN='XXXXXXXXXXXXXXXXXXXX'
$ export CHIWAWA_API_TOKEN='XXXXXXXXXXXXXXXXXXXX'
$ python main.py
```

- CHIWAWA_VALIDATION_TOKENにはWebhook検証トークンを記載してください。
- CHIWAWA_API_TOKENにはAPIトークンを記載してください。
- これらの情報は外部に漏れた場合、知話輪を自由に使うことができる可能性があります。その点を理解した上で使用してください。
