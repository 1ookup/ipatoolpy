参考： https://github.com/majd/ipatool

使用python改写

增加支持:

* [x] 支持linux(理论支持windows未测试)
* [x] 支持查询历史版本号
* [x] 支持历史版本下载
* [x] 支持http请求增加代理支持(http/socks)

## Requirements:

python3

## Installation

pip install ipatoolpy

## Usage

```bash
$ ipatoolpy 
Usage: ipatoolpy [OPTIONS] COMMAND [ARGS]...

  A cli tool for interacting with Apple's ipa files.

Options:
  --debug / --no-debug
  -p, --proxy TEXT      http proxy
  --help                Show this message and exit.

Commands:
  appinfo   Show app info and history versions
  auth      Authenticate with the App Store.
  download  Download (encrypted) iOS app packages from the App Store.
  purchase  Obtain a license for the app from the App Store.
  search    Search for iOS apps available on the App Store.
  version   Display the current version.

```

### auth (登录授权，使用-c参数指定登录地区)

`ipatool auth login -e xxxx@hotmail.com -p ssssss`

登录后二次认证可能无法触发通知，可以自行在手机设置中->Apple ID->密码与安全性->获取验证码按钮获取

### search (搜索App)

`ipatool search twitter`

### appinfo （查看App信息和历史版本号）

`ipatool appinfo -b com.twitter.xxxxxx`

### purchase (App第一次下载需要先购买)

`ipatool purchase -b com.twitter.xxxxxx`

### download （下载App）

下载最新版本

`ipatool download -b com.twitter.xxxxxx`

下载历史版本, -e 参数为 appinfo参数中获取到的版本号

`ipatool download -c US -b com.alipay.iphoneclient -e 849878646`

### 代理使用

`ipatool -p socks5://127.0.0.1:7890 download -c US -b xxxxx -e xxxxx`

## 注意

guid参数为网卡mac地址，如果获取不到网卡地址后使用默认guid

如果使用windows没有测试过是否可以获取网卡mac计算出guid，可以使用手动指定guid

`ipatool -g BCD016081FF0 download -c CN -b xxxxx -e xxxxx`
