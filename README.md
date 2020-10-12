结对编程作业：图片华容道</br></br>
![language](https://img.shields.io/badge/language-python-blue)
![license](https://img.shields.io/badge/license-BSD-green)
![code quailty](https://img.shields.io/badge/code%20quality-A-brightgreen)
# 运行环境
操作系统：windows10；python版本：3.7以上，依赖参照requirements.txt</br>
` pip install -r requirement.txt `
# 编译与运行
安装完依赖后可以直接运行main.py
# 使用方法与注意事项
* 本程序为解决图片华容道问题的AI部分，由于没有给出标准的输入格式，暂且提供了两种使用方式：从接口获取题目json文件；读取本地题目json文件。请自行在main.py文件中修改。
* 本次实现的过程和拼拼图一样，很多代码只是为了得到相应的数据，写完只运行了一次，可以忽略它们。
* 请务必保证项目文件夹中存在`record`和`target`文件夹，`record`文件夹中的内容为程序运行提供所需要的数据，`target`文件夹为所裁剪问题图片的保存路径。
* 程序输出前会向答案接口提交答案，但目前不知道为什么一直提交失败，只能用接口测试工具进行测试，所以会输出Json格式的答案，便于使用接口测试工具。
* 程序中暂时存在很多调试代码，还没有为AI大比拼做出调整，在AI大比拼阶段会进一步完善。
* 想到再补。