```
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
- [Example :memo:](#example-memo)
- [Restrictions :ghost:](#restrictions-ghost)
- [Contact :tophat:](#contact-tophat)

## About :speaker:

If you want a different approach than following your logs by typing print between codes, here is **Logges**.

With **Logges**, you can follow your logs that you want to follow, whether you print them on the screen or not, and automate your log outputs by making these log outputs as **PDF** or **MarkDown** extensions.
## Installation :open_file_folder:

You can install Logges with typing `pip install Logges` on Python package managers/terminal. (*Docker file will be here as soon as possible*)

## Example :memo:

* :pushpin: Step 1: Import package as `from Logges import Logges`
* :pushpin: Step 2: Initially, You have to setup your log file as `Logges.setup(__file__)` in the run script/method.
* :pushpin: Step 3: Log your outputs/logs with `Logges.log()` method. You can use 3 different status message, and show or hide your logs with `print_log` parameter.
  * :gem: Status = 0 for information logs.
  * :gem: Status = 1 for warning logs.
  * :gem: Status = 2 for error logs.
* :pushpin: Step 4: At the and, use the `to_markdown()` or `to_pdf()` method for saving your logs. (If you want just show your logs at console, use `console_data()` method.)

Check our [example](examples) scripts to understand how to use.

## Restrictions :ghost:

Please do not use dash (-) character on your script name. If you want to use that character, markdown and pdf inside header will change dash to dot. (For beauty.)

## Contact :tophat:

[Serkan UYSAL](https://github.com/uysalserkan) - [Özkan UYSAL](https://github.com/ozkanuysal)
