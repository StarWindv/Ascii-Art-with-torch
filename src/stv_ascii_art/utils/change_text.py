# MIT License
# Copyright (c) 2025 星灿长风v

import os
from stv_utils import system_check
from stv_utils import is_ch


def get_config_path():
    if system_check():
        config_path = os.path.join(os.environ['LOCALAPPDATA'], "stv_language.config")
    else:
        config_path = os.path.join(os.environ['HOME'], ".stv_language.config")
    return config_path


def language_config():

    config_path = get_config_path()

    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "chinese" or "zh-cn" in str(content).lower():
            return True


def set_cn(code, show_info = False):
    available_path = ["zh-cn", "chinese"]
    if code.lower() in available_path:
        config_path = get_config_path()
        with open(config_path, 'w', encoding="utf-8") as f:
            f.write(code)
        if show_info:
            print("\033[96m已将语言设置为中文\033[0m")
    else:
        print("\033[31m不支持的语言代码\033[0m")
        print(available_path)


def parse_text(check = False):

    if check:
        check = language_config()

    if is_ch() or check:
        title = '========= 星灿长风v & CLI-ASCII Art 生成器 ========='
        input_help = '输入文件路径'
        output_help = '目标输出文件主目录'
        video_help = '启用视频模式'
        enhance_help = '启用增强模式'
        export_help = '输出处理后的视频'
        gpu_help = '启用GPU加速模式'
        license_help = '输出项目所用的许可证'
        solidify_help = '固定字号为输入值(x, y)'
        version_help = '输出项目版本'
        reset_language = '清除语言设置'
    else:
        title = '========= StarWindv & CLI-ASCII Art Generator ========='
        input_help = 'Input file path'
        output_help = 'Target output directory'
        video_help = 'Enable video mode'
        enhance_help = 'Enable enhancement mode'
        export_help = 'Export processed video'
        gpu_help = 'Enable GPU acceleration'
        license_help = 'Output the licenses used'
        solidify_help = 'Fixed font size is the entered value.(x, y)'
        version_help = 'Project version'
        reset_language = 'Clear language settings'

    language_help = "设置帮助语言为中文"

    array = [title, input_help, output_help,
             video_help, enhance_help, export_help,
             gpu_help, license_help, solidify_help,
             version_help, language_help, reset_language]

    return array


def beautiful_parse_text(check = False):

    from stv_utils import is_ch

    if check:
        check = language_config()

    if is_ch() or check:
        help_text = '展示此帮助信息并退出'
        io_help = '输入/输出选项'
        process_help = '处理选项'
        high_help = "高级选项"
        system_help = '系统选项'

    else:
        help_text = 'Show this help message and exit'
        io_help = 'Input/Output Options'
        process_help = 'Process Options'
        high_help = "Advanced Options"
        system_help = 'System Options'

    array = [help_text, io_help, process_help,
             high_help, system_help]

    return array