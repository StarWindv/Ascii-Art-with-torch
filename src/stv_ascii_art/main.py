# MIT License
# Copyright (c) 2025 星灿长风v

# import locale
# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

__version__ = '0.1.5'

def main(__version__ = __version__):
    from stv_ascii_art.core.stv_parse import stv_parse
    args = stv_parse()

    if args.license:
        from stv_ascii_art.utils.lic import return_license
        print(return_license())
        return

    if args.version:
        print(__version__)
        return

    if args.set_language:
        from stv_ascii_art.utils.change_text import set_cn
        set_cn("zh-cn")
        print("\033[96m帮助语言已更新为中文\033[0m")
        return

    if args.reset_language:
        from stv_ascii_art.utils.change_text import get_config_path
        config_path, os = get_config_path()
        if os.path.exists(config_path):
            os.remove(config_path)
        from stv_utils import is_ch
        if is_ch():
            print(f"语言设置已清除")
        else:
            print(f"Language settings have been cleared")
        return


    if args.video:
        from stv_ascii_art.core.video_processor import handle_video
        handle_video(
            args.input,
            enhanced=args.enhanced,
            export=args.export,
            output_path=args.output,
            use_gpu=args.gpu
        )
    else:
        from stv_ascii_art.core.image_processor import handle_image
        handle_image(
            args.input,
            output_path=args.output,
            enhanced=args.enhanced,
            use_gpu=args.gpu
        )


if __name__ == "__main__":
    main()