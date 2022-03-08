# GneListBackend

 接收从 GneList 发来的数据

## 运行方式

本项目依赖 MongoDB。请确保你本地安装了 MongoDB，并且可以使用`mongodb://localhost`连接。
如果你的 MongoDB 不在本地，或者在本地但有账号密码，请在 `config`文件夹
中创建一个 `prod.yml` 文件，并模仿 `local.yml`填写链接 URI 和 db、col。


```bash
pipenv install
pipenv shell
export prod # 你自己创建的 yml文件的名字
uvicorn main:app --port 8800 --host 0.0.0.0  # 使用8800端口
```