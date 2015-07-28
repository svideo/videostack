VideoStack：构建网路视频服务的开源软件
====================================


VideoStack是什么？
-----------------

1. VideoStack解决互联网视频上传、转码、封装、存储、分发、缓存以及随之而来的集群管理问题；

2. 为大并发视频直播以及处理海量点播内容而设计；

3. 不断追踪浏览器技术以及视频技术进展，VideoStack尽量采用最新的技术以优化用户体验；

4. 提供各平台上的浏览器视频播放，但不包括播放器软件或是播放App的实现；

5. VideoStack可以通过后台Web管理界面或VideoStackAPI来控制；



VideoStack开发方式是什么样的？
-----------------------------

1. VideoStack使用大量的，包括Python、FFmpeg、Varnish在内的开源／免费软件，使它们成为理想的基础设施。VideoStack不重复解决优秀软件已经解决的问题；

2. 发布周期为半年，期间穿插频繁的里程碑。另外，你可以从http://snapshots.videostack.org 下载到我们的每日构建版本；

3. 可以抽象出来的部分作为独立的项目来维护，如x100http、x100redis2mysql、x100FFmpegWrapper。


VideoStack开发完成了吗？
-----------------------

1. 它的版本号还没到1.0。但我们仔细设计和实现了VideoStack中现有的功能，这些已经发布的功能可以完美地工作；

2. 在后续的开发中，我们会仔细考虑旧版本API的兼容问题，尽量不破坏它。


如何体验VideoStack？
-------------------

1. 可以在http://demo.videostack.org 看到演示并操作一个小的VideoStack集群；

2. 用户名密码都是videostack，每天凌晨重置至初始状态；


如何安装VideoStack？
-------------------


使用手册在哪？
-------------

1. 设计文档 - http://docs.videostack.org/design  

2. API文档 - http://docs.videostack.org/api




VideoStack使用了哪些开源／免费的软件项目？
-----------------------------------------

VideoStack使用了以下开源项目，我们对它们的编写者们表示由衷地感谢。

FFmpeg - http://ffmpeg.org/  

Varnish - https://www.varnish-cache.org/  

Python - https://www.python.org/

