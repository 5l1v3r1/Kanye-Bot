import asyncio
import os
import discord
import youtube_dl

from discord.utils import get
from youtube_dl import DownloadError

from SRC.utilites import get_random_gif

list_of_albums = ["college dropout", "collegedropout", "cd", "late registration", "lateregistration", "lr",
                  "graduation", "gr", "808s & heartbreaks", "808s and heartbreaks", "808's & heartbreaks",
                  "808's and heartbreaks", "808", "808s", "808's", "my beautiful dark twisted fantasy", "mbdtf",
                  "watch the throne", "wtt", "yeezus", "the life of pablo", "tlop", "pablo", "ye", "kids see ghosts",
                  "ksg", "jesus is king", "jik", "sunday service", "ss"]
playlists_of_albums = ["https://www.youtube.com/playlist?list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh",  # cd
                       "https://www.youtube.com/playlist?list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7",  # lr
                       "https://www.youtube.com/playlist?list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql",  # grad
                       "https://www.youtube.com/playlist?list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t",  # 808
                       "https://www.youtube.com/playlist?list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C",  # mbdtf
                       "https://www.youtube.com/playlist?list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb",  # wtt
                       "https://www.youtube.com/playlist?list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t",  # yeezus
                       "https://www.youtube.com/playlist?list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b",  # tlop
                       "https://www.youtube.com/playlist?list=PLAUxsgLNM2Bt8apMzywvdzOJSzlfW4OQa",  # ye
                       "https://www.youtube.com/playlist?list=PLzMq4yH_FvVaq5TFtfCDs6FxWef45gyHW",  # ksg
                       "https://www.youtube.com/playlist?list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK",  # jik
                       "https://www.youtube.com/playlist?list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo"]  # ss

cd = ['https://www.youtube.com/watch?v=OTZzjAU0Kg0&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=0Tdpq3FRGhY&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=tbmNuB7spmA&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=uHcP8XX5IJA&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=psb2dFToHLA&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=mn77gzjBl1U&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=1fpkdSfPzio&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=p4NvOKy7GOU&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=9&amp;t=0s', 'https://www.youtube.com/watch?v=UHpaLbhk8vM&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=10&amp;t=0s', 'https://www.youtube.com/watch?v=hLeS2By_zPE&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=11&amp;t=0s', 'https://www.youtube.com/watch?v=IzNunT2AOO4&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=12&amp;t=0s', 'https://www.youtube.com/watch?v=pwkYUhePecQ&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=13&amp;t=0s', 'https://www.youtube.com/watch?v=E3dWKq3s6u0&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=14&amp;t=0s', 'https://www.youtube.com/watch?v=g9xopViBKOQ&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=15&amp;t=0s', 'https://www.youtube.com/watch?v=-MOIPnu50O4&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=16&amp;t=0s', 'https://www.youtube.com/watch?v=7xL9VLARq8k&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=17&amp;t=0s', 'https://www.youtube.com/watch?v=ufN8MxyMlEQ&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=18&amp;t=0s', 'https://www.youtube.com/watch?v=cgo2IKS4inU&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=19&amp;t=0s', 'https://www.youtube.com/watch?v=AE8y25CcE6s&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=20&amp;t=0s', 'https://www.youtube.com/watch?v=JwAjANmjajc&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=21&amp;t=0s', 'https://www.youtube.com/watch?v=cpbeS15sHZ0&amp;list=PLeO-rHNGADqzCkDOyEUZbJMnuu5s9yIGh&amp;index=22&amp;t=0s']
lr = ['https://www.youtube.com/watch?v=Bwyu-SZ7g_E&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=NeGDS3zIsxU&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=Wa2PeMZnBZ4&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=uVL4d8P44eM&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=G4qTNRbAp-c&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=Q1ViJEYNki4&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=TgAomHGqKUM&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=2tmPSK-w90o&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=9&amp;t=0s', 'https://www.youtube.com/watch?v=Qxlnb1lEdEs&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=10&amp;t=0s', 'https://www.youtube.com/watch?v=CZ_-O31R3p4&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=11&amp;t=0s', 'https://www.youtube.com/watch?v=YuCwP-NbY0s&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=12&amp;t=0s', 'https://www.youtube.com/watch?v=vRBOIbTyTnU&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=13&amp;t=0s', 'https://www.youtube.com/watch?v=4q7OpvvfjWs&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=14&amp;t=0s', 'https://www.youtube.com/watch?v=_fr4SV4fGAw&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=15&amp;t=0s', 'https://www.youtube.com/watch?v=HyXEzp85RGE&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=16&amp;t=0s', 'https://www.youtube.com/watch?v=B3NmMKfl3Ic&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=17&amp;t=0s', 'https://www.youtube.com/watch?v=FZjlP-N7Hl4&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=18&amp;t=0s', 'https://www.youtube.com/watch?v=Y4r6lS04RpQ&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=19&amp;t=0s', 'https://www.youtube.com/watch?v=TwPCaWQIJME&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=20&amp;t=0s', 'https://www.youtube.com/watch?v=glTZy-Sujuw&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=21&amp;t=0s', 'https://www.youtube.com/watch?v=YRwTaWWK3dI&amp;list=PLRNstPwi0r8dhdTBkA7iNXRaG_yynueP7&amp;index=22&amp;t=0s']
grad = ['https://www.youtube.com/watch?v=JRnp5nwnkgI&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=L1SEEMkc-qw&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=z15wKo0r-74&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=jG1joHmrRoQ&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=6&amp;t=0s', 'https://youtu.be/ZRKkY2x7aWM', 'https://www.youtube.com/watch?v=6QARCF_dvWo&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=4UvPbIbLFAc&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=9&amp;t=0s', 'https://www.youtube.com/watch?v=hLRUVURf4NU&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=10&amp;t=0s', 'https://www.youtube.com/watch?v=1ey-fHASEuQ&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=11&amp;t=0s', 'https://www.youtube.com/watch?v=gfj5FYaCxIA&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=12&amp;t=0s', 'https://www.youtube.com/watch?v=qh8khoDhcUQ&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=13&amp;t=0s', 'https://www.youtube.com/watch?v=_EgP-GUDd1g&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=14&amp;t=0s', 'https://www.youtube.com/watch?v=35c8IW0vsSE&amp;list=PLXR4OlatIg5Fpc8HaoBlznnCGXMVJC9Ql&amp;index=16&amp;t=0s']
eight = ['https://www.youtube.com/watch?v=d9BMPmfxaoM&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=tX3IvpH6loc&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=s40BTpfAELs&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=KaumK4b6DqQ&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=ek_T6atbfe0&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=CiY8-LYkCEk&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=kVl__NgDAdw&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=TUfuDKKGQxU&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=9&amp;t=0s', 'https://www.youtube.com/watch?v=1BlH1JZBeXI&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=10&amp;t=0s', 'https://www.youtube.com/watch?v=T5e-nhk4HTQ&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=11&amp;t=0s', 'https://www.youtube.com/watch?v=tpT7H7qIHIo&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=12&amp;t=0s', 'https://www.youtube.com/watch?v=OeCdG0Mzrkw&amp;list=PLX68ZEYlh74tpCb5sOXP98ito6DhP60-t&amp;index=13&amp;t=0s']
mbdtf = ['https://www.youtube.com/watch?v=UTH1VNHLjng&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=miJAfs7jhak&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=k8JflBNovLE&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=WHxRd_va950&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=DTq4XEliPag&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=pS6HRKZQLFA&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=0o9HzQ3zAcE&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=sk3rpYkiHe8&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=9&amp;t=0s', 'https://www.youtube.com/watch?v=VhEoCOWUtcU&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=10&amp;t=0s', 'https://www.youtube.com/watch?v=tJKNcI6jC6A&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=11&amp;t=0s', 'https://www.youtube.com/watch?v=6mp72xUirfs&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=12&amp;t=0s', 'https://www.youtube.com/watch?v=1nawiZsuFI8&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=13&amp;t=0s', 'https://www.youtube.com/watch?v=UB6sXiZ1ldw&amp;list=PLzMq4yH_FvVa5kPgtKmgdzPssfmBUtO2C&amp;index=14&amp;t=0s']
wth = ['https://www.youtube.com/watch?v=FJt7gNi3Nr4&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=bt5UvqIotlo&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=gG_dA32oH44&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=BoEKWtgJQAU&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=fSULYFCSaYI&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=77XUrtPFZ-M&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=rDqhuGsjDeI&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=3BYjmyFN_R4&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=9&amp;t=0s', 'https://www.youtube.com/watch?v=qXauaxH5Ltg&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=10&amp;t=0s', 'https://www.youtube.com/watch?v=QAwR-vbrjjw&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=11&amp;t=0s', 'https://www.youtube.com/watch?v=A4yDI7XauPM&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=12&amp;t=0s', 'https://www.youtube.com/watch?v=UtoHI0JEfDg&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=13&amp;t=0s', 'https://www.youtube.com/watch?v=w34GoljYriw&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=14', 'https://www.youtube.com/watch?v=QO97cGFJx-Q&amp;list=PLTI4-CRTcbtZup8J0WdvJm-JMgMJhnnOb&amp;index=15']
yeezus = ['https://www.youtube.com/watch?v=uU9Fe-WXew4&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=QF7_tsKaRx8&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=KuQoQgL63Xo&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=IyOL-f_UO5k&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=bvBfiRWLj_0&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=_jZuz3NEr18&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=KEA0btSNkpw&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=5hthMeEqf40&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=9&amp;t=0s', 'https://www.youtube.com/watch?v=vUFiVwa6U_c&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=10&amp;t=0s', 'https://www.youtube.com/watch?v=cSFdvdFRNzc&amp;list=PLY6gDeHQ2ViWvHWTgnFcLn-1lNSAMpp3t&amp;index=11&amp;t=0s']
tlop = ['https://www.youtube.com/watch?v=6oHdAA3AqnE&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=wuO4_P_8p-Q&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=xp8z7pconzw&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=Lq2TmRzg19k&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=Q-fluWQ6zW8&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=wj0C2oet2r0&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=AXz78NYL4r4&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=ML8Yq1Rd6I0&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=11&amp;t=0s', 'https://www.youtube.com/watch?v=SHfB5HBFeTc&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=12&amp;t=0s', 'https://www.youtube.com/watch?v=fWD9GF-Ogf4&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=13&amp;t=0s', 'https://www.youtube.com/watch?v=lDLEsnXauwU&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=14&amp;t=0s', 'https://www.youtube.com/watch?v=6oaaKNXuUv4&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=15&amp;t=0s', 'https://www.youtube.com/watch?v=SeeP7YhFy0Q&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=16&amp;t=0s', 'https://www.youtube.com/watch?v=OH3bNgA1rkE&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=17&amp;t=0s', 'https://www.youtube.com/watch?v=NnMuFqsmYSE&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=18&amp;t=0s', 'https://www.youtube.com/watch?v=yiwDWKg9AMA&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=19&amp;t=0s', 'https://www.youtube.com/watch?v=qOZ0hPp3OZU&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=20&amp;t=0s', 'https://www.youtube.com/watch?v=w9rzz4pDFwA&amp;list=PLzMq4yH_FvVac_1R0DMcMkcwnJ1-hFx6b&amp;index=21&amp;t=0s']
ye = ['https://www.youtube.com/watch?v=2SeVgStQ5T0&amp;list=PLAUxsgLNM2Bt8apMzywvdzOJSzlfW4OQa&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=kPPyUO6m3-4&amp;list=PLAUxsgLNM2Bt8apMzywvdzOJSzlfW4OQa&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=YdA7swZoxks&amp;list=PLAUxsgLNM2Bt8apMzywvdzOJSzlfW4OQa&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=nMkXJohQiuQ&amp;list=PLAUxsgLNM2Bt8apMzywvdzOJSzlfW4OQa&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=4I8gDpuvZt4&amp;list=PLAUxsgLNM2Bt8apMzywvdzOJSzlfW4OQa&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=qAsHVwl-MU4&amp;list=PLAUxsgLNM2Bt8apMzywvdzOJSzlfW4OQa&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=pOLMGTtphCc&amp;list=PLAUxsgLNM2Bt8apMzywvdzOJSzlfW4OQa&amp;index=8&amp;t=0s']
ksg = ['https://www.youtube.com/watch?v=rnZQvgWhM5s&amp;list=PLzMq4yH_FvVaq5TFtfCDs6FxWef45gyHW&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=ZBIzL1OdKMI&amp;list=PLzMq4yH_FvVaq5TFtfCDs6FxWef45gyHW&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=6Hj5tucYv1Q&amp;list=PLzMq4yH_FvVaq5TFtfCDs6FxWef45gyHW&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=5bZqAfJBsSk&amp;list=PLzMq4yH_FvVaq5TFtfCDs6FxWef45gyHW&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=hQC8COGQ4BM&amp;list=PLzMq4yH_FvVaq5TFtfCDs6FxWef45gyHW&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=cHFzyFMT0pw&amp;list=PLzMq4yH_FvVaq5TFtfCDs6FxWef45gyHW&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=RaTAlvbC_T4&amp;list=PLzMq4yH_FvVaq5TFtfCDs6FxWef45gyHW&amp;index=8&amp;t=0s']
jik = ['https://www.youtube.com/watch?v=T58tRXzjC7c&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=6CNPg2IQoC0&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=ivCY3Ec4iaU&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=MKM90u7pf3U&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=AOBQkHy8_p8&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=Mrfu0FBB110&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=-YfG1Xbo4OA&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=G8u3P7Xqlvo&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=9&amp;t=0s', 'https://www.youtube.com/watch?v=dojATOk1GHA&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=10&amp;t=0s', 'https://www.youtube.com/watch?v=8yQVcGkbpAc&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=11&amp;t=0s', 'https://www.youtube.com/watch?v=rns_n82HiMo&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=12&amp;t=0s', 'https://www.youtube.com/watch?v=-dTEV7lxFc4&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=13&amp;t=0s', 'https://www.youtube.com/watch?v=DD5GG4iGJfo&amp;list=PL5Z-QTr_hR1gTIk7T-bPCmRaaXNmiP3aK&amp;index=14&amp;t=0s']
ss = ['https://www.youtube.com/watch?v=2Czs7fl1r7c&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=2&amp;t=0s', 'https://www.youtube.com/watch?v=kTB-iHnDpfc&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=3&amp;t=0s', 'https://www.youtube.com/watch?v=-T9qvRsgrP4&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=4&amp;t=0s', 'https://www.youtube.com/watch?v=GM0KKjXB1Bc&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=5&amp;t=0s', 'https://www.youtube.com/watch?v=ibN7Lh19Vls&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=6&amp;t=0s', 'https://www.youtube.com/watch?v=OhBcFDu78dU&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=7&amp;t=0s', 'https://www.youtube.com/watch?v=uno5zkKbgvQ&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=8&amp;t=0s', 'https://www.youtube.com/watch?v=97tvJs5fQwM&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=9&amp;t=0s', 'https://www.youtube.com/watch?v=jMb4WuxQ5jE&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=10&amp;t=0s', 'https://www.youtube.com/watch?v=kWM0FQC76k0&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=11&amp;t=0s', 'https://www.youtube.com/watch?v=nTgzYv7LLmc&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=12&amp;t=0s', 'https://www.youtube.com/watch?v=Aui5Yb3-wD4&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=13&amp;t=0s', 'https://www.youtube.com/watch?v=jpSkWEDkItY&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=14&amp;t=0s', 'https://www.youtube.com/watch?v=8FmX2KKmKLQ&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=15&amp;t=0s', 'https://www.youtube.com/watch?v=iH7odOXB1GA&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=16&amp;t=0s', 'https://www.youtube.com/watch?v=202U6qyVIqY&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=17&amp;t=0s', 'https://www.youtube.com/watch?v=qcuS6A3_Gkc&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=18&amp;t=0s', 'https://www.youtube.com/watch?v=bPY4KbUmVdk&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=19&amp;t=0s', 'https://www.youtube.com/watch?v=urQAfD7EtMY&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=20&amp;t=0s', 'https://www.youtube.com/watch?v=3sejSHbSDGo&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=21&amp;t=0s', 'https://www.youtube.com/watch?v=qkfS3jF9rUg&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=22&amp;t=0s', 'https://www.youtube.com/watch?v=RPiwNOPCy0k&amp;list=PLcllBDpP7V-_NOCf4wbYTbh4VUsObhNyo&amp;index=23&amp;t=0s']


play_help_embed = discord.Embed(title="Play Help", description=".")
play_help_embed.add_field(name="song", value="!ye play Saint Pablo", inline=False)
play_help_embed.add_field(name="album", value="!ye play Graduation", inline=False)
play_help_embed.add_field(name="url", value="!ye play https://www.youtube.com/watch?v=x-FkJ5FzWgs", inline=False)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, ctx=None):
        # Play list of song's given album name
        if type(url) is list:
            index = 0
            for link in url:
                # download first link
                loop = loop or asyncio.get_event_loop()
                try:
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=not stream))
                except DownloadError:
                    return

                filename = data['url'] if stream else ytdl.prepare_filename(data)
                player = cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
                # Play first song so people don't have to wait to download the whole playlist if its large
                if not index:
                    voice_client = get(Music().client.voice_clients, guild=ctx.message.guild)
                    voice_client.play(player,after=lambda e: Music().client.loop.create_task(Music().play_next_song(ctx)))
                    Music().server_music[ctx.message.guild.id] = {'voice': voice_client, 'players': [player]}
                    await ctx.send(embed=Music().now_playing_embed(player.title))
                else:
                    await Music().add_to_queue_player(player=player, ctx=ctx, show_message=False)
                index += 1
            await ctx.send(embed=Music().now_queued_embed(f"{index + 1} songs"))
            print(f"Now adding to queue {index + 1} songs")
            for file in os.listdir("./"):
                if file.endswith(".webm") or file.endswith(".m4a"):
                    Music().server_file_names.append(file)
            return None
        else:
            # Play song name or song link
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
            data = data['entries'][0]
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music:
    server_music = {None: {'voice': None, 'players': []}}
    server_file_names = []
    client = None

    @classmethod
    def initialize_client(cls, given_client):
        cls.client = given_client

    @classmethod
    async def add_to_queue(cls, ctx, url):
        player = await YTDLSource.from_url(url, loop=cls.client.loop)
        cls.server_music[ctx.message.guild.id]['players'].append(player)
        await ctx.send(embed=cls.now_queued_embed(player.title))
        print(f"Adding to queue: {player.title}")

    @classmethod
    async def add_to_queue_player(cls, ctx, player, show_message):
        cls.server_music[ctx.message.guild.id]['players'].append(player)
        if show_message:
            await ctx.send(embed=cls.now_queued_embed(player.title))
            print(f"Adding to queue: {player.title}")

    @classmethod
    async def skip(cls, ctx, skip_all=False):
        try:
            players = cls.server_music[ctx.message.guild.id]['players']
            voice_client = cls.server_music[ctx.message.guild.id]['voice']
        except KeyError:
            return

        if skip_all:
            players.clear()
        else:
            try:
                players.pop(0)
            except IndexError:
                pass
        print("Hio")
        # if connected
        if voice_client or voice_client.is_connected():
            # check for queue
            if players:
                embed = discord.Embed(title="Skipped")
                embed.set_thumbnail(url=get_random_gif())
                # get next player and remove it
                try:
                    player = players[0]
                except KeyError:
                    pass
                else:
                    voice_client.stop()
                    voice_client.play(player, after=lambda e: cls.client.loop.create_task(cls.play_next_song(ctx)))
                    await ctx.send(embed=cls.now_playing_embed(players[0].title))

                # remove song from folder
                song_is_there = os.path.isfile(cls.server_file_names[0])
                if song_is_there:
                    try:
                        name = cls.server_file_names.pop(0)
                        os.remove(name)
                    except PermissionError:
                        pass

                for file in os.listdir("./"):
                    if file.endswith(".webm") or file.endswith(".m4a"):
                        cls.server_file_names.append(file)
            else:
                voice_client.stop()
                skip_embed = discord.Embed(title=f"Skipped! 0 songs left in queue")
                skip_embed.set_thumbnail(url=get_random_gif())
                await ctx.send(embed=skip_embed)
                # still remove file
                try:
                    song_is_there = os.path.isfile(cls.server_file_names[0])
                except IndexError:
                    return
                if song_is_there:
                    try:
                        name = cls.server_file_names.pop(0)
                        os.remove(name)
                    except PermissionError:
                        pass
        else:
            await ctx.send("Im not playing any music!")

    @classmethod
    async def play_next_song(cls, ctx):
        try:
            players = cls.server_music[ctx.message.guild.id]['players']
            voice_client = cls.server_music[ctx.message.guild.id]['voice']
        except KeyError:
            return

        try:
            players.pop(0)
        except IndexError:
            pass

        # check if queue is populated
        if players:
            player = players[0]
            try:
                voice_client.play(player, after=lambda e: cls.client.loop.create_task(cls.play_next_song(ctx)))
            except discord.ClientException:  # Caused because this is called after the song is skipped but the skipped func already plays
                pass
            await ctx.send(embed=cls.now_playing_embed(players[0].title))

            # remove song from folder
            song_is_there = os.path.isfile(cls.server_file_names[0])
            if song_is_there:
                try:
                    name = cls.server_file_names.pop(0)
                    os.remove(name)
                except PermissionError:
                    pass

            for file in os.listdir("./"):
                if file.endswith(".webm") or file.endswith(".m4a"):
                    cls.server_file_names.append(file)
        else:
            # still remove file
            try:
                song_is_there = os.path.isfile(cls.server_file_names[0])
            except IndexError:
                pass
            else:
                if song_is_there:
                    try:
                        name = cls.server_file_names.pop(0)
                        os.remove(name)
                    except PermissionError:
                        pass

    @staticmethod
    def now_playing_embed(title):
        now_playing_embed = discord.Embed(title=f"Now playing: {title}")
        now_playing_embed.set_thumbnail(url=get_random_gif())
        return now_playing_embed

    @staticmethod
    def now_queued_embed(title):
        now_queued_embed = discord.Embed(title=f"Added to queue: {title}")
        now_queued_embed.set_thumbnail(url=get_random_gif())
        return now_queued_embed

    @staticmethod
    def get_source(input):
        if input.find("https") != -1:
                return input
        elif input.lower() in list_of_albums:
            index = list_of_albums.index(input)
            if index < 3:  # college dropout
                return cd
            elif index < 6:  # lr
                return lr
            elif index < 8:  # grad
                return grad
            elif index < 15:  # 808
                return eight
            elif index < 17:  # mbdtf
                return mbdtf
            elif index < 19:  # wth
                return wth
            elif index < 20:  # yeezus
                return yeezus
            elif index < 23:  # tlop
                return tlop
            elif index < 24:  # ye
                return ye
            elif index < 26:  # ksg
                return ksg
            elif index < 28:  # jik
                return jik
            elif index < 30:  # ss
                return ss
            else:
                return input
        else:
            temp_input = input.lower()
            if temp_input.find("ye") or temp_input.find("kanye") or temp_input.find("west") or temp_input.find("kanye west") or temp_input.find("west kanye") or temp_input.find("kanyewest") or temp_input.find("westkanye"):
                return input
            else:
                input += " kanye west"
                return input

