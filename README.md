# QTML - 免费的我的世界启动器


## 帮助我们更好的发展

1. 可以去我们的Github存储库做出贡献 (就在这里)
2. 去爱发电赞助我们 [传送门](https://afdian.net/@chenmy1903)
3. 提出bug [在issues上](https://github.com/chenmy1903/QTML/issues)

### 更新了什么?

> 差不多就是重做了

1. 更快的下载速度 (请支持[bangbang93](https://afdian.net/@bangbang93)来让他继续为我们提供下载服务)
2. 解除收费内容 (改为自愿支持[鸭皇](https://afdian.net/@chenmy1903), 请支持他, 他是这个项目的作者)
<!-- 3. 对我的世界基岩版的支持 -->
3. 毛玻璃效果

## 我们修复了[Minecraft-Launcher-Lib](https://minecraft-launcher-lib.readthedocs.io/)的bug

1. 修复微软登录错误的bug
2. 修复在中国下载如龟速的特性

### 如果Minecraft-Launcher-Lib的作者想看看怎么修复, 来看这里

在`microsoft_account.py`文件的39行中, 在修复前的代码是这样的

```python
parameters = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": auth_code,
        "grant_type": "authorization_code",
    }
```

但是这个地方不应该存在`client_secret`

修改后它是这样的

```python
parameters = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code": auth_code,
        "grant_type": "authorization_code",
    }
```



### If the author of minecraft launcher lib wants to see how to fix it, check out here

In file `microsoft_account.py` on line 39, it like this

```python
parameters = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": auth_code,
        "grant_type": "authorization_code",
    }
```

You will delete `client_secret`, code is like this

```python
parameters = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code": auth_code,
        "grant_type": "authorization_code",
    }
```
