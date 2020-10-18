# 结对编程作业：图片华容道
![language](https://img.shields.io/badge/language-python-blue)![license](https://img.shields.io/badge/license-BSD-green)![code quailty](https://img.shields.io/badge/code%20quality-A-brightgreen)

## 简介

本程序为解决图片华容道问题的AI部分。

## 运行环境

操作系统：windows10；python版本：3.7以上，依赖参照requirements.txt</br>
` pip install -r requirement.txt `

## 编译与运行

安装完依赖后可以直接运行`main.py`。</br>

`python main.py`</br>

**测试组**请修改` aiBattle.py ` 中的`teamInformation`后运行` aiBattle.py`</br>

`python aiBattle.py`

## 使用方法

* 本程序为解决图片华容道问题的AI部分，由于没有给出标准的输入格式，暂且在main.py中提供了两种使用方式：从最早给出的接口获取题目json文件（虽然好像现在被关闭了）；读取本地题目json文件（格式为最早给出的格式）。请自行在main.py文件中修改。
* **测试组**请修改` aiBattle.py ` 或`aiBattleSolveAll.py`中的`teamInformation['teamid']`和`teamInformation['token']`后运行相应程序。
* 运行`aiBattle.py`会解决特定的题目，还要自行修改`challenge_uuid`。运行`aiBattleSolveAll.py`会通过接口获取未解决的题目并一次性解决。

## 注意事项

* `main.py`中的代码为最早实现版本，考虑到了图片是F的情况，代码有很多冗余，如要运行`main.py`需要最早开放测试接口的支持。
* `aiBattle.py`和`aiBattleSolveAll.py`是为方便AI大比拼而写的代码，也可供测试组使用。

* 如需了解`aiBattle.py`和`aiBattleSolveAll.py`中代码的作用可参考`main.py`中的注释。
* 请务必保证项目文件夹中存在`record`和`target`文件夹，`record`中的文件记录解题所需数据，`target`保存裁剪下来的问题图片。
* 想到再补。