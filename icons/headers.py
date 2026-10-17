import os
import platform
from icons.colors import *

def clean_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def header_tools():
    print(f"""{r}*****************************************************************{rs}
{r}*{rs}                                                               {r}*{rs}
{r}*{rs}                           {c}KEY WIFI{rs}                            {r}*{rs}
{r}*{rs}                  {b}https://github.com/keydo5507-del/key-tols{rs}               {r}*{rs}
{r}*{rs}            {y}Tools that perform DOS on Wifi networks{rs}            {r}*{rs}
{r}*{rs}                      {g}Develop by Key{rs}                           {r}*{rs}
{r}*{rs}                                                               {r}*{rs}
{r}*****************************************************************{rs}""")
