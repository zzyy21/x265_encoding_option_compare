<!--
 * @File Path    : /readme.md
 * @Project Name : x265_option_compare
 * @Author       : zzyy21
 * @Create Time  : 2021-04-26 23:01:27
 * @Modifed by   : zzyy21
 * @Last Modify  : 2021-06-08 23:17:09
 * @Description  : 
 * @Revision     : 
-->

# x265_option_compare

Compare the encoding settings of x265 video clip with the x265 default encoding settings.

It's only a draft version now...

## how to use

Export stream information using MediaInfo and drug onto `analyse.py`, or use command line `python analyse.py <mediainfo_file>`.

## default settings info

Export by MediaInfo from a clip encoded by x265 3.5+1-ce882936d default setting.

## TODO

1. ~~输入文件~~ (added in v0.12, 210608)
2. ~~参数区分 bool int float string~~ (added in v0.11, 210427)
3. 不同preset为基础
4. 参数的简单说明
