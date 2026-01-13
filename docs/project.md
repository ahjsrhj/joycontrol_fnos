这是一个前后端分离的项目，后续会合并打包为飞牛OS 的应用
飞牛应用开发文档：https://developer.fnnas.com/docs/core-concepts/framework
backend 文件夹内为后端代码，目前已有joycontrol相关的库，示例代码在 backend/run_controller_cli.py 中
前端代码在 frontend 文件夹中，目前是空的

帮我完成这个项目，提供一个模拟switch pro手柄的应用
前端页面模拟手柄的布局，点击可以按键，点一下为按下一次，点住为持续按下，直到松开
同时提供 nfc 能力，可以选择amiibo文件进行模拟，可以停止nfc模拟

首先，记录用户是否已经配对过switch，若配对过，界面显示连接和重新配对按钮，未配对过，界面显示配对按钮，
配对成功后连接 switch，界面上显示各种操作和 nfc 相关的东西
点击 nfc 后 弹窗，弹窗内显示一个文件列表，展示指定目录下的所有子文件夹内的 .bin文件列表，为amiibo文件列表，选中并确认后即装载到 nfc 上，模拟后可以取消模拟

帮我实现以上的功能，前后端都要改造
前端采用最新的ts+vite+vue3技术栈