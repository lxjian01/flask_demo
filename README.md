## python版本
python 3.6.4
runserver --host=0.0.0.0 --port=8003

## VirutalEnv
pip install virtualenv  
添加环境变量  
mkdir /opt/venv  
/usr/local/python3/bin/virtualenv -p /usr/bin/python3 flask_demo


## 生成requirements.txt
* 生成架包依赖文件  
(venv) /opt/code/flask_demo>pip freeze > requirements/linux.txt
* 安装依赖架包  
(venv) /opt/code/flask_demo>pip install -r requirements/linux.txt

## linux设置运行环境
export FLASK_ENV="dev"
