# SCP-JP integrated management system

## 注意

proxyサーバーを使用している場合、以下のように設定してください。

```example_site.conf
proxy_set_header   Host             $host;
proxy_set_header   X-Real-IP        $remote_addr;
proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
```

## IDEAにおけるプロジェクト構造

### ソースフォルダ

* frontend
* backend
* bot

### 名前空間パッケージ

* db
