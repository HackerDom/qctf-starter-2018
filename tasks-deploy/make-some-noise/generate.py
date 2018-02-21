TITLE = 'Сенсация! Пойманы сигналы из космоса!'

STATEMENT = '''
Появилась информация, что один разработчик-эксперементатор сумел получить [сигнал из космоса](https://make-some-noise.contest.qctf.ru/{}).
Возможно, инопланетяне хотят нам что-то сказать... только сообщения не разобрать.
Они очень сильно зашумлены. 
Наш информатор рассказал, что смог получить что-то вразумительное после долгих попыток и вычислений,
но делиться информацией с редакцией не собирается.
'''

def generate(context):
    participant = context['participant']
    id = ids[participant.id % len(ids)]
    return TaskStatement(TITLE, STATEMENT_TEMPLATE.format(id))

ids = ['i2yctSSMGde1TjBIor4T', 'DZrIgOypvPqMctJS06O9', 'lH4uWfzCg1kFeULgUIVC', 'N9mUMmG8maidbCD0s4mV', 'PuqvlpXgaa5s42mZKE4j', 'CoRVyJtEoNE87xUoRqw0', '8uKC7RXAOBlOXdP7KVGl', '2cVvsSZY3QLRmoAYRFkL', '22enKTGqQwxga5RFQdus', 'Sw1vkSnYDQdEtOjTnfH0', 'S7mUlJwhAJhCFgxCOoAW', 'JkTjzY6JUEgo9G7tHciV', 'xn8irINr3sDQLIAb2CkI', 'WPnNc5oYE4s3IPkL0fGg', 'dVqlZVLNgCCm1Sy4qfOW', 'l5cEE0hLMVCt2TjTit5c', '7BcmXXs7kbip5gfT853u', 'QZrfCklvGpdwt4vB6oh8', 'hAiHcE7oRy0zXqpoNeWh', 'LbSDhksl1vNujaAmhVhJ', 'oZZ1TyF3Ysg9KxtBGVs8', 'FKerevwgUjdoWUGyZ652', 'jvutz2HwlzcUGbSoZkgu', 'oV28KmKrYyvSdosdRck1', 'tuacfxYJA1CE54Ixao5F', 'q2B8TWtgwVD2rsGEeehx', '5bO4XLG9OyswG01jVleq', 'rZBIgEB002nWqVjMIBzg', '5ojT7jrimtbZP6mp7MAh', 'Z31bdvkrb3NtMIC3MenW', 'bbH9tpTiZz7V8a7i848m', '9xWkjKVCX91TzD933bMD', '3Jq5yRa0S0DKpIi96kjH', '2h3bhgxJ3ohZeNuG5Noq', 'o2YpZKg7619CB6yzN5SB', '1JZsemZRho77QrN0skkl', 'K9ySRqaGklft8OAY4l0G', 'r4wgNCzZbxtMhx8SHZlv', 'zLUWPrq0JEvsXn0yb2c5', 'fa87JWxShRCUK1xAV611', 'Kcr65dOqJVpTDU2cuUP1', 'aidLGpK1oiHQ2lv7gC12', 'Ttxgw2BqBD1jrm5l7hYc', 'YbQgYJDKArj2kOh95j86', 'tF82UdE6QhLaNfxbJ5PB', '3lN47CbPRR22TsFVdP6i', '2msPQ0ruOJ5rvOzvi0Gz', 'MUdVTNaq9i2k85AqIlVl', 'AiPFQJJBnJGTKtU6Ifrc', 'a7patLnLlBvWKjzfoPUy', 'sAsApUGUvINTq68IVRXX', 'Ne2J72wYP6LAnrckWZIh', '0D774XxxX56yC2WM7qkr', 'oggJm9bOxLAEEb1FswRZ', 'DXonEXUOBi61oAAj24MG', 'udpI7111q5lofsEmVkZN', 'lSoDYeb6RnTtOUZCG0y5', 'foE9zcv1E3n4VlnbnMGO', 'H69Fr2lKjto9PoNhbGdO', 'rKPI7ONeLkxt6p0bkCnC', '0gXXuhUYpAfF5TWuouUu', 'R4AMaHKEDnMx2fxdFR4v', 'p8HtmlwqQFbRvmlWj09t', 'Gv8gN89ZvU32kvteW3Kw', 'xOtLyoBFxgTskjoHCA74', 'zWesr92l1uJKm9RGGFwt', 'iCkYhQIGrM46gZyOeivp', 'R6BRGvq6uPZ7cRHdx5iq', 'UiIfbhnbY0J7SmnPOiHI', 'tgzeloib826aSzWzJRqr', '2XNmQ1h3uOXxvBY5cf45', 'TronVfZ9KWuimzkX7o56', 'iN2I21k3xQ1x4slI1q81', 'Tg0LMsdZFyyuv5spDpcM', '5Tg0M84vOTpM5jee3xCj', 'xS5dAwdL8ZLCUBCRZnEf', 'r9lyMRAjrWp3BxpT9NB5', 'hhsJYamIQskGD4BkLPUK', 'Du0ryLhVJFhfoDDOquON', 'yJkQ3y6kv93edSSoPcXl', 'ax6V8yGruNZMWmQJW8s8', 'U7GWGaCUjYSJQROeJNPl', '0Kr0BkEkkbj0fHi0HVt9', 'TvX8REHZmZGFWchiFFff', 'unBi2qvY43oHIf67DpJk', 'f70Yf2D6U2cokFrE4M89', 'UHR1IIsj0RqR0tCMWjaY', 'k7noV2tQkX0mXSwbRTeA', 'G2RCr57Ur0r8Bd0msCnh', 'uEs94rT8dvyMSK3tgUmb', 'Cn86UI8t4tEU5LslZLhT', 'GasDs9W7O7zE5UOLlUyU', '8yBxaH7rrliGXrE9iN6l', '2ib88yqt6IMAhZLbP5eR', 'OqZnGIsjGmw2MGsS4Y7F', 'JRj9gpEn7JmdErJthkDN', 'OHoTjcphFL1tWxfdmwfb', 'CmLSRN8HL8CpH7Je56lw', 'BQPKERa1jaW7lv99ETYL', 'tshNpN967rtSld8NYCgt', 'MWVDlAwG0z6KSFKDVdxy', 'Aj6Wbseon4e6CM2a8N1s', 'ZtDlWQnQaURZqkWVxPSc', 'KdtXIlqS604uHDKoqenD', 'QO0sLYHHSnzPUKHjZgiy', 'C1Tn5OZCJfSewPe9qxnP', 'plyCyxg03GwFY0kc9Mh7', 'BV5FLHzyksnrHn4qgb7Z', 'uz2OONdBpGpWREOFn2Dp', 'nRafhWiq9ady7YMjMfmD', 'jbKC4rnCJqnSWNybL0ho', 'v15v2YSAdmmwFsbJzv17', 'wrA9JCI3vQ17wKRznfmT', 'Wrppq31UosvJyjTECnOB', 'MxloukUZxGkyVaDtGyG1', 'CoeFnlaucvloF9dGCV1K', 'q0z4Vqf8uVOJjXMooAd0', 'tEu9sRK1yGBC8kH7sDUb', 'lgMRRPCNwMKSjb82hJN0', 'UhYGSPsJx6dNUCzuVaEw', '0lzOfTipjEFqzJsLiyYI', 'hbTF34f4iv7a981bHuV7', 'DYvTEJqsIk8pPuQS5Hai', 'mG9i1Q9oOtimP7Xpge4R', 'fI4oQBFO67nD6GeFxPjb', 'TkZRLa98jQEvEk5xiBi2', 'gJdNhYVuNHsXemBEU0XX', 'TxyeoCCGL80nX6hv7OcE', '5SayX4207FIvIIjqBANn', 'Kt1CH39vMZQO8mVVbPVG', 'sZInNDG5pKcfzsL1GeJk', 'lSoiTyLc5Pm2g8bS25fO', '8RygrlGoU9tVd20nB6pU', 'QjpdFah2GgN73iMOcKgu', '5uqRz6u3P0kcLddR0X1Q', 'JlYTWI9NtbINkqA9Gcx8', 'O48qYJt8hOoOeIRFZiZ5', 'HKhGZkv4v4SCwVNgowvF', 'fV4BZGFvUS2PUNCHQJoQ', 'kqSSIrlgFzfrYzW7LeC6', 'Yf2waPjPfokxDnTkbKR0', '41fFikB0JwoZ2d3bbT2N', 'XzITKmVvLkUGANuolqjs', 'WeL0qrrg3VUSvce4eOqH', 'bnC1DabRzDnbLOHlVs95', 'iNVSQXEm7uamgR2uM8ub', 'Us0NNywPFasbh18rhKJL', '0UJ9ZTXiVSsXjpJCXYw5', 'MAZtrsxoVBMmh1KxOXIC', 'XMHVLcPDSFEL4PBgO5Uw', '57aBZrcavR7OsV8mFfdL', 'SDYrvSy5HNxZvCHpdPBa', 'qZjSvBWwtiV16tprHaJZ', 'cwYVhgQzRGa1UZa6wVXJ', 'ZurZjCN8DEZ87clrXlr0', 'sLTnm7u7ZtN9JfT29Vxg', 'sYdSmELU7dTZzi9tPmkG', 's0JdJwu3TsxmUDccEpKQ', 'jZrz2x2pItkIAFD2oyWF', 'ooOzVV9Dd1POoGwBiWsd', 'MuFsWSaRIWDWxUtMtHdH', 'mYEILDLnIaMBAg4LJZYA', 'w402UedR0qSN03uxFKro', 'Xh4tAImtQ11tnq25JIwt', 'Q6YOeR6OYFXpRc2vaqp4', '6EaLzsqaq7s0qRavwFOR', 'KipsQDR4RI6fgYkiYQeu', '5TByalXqgofiGuUFQ8ga', '6WSjCzum30MOuHJHI25r', '8o9mxMvUtlKMAIFxuQkY', 'x2N5Jp1uJPsIeLAknqrk', 'fn1DYGLRxayGv91i3ico', '1vpNXERfEuuvKG1yt6Es', 'YDgM6cyCeZ3WMbKtnZRA', 'VXcpNpWmcOD4ZuH0vvqE', '67bfDWVAqymhAV8xoow2', 'shuxt8SQoWuiSjmNCrq6', 'SUAwETaPiK5yZWwWgzLe', 'v8c6KsbsY0O7r20NcTc9', 'Z3I5tZoUE9Sl80IPDio7', 'erz0CZLp38LLQtw5CEyE', 'qiV6CQW3Np8fLUi4aUx1', 'UMxKLOtyDTZsD89IVXn5', '6Ue63hlYvUd2vHbNQTSZ', 'zLwT4gUVggNYF1Qz3eJK', 'EcfEf5UUER30630SJtcM', 'd1GbTz3UiUdCZAtOiSfH', '8I6JNrQL7zXkoMLQ14AI', '9oylE0h4WnWRlJJJ81RO', 'nSMZmbS7vIdnKGym2NOB', 'CJCVx5gq2zEVFZSsHlUi', '1okbUDCHJuIZJ4c4r0cN', 'rc8HONSCGpF0WTct384T', 'EcrLmnCC47uM5uNzapU7', 'BKcxCqu6kH2eB5tvqbp8', 'zxcpVWFMGRo96KdhAWC4', 'pNAbg6kLWHvgWU18GSDR', 'rXsOIcfQbrObgjhKFD1y', 'gng3koJU2ngLBOMBkn09', '6eDv9WvCunSJ3rbR7P41', 'M0VwcTfIh2JHoD1gJ7Sf', 'ipqGoS5NnzBtipdnMo2i', 'sNgfjVax89DjDRU9rTxu', 'zkT5KsvVa7nj6PTYIOyX', 'AKpIUXYisz485o6mIAfQ', 'oFu7jwOR0eVf9DcJEXvX', 'r8yGte0Wg6vG2yxorP4F', '6SylSfy6NZMHIZ0fbesN', 'uI3Ofy6nbU4EnbjTy3F5', 'ZeCN3fqJE6fK86VxMNVX', 'RzesJyPPq5JGYTE9NcaQ', 'ztPy2JblyepRkv2SsIXv', 'O1Hz6rH6n4Z9Ncw3Z8KU', 'cuzKqIY0i2084rczCSOV', 'ieTx304ONQHYemj2yrJp', 'fYETybKFKGphY67kzXDF', 'aPLipH9R0CJz9TY7JGxd', 'KoEEUsf3tffJEUmCsaLE', 'F8J0OW9l20a6bZHXxrWX', 'InmTgiBP9cS3OxlhfVRZ', 'xkOePWlpVrqnRwIoLWv0', 'IyM6fAauHrW6oK579VRV', 'ElQCoR9AqczPD9Za5khQ', 'WkwydJs2ttNaudkIMIU7', 'SNahdBkBCPmLBpNCv3IZ', 'PzC4s6kihAKX4A5LuQUZ', 'zA632Y2AW135ftLE6N7W', 'KyICZezkD0rf9buyIvkG', 'EOoyZfBib1z0slZ288A0', '1UoUNEDPCnyscg7IkYG0', 'gF0wmIyMF2cRTXzhcc3v', 'UVPT75g5WuZGkNWN9baV', '51emoXAOpVghGTtQFOWQ', 'jd4ZuekcVj6FXBIDjPhC', 'Vw6CtkYVgwt7tZkx6xlF', 'Z6HSWb9csLOi9lYXkZdr', 'K5w8aUmv8ziuvxVAEtaz', 'gJlUZ2NJdpJaF5vVKxSi', '7ROI6SRb4R6m2ixtOTsi', '8ulVa0HkjTleFcrnrLzI', 'DDbwwh2Fh6pkrF9v1Lq2', '2AVyf8vWVZ9rR0aeVraB', 'hSoDcdRkTNkY2jRJ44p6', 'PYM7nODrjrBtlsll48wY', 'nOTBcmallErmPsfEHtQe', 'gjShxrDaj3S7CfIRqCpX', 'UtMdrhVZVxCqsRWpyNBC', 'A6vw6ySlJzxHxqWcjjdr', 'AKedWkhs10Sa5WBLqq1r', 'iPbDdV1wxOor6wJEbfr8', 'E6Jlgc1Dt1J8ZG8m9ery', 'hiVkBdvIrWADMn9K3Bpg', 'jdiBazAstfwwURNXdtXq', 'uCqYuvXYrIkruuATULAI', 'wernRdpvziV6WPIIJQyJ', 'PisdxrXPrQj0IkqHwXBl', 'ZxDKBsw5l9JeSMjPVEqw', 'BuGWtjmJWPmx2zArydrP', '5bahZ86HGmm08J5VhukA', 'NsP2KSOOaauXbWkZ6TBv', '9cqcd51JF3F4rXOd5G55', 'n0nh5CYVV7MvW6IEOR3a', 'lMc2DnDcYTrQCMXOYylE', 'zS2xSCIN5RbTqhVlCXaO', 'Deq9fN9pLE5dxBh5ppSj', 'dWP3pdhq7VKWFZbCCLz5', 'awA9CSiOASuoduTGJnXZ', 'FHcjTniOYY3idvdEdn51', 'MB6D2gabYDyAHmTSYv4e', 'mfHRpODtQwQQuOxBtIN7', 'VrPjN1tcAXQPJptLdHqP', 'S7i03QfGSsCnE9rSf1CO', 'qhQOeX0Ep8w2rAC3MTOo', 'HgKWMudFaUjMm7mHqhWU', 'mXYHQ5qBarilfdgvRtod', 'BmZKX45pVNlaEwcpHPRr', 'vkVPgpXzOIOnvJOQmHO2', 'xiEyxUYl5PBPOlsuuor1', 'AykfIrrrgOzELMDjEXbG', 'nFjwgiev0ifFTWSClLDs', 'Us9DnjUSK3nzNVk2Jmym', 'rCG3nBdhL29jgmbeJ3ip', '73w3b35jkAmcNPt6WUw2', 'E3mYkhU9dISSM5fI6zNn', 'Kr3JPdazNCr2fFS2C4pQ', 'tQK3I8E5FQ2stLqgtpGA', 'FRn0yQOPIySOZYD7RZQo', 'FcOcCdCD1PZZKc6PTCqv', 'Dzkv7buCdvX18dN57uai', 'MOnnF4psJ1vjcxlHQU2h', 'j17wIPbFs5nWxSkjgFsi', 'YJjEGpxOF7lk5EKoWw28', 'ql25h0vlF2yejgMy8xh3', 'SbMmww5QnYtJtp9iY8iz', 'y5cy0cS9VPqHYIvoJB1X', 'm7NSyXHcZUCH3wpj8JTe', 'IC3vrMDSOiSsCNDnUFnv', 'ydDSpVRCJ1fhukuxeCJb', 'PBJFoFcfdk6LQHMjUvxy', 'RJk2XmA2V170SebetXtf', 'EHEbpGGgW9dwvbCBpkAr', 'Ft4F2UywuvJyUJVtwV03', 'wSkVEbzEcJ0N8gTJYJJn', 'NFwirDC6s0ZK5D09MV9d', 'L69rtPAnJBniZQ1wY9Rp', 'sat8N8y9rD871tlRNkIM', 'RkpY8UrN618kIfYErUU0', 'WV3XCsnC1QUxf4DwI7Vi', 'hrskfP4KhZ6uxWWX2Wf6', 'uJzQ75TpLeXRXU2Ufayn', 'ryxiMJmUshE9V6Tl3gVa', 'EBEFnLNuQ5KZL2mlMcsP', 'mckoZKAxQ1IVKM0Z70LP', 'JLDJa1zO62MvHRC9c9Id', 'wnkv3SWvOL0nbVXbDrKK', 'IQay2xUcizSto636XopR', 'A0KIKmr1Svhd6Zf7XEL2', 'Chuwd2uyYTYSauiVSclo', 'BjHw8Ia8Yegbye7bIVAN', 'oiRsaEaW5XtS4pUzXhkq', 'Erytew9yhDCKsnqemMfM', 'ml9tr1UK7GhHg9tDv97s', '2dN7o1desEaVwUa7nP8P', 'ten7xhCJ4Xj8H4gz3dWP', 'lJRMxAcfte1M6hssmlCD', 'xoFkVm0aRhWM8QI1gqiA', 'XDIvH4n5DaNU1eKZRrR0', 'tJBfcb59t4mSrQccthHx', 'RROWkqDeQAZNtXmOvJ49', 'v5qmmECmEQt3AZYt3B9l', 'y4v0IqC80IAtwXnT4hvH', 'wmUVbqNw0DbpxMVV2BOF', 'ziqDC9x39YuUKhFmCd9S', 'Wdlb12RLuG9KmoAYa9cM', '2iAUcnhcGFxigMgZ8juK', 'TV9cMzLBbMemPt0Vu6UX', 'tJmtJsta1korXwVPTvax', 'kO4QSxR1iD11CqLDQkxs', 'M9wQwfk1TGWe1DCSmo2y', 'oGPCXLPKT1lnWoNNtbSM', 'qbfuh7TreONgP9K72Hlx', 'LJOnpXCF5lf7xzD9Zboa', '70LHLYI4dryWBMIZ85iC', '6sKBeFahriATaDBu7Cqj', 'qvG7l8AtRDu2wexD6w82', 'CLj0FECmFQTeVxQ1If8E', 'AYXrtgxnAQiC1WnUZHKr', 'rvBtxsYKTQjYMNivJNam', 'IfkR2CiTo4g1nhUUL9F4', '7Y5nkOZ4H9Pm3PzcFMqP', 'Qd5V0DKY6YfD7jTJdfXU', 'bm3gk5wM9C2lV1Z4oAy0', 'XvEVlTtcNVg7qMG0tC6r', 'WCwxHVMVca8cJmGMcxqK', 'KWQdZohpsRFPURIvMriB', '0Zd8GGPlfFLYQmqHo8ed', 'dDoV8m4VVNz6LHTv8bSl', '3tVF6RMLsLH7rhoVhW1k', 'BID5ZzQwHBdtigGHnNsh', 'ZGDxOy3p3vajM8C1hEwM', 'lGNtpOw3LxjqstCVzaVF', 'tAgC2sKtSUljoF93txgW', 'dsPXoofIT7jYiLf8W9bx', 'RwxjVhOXi1dTtIrkTnCY', 'm6iNYv8DOekwo6iA2O4W', 'YnULmZPnpMjF14xelqZo', 'VHRZP43O2NDp6lcIUCy2', 'D3AMWYHrElbi6OSIlyRG', 'MzlN5uoTjiyrEl8LURG8', '3fDKjj7xpnlQHOkpIa6X', 'SOmxD7RqEXLQDFd2CRtB', 'kcSWhiNtiZMFxuF0pyWZ', 'Ls70yXN8hvRvCa5hgls0', 'jq0MU6QoXhoMZaLvH2VT', 'ZJM4HY0C0IEslRRkN3fm', 'EHNiL6tjyw8GTupeHMJC', 'ahQYyiFcQem0cDvFXrSF', '8rXsIlcqhMnvr6TEMuN7', 'hoFZ18iZ6pwvmK2RZUEZ', 'w0q8TiYMCCUNddfTII8E', 'SOOG2DdubRP5AlkVw979', '4YLKgLH0nRI5gS2gCI0k', '3hKDB8FtqjDbRVh9EkrW', 'yKlVqKLiKxtXftFxeWiN', '16pS2Pzzih5dr7JkAEqI', 'Xu9O8lLG53YhjKJNdo1V', 'Wg1PdXL2YTRSABqtErtX', 'VkC825R2ko68Xn9NwMAa', 'J5NvjtUrvfbEJQogMTH3', 'FFvBbB8yQmwj8iG46hEp', 'g1Qlkh268ezMG8VTSTiC', 'tL0PYhxsf3EgJ2j5BUhA', 'zNFkyw87SbAjf2hyo1MD', '1VU7pLvC1h43EpQfmVTQ', 'qZQabpPqtKkZEJZ7Vt0W', 'MNoEgrIVwf1omOubw1Di', 'eCZwsvj9OkwG782U5pyT', '62VUlndqFsfkp4TpGe9o', 'T1BAIb7iDdwieCKmouLp', 'exopoBpocE8uZb2E0VG3']