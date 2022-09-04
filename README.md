```txt
LLLLLLLLLLL                                                                                            SSSSSSSSSSSSSSS
L:::::::::L                                                                                          SS:::::::::::::::S
L:::::::::L                                                                                         S:::::SSSSSS::::::S
LL:::::::LL                                                                                         S:::::S     SSSSSSS
  L:::::L                  ooooooooooo      ggggggggg   ggggg   ggggggggg   ggggg    eeeeeeeeeeee   S:::::S
  L:::::L                oo:::::::::::oo   g:::::::::ggg::::g  g:::::::::ggg::::g  ee::::::::::::ee S:::::S
  L:::::L               o:::::::::::::::o g:::::::::::::::::g g:::::::::::::::::g e::::::eeeee:::::eeS::::SSSS
  L:::::L               o:::::ooooo:::::og::::::ggggg::::::ggg::::::ggggg::::::gge::::::e     e:::::e SS::::::SSSSS
  L:::::L               o::::o     o::::og:::::g     g:::::g g:::::g     g:::::g e:::::::eeeee::::::e   SSS::::::::SS
  L:::::L               o::::o     o::::og:::::g     g:::::g g:::::g     g:::::g e:::::::::::::::::e       SSSSSS::::S
  L:::::L               o::::o     o::::og:::::g     g:::::g g:::::g     g:::::g e::::::eeeeeeeeeee             S:::::S
  L:::::L         LLLLLLo::::o     o::::og::::::g    g:::::g g::::::g    g:::::g e:::::::e                      S:::::S
LL:::::::LLLLLLLLL:::::Lo:::::ooooo:::::og:::::::ggggg:::::g g:::::::ggggg:::::g e::::::::e         SSSSSSS     S:::::S
L::::::::::::::::::::::Lo:::::::::::::::o g::::::::::::::::g  g::::::::::::::::g  e::::::::eeeeeeee S::::::SSSSSS:::::S
L::::::::::::::::::::::L oo:::::::::::oo   gg::::::::::::::g   gg::::::::::::::g   ee:::::::::::::e S:::::::::::::::SS
LLLLLLLLLLLLLLLLLLLLLLLL   ooooooooooo       gggggggg::::::g     gggggggg::::::g     eeeeeeeeeeeeee  SSSSSSSSSSSSSSS
                                                     g:::::g             g:::::g
                                         gggggg      g:::::g gggggg      g:::::g
                                         g:::::gg   gg:::::g g:::::gg   gg:::::g
                                          g::::::ggg:::::::g  g::::::ggg:::::::g
                                           gg:::::::::::::g    gg:::::::::::::g
                                             ggg::::::ggg        ggg::::::ggg
                                                gggggg              gggggg

```

![PyPI - Downloads](https://img.shields.io/pypi/dm/logges?label=Downloads&logo=monthly_download&style=flat-square) ![Scrutinizer code quality (GitHub/Bitbucket)](https://img.shields.io/scrutinizer/quality/b/uysalserkan/logges/main?style=flat-square) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/uysalserkan/logges?style=flat-square) ![Scrutinizer coverage (GitHub/BitBucket)](https://img.shields.io/scrutinizer/coverage/b/uysalserkan/logges/main?style=flat-square) ![GitHub](https://img.shields.io/github/license/uysalserkan/logges?style=flat-square) ![GitHub forks](https://img.shields.io/github/forks/uysalserkan/logges?style=social) ![GitHub Repo stars](https://img.shields.io/github/stars/uysalserkan/logges?style=social) ![PyPI](https://img.shields.io/pypi/v/logges?style=flat-square)

- [About :speaker:](#about-speaker)
- [Installation :open_file_folder:](#installation-open_file_folder)
- [Usage :memo:](#usage-memo)
  - [Library :closed_book:](#library-closed_book)
  - [CLI :clipboard:](#cli-clipboard)
- [Encountered Bugs :ghost:](#encountered-bugs-ghost)
- [Contact :tophat:](#contact-tophat)

## About :speaker:

If you want a different approach than following your logs by typing print between codes or do not want to use `logging` library, here is **Logges**.

With **Logges**, you can follow your logs that you want to follow, whether you print them on the screen or not, and automate your log outputs by making these log outputs as **LOG**, **PDF**, **MD** or **Zip**ped file.

## Installation :open_file_folder:

You can install Logges with typing `pip install Logges` on Python package managers/terminal. (_Docker file will be here as soon as possible_)

## Usage :memo:

### Library :closed_book:

![console image](/imgs/img_2.png)

- :pushpin: Import package as `from Logges import Logges`
- :pushpin: Firstly, Optional parameter is `Logges.setup()`. You can name your log file with `logname` parameter and print logs with `status` parameters (Default is `Logges.LogStatus.ERROR`).
- :pushpin: We have 5 log type under LogStatus enums;
  - :gem: LogStatus.DEBUG
  - :gem: LogStatus.INFO
  - :gem: LogStatus.WARNING
  - :gem: LogStatus.ERROR
  - :gem: LogStatus.CRITICAL
- :pushpin: Before add logs, you can ignore specific files and directories on your logs with using `ignore_files()` method.
- :pushpin: You can check in entered logs messages with `in_log()` method with `keyword` parameter. It returns `True` or `False` if keywords in log messages.
- :pushpin: Finally, you can add your logs with `log()` method with specific parameters.
  - :heavy_plus_sign: `msg` parameter defines your messages, alsa could be a variable which can be print.
  - :heavy_plus_sign: `status` parameter defines your log type. Default is **DEBUG** but you can change it with LogStatus enums.
  - :heavy_plus_sign: `print_log` default is `False`, if your status is equal or upper than `status` of `setup` parameter, it will also print if you set it `False`.
- :pushpin: Also you can export your logs as `log`, `md`, `pdf` or `zip` files, which is exported as `md, pdf, log`.

Check our [example](examples) scripts to understand how to use.

### CLI :clipboard:

![console image](/imgs/img_1.png)

- :pushpin: Also we have an CLI tool about log files.
- :pushpin: `logges` is main command for listing, showing, searching operations.
- :pushpin: `logges list` has 2 optional parameter for listing log files.
  - :gem: `--max-date` is filtering logs with maximum date.
  - :gem: `--min-date` is filtering logs with minimum date.
  - :gem: Please enter your date format as _YYYY-MM-DD_
- :pushpin: `logges show` is showing entered filename.
  - :gem: `-f`/`--file` parameter is defines the log filename which is showing on `list` command or local file.
  - :gem: `--local_file` parameter default is `False`, if you want to see your local log file, you need to set this parameter `True`.
- :pushpin: `logges search` is filtering command in all log files.
  - :gem: `--max-date` is filtering logs with maximum date.
  - :gem: `--min-date` is filtering logs with minimum date.
  - :gem: `-sen`/`--sentences` is REQUIRED parameter for filtering. It search keywords (seperated with `,`) in log messages.
  - :gem: `-fun`/`--functions` is filtering functions on logs.
  - :gem: `-sta`/`--status` is filtering status on log.
  - :gem: `-fi`/`--files` is filtering executed files in log file.
  - :gem: `-e`/`--export` if you want to export result, set this parameter `True`.
  - :gem: `--export_name`, if you set `--export=True`, it defines exported file name.

## Encountered Bugs :ghost:

If you find any bug or want to a feature nice-to-have, do not hesitate open an [**issue page**](https://github.com/uysalserkan/Logges/issues/new).

## Contact :tophat:

[Serkan UYSAL](https://github.com/uysalserkan) - [Özkan UYSAL](https://github.com/ozkanuysal)
