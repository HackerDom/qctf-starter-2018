TITLE = "Новый шифровальщик"
STATEMENT_TEMPLATE = '''
В сети переполох из-за нового вируса. Он шифрует все изображения на вашем компьютере.
Мы смогли [получить](/static/files/unique_random_secure_task_id/generated/{}.zip) его исходный код и одно из защифрованных изображений. 
К сожалению, мы не можем найти его главную часть - библиотеку с функциями шифрования.
Можете ли вы нам чем-то помочь?
'''

def generate(context):
    participant = context['participant']
    id = ids[participant.id % len(ids)]
    return TaskStatement(TITLE, STATEMENT_TEMPLATE.format(id))

ids = ['CAqvg5Zr6eARLKdlUZ0X', 'TNro4LqtIvWtaFwCnrzn', '2hpyVO7hKnjaEJdfsqfm', 'xYV2DmR7iOo52aeYzitT', 'IsckE62MelRUkZYUEIxP', 'FGCEQreZyAsv5KEQoNpp', 'jBzbhDPvwqcsY05ULja1', 'xEXpcIVBTjxqWXvYY17r', 'LyolNJbl7YfdcJWARbof', 'av2MrzbilZqmTHu6JlPF', 'FZg7HKpapQ3byvBsWz3v', 'fi0VlrbdK6yAE1R1iJAX', 'ATrd1C3UkjKfdO2bdu78', 'AGTb9Tdr2dE3beS4csUO', 'zQ1DznBfXp71uv9VvJuO', 'e6oEIMLF2fgyFdgBFday', 'JTXSF5eqtPkpifHegUlb', 'Y3nywSsGOu1DYtMPftFi', 'cW2EJwC4Ys9Anbvazg1H', '3lRQ9tVwsOl2ZOKljj3f', 'yj4Jo8EY6PXVlX1HgHwC', 'CfWpD8bAHeE9IZJSYQjX', 'lewBP0wvE91nyu39xIZf', 'r4L960UI0NLRmd7u9rXD', 'Cxg0GanJKwHslsiL1Vny', '3v4WOKfBu9Wv0dlylJmA', 'wqDlcYo6Wt7HMQ99bpmo', 'Fgtgnf7XtMqsgD0uOQXp', '5GDjQDMvBtQ9mTcGyOhz', '72NCAqHVA7mQDhScMfe1', 'gRE6X8QHIe5LmJ5xUUwn', '8OrVyKSZkFFyV0n4Giah', '7B6UaaebMjkAEuHz8Csa', '4shngNQs9ogRIts2tAC6', 'uZIEuZOZJYnPuEMeKMGN', 'twxUUwWvMTGm061507C7', '18IEgoExtVYlnUxQ3Zxy', 'tSJb7HUCOQNHl8D3DsQN', 'J65fJry5rvOQsUyKt8NH', 'WugIt5QFK3E6AxeGRp3G', 'lLm2x8RPQt0sBCM41SpJ', 'Q44D9nPepWVP5G6wVuLd', '32xvcmKDWVOha6eTBPDv', '21YHR0KqG8KJIy2b82pn', 'gcHY0JhxYhxlPaV6ACAK', 'ZNwryojU1n880eyeOay8', 'cHQzH3XfuTCTOjQTfKfv', 'wbLbkBLXUb93jipwqot9', '7YBTnqVpJded9fKB2SCp', 'fzwu6PhIZWLIh1QfeFJE', 'kyHfjpjb63j2vkoskV1h', 'OEvOfnold48ALeaGCb4K', '83pDjlyDDw9FP3xRznvM', 'ibXeB2TrbFgZR0K3xvGP', 'sY0jCPge2aWmiOHHuSuy', '1ejsWOOJnbtPlrPehMmw', 'w8a0hgIfLsjVbganjJ2D', 'o6xJG7d7dZljfMgGVQ2Y', 'q6wm9WJEnWTnNBjYlGB9', 'rqldhAlxNvfNvCrFwBKM', 'wLRszowzUWdizrZQn5OD', 'Vddm55lp5VQ3iLHCpDYv', '382LQMgI0akTB55HCijj', 'y8cfmDOYJmSppRw0oSXb', '1y20qubIYWn9Eu8dq0YB', 'zLDQti1q18t0Szo5V5y2', 'b3EyW9ZRsKflh9yA4VUl', 'tNLlsOprjmOQe5cQHZtU', 'EpfTqBcFBzEddAqVqslT', '17SIAJg03GEMLNtr8cSr', 'TquRyGXnoUxscGHjWZQc', 'uBszBfxo4A2wbDQSQSSu', 'VJd1xsBD9gm7XcR4YxsC', 'ZOJldSdslODxGxq0efex', 'A9g5J3j2oe0QLnKgWw1z', 'A8qzXZf1Wesfkpy3NDyK', '6CbAFwnUKjNNCP9vrhgF', 'wJiXyIaQrJSMevytadBC', 'ZmgjLozldON2rHqbuN4C', 'V8U2jXBCsFWgRAv2lCvw', 'XQXoZaPy4lEA5FeYZLcR', 'q7rvrniL7X2MuKIiguAm', 'ZOvgYahZRjRLNckLCSPf', 'MASgveRUnhYgbNar75C8', 'mst1sGKyTSLQphE8yBDw', 'dTGPZBJwdbjRSQnEcxda', 'Hz6lP4kj8L8u7ogozjlE', '9cbFQAo7n5a8Xz7tNwgY', '23Xia4IYy1kLXnshNMJX', '0i26TSAjGHjU2bQMCfSd', 'ZEUGyr7MEIleOVQNDbrG', '5luU7OaHaIvbemJM7pYk', 'dyoztDuEAqLyoG8Nna3V', 'fuIfVgNp6xW4C5TX32GE', 'N3TTDRjaoRQdeskH1ndN', 'OCXQx4VI1QUUWXU2grny', 'WiiiR1P6dmlu2P91Avys', 'lJrOvKmFGwHhGDJioTRG', 'wmS2DazqSiRA33lKyaVR', 'aMtH4e27wAm6MYcBMLKX', 'caEvpzi88y4LIvEMWD3Q', 'HBhqP4LjsgTQhe1JFD0R', 'Aw9Crv3r0vymLTbz7unU', 'CSkq0yJLE4znZpdr0S2m', 'JpwVYZ4ujmIcM3t5tBSc', 'isU53cH0kzZhTa59TcQ2', '9v1pnhhzHHErs83rkIYm', 'RmBsWjjWNvB9WVc9SgJO', 'tyng8Fqtgd1dDHvhNFGV', 'nDp3pSe0NkPJQggV5kIM', 'jphE3377GPppr4o7ly4U', 'RFCcw8M98FpYWT8sf7cV', '26JHUGT1lH61dmsNo0JM', '8AoHtUE40miSDQ4uJfaV', 'SCCbOEAfLVl3WFyTzZDC', 'kcjCOraiur88dwsuyCR5', '8SpUvyuwLVFOrKqaqS8d', 'qjbs76rPeQ5Mp7cUUa2E', 'XKb1wL4hqHGqf7PtwRGE', 'ICDqiYh2Griil6hV8qRx', 'EEMhT6lANNKj870ySuTo', 'MJWp88Q1Mmj3Cml7oLLX', 'OvPOBtZXBw1QVl1IAo6h', 'crMeQIxFWI8wK51XhOul', 'OAaccKIjgSUX80EiXrZc', '9RKqdbi9xB7YW5bh74Fo', 'O77dwOZZoTiN0WvvmEXu', 'meaPhcFnWSvdgXhQGVDa', 'nDPlEmtZfT19YFwOzu8V', 'BCPc7zSUGg01n9jQY9an', 'e2toxWYXuumez5cBd3xt', 'VQxbbeU5jiSYdkUN1itC', 'VP7AvGkfdzTwO61S4yYY', 'BOBzuFXhvNjJzdFHLAP3', 'xuKFPZ652C3Lg8jrYCZt', 'a1YMgo2QE9mTVudP0baE', 'R3018C1OXkUDG31YCvYz', 'SZJQ3gGpIlP5CSZfY9ao', 'uYkdIrS2cg2Yq9sEMWHk', 'vV4QIECLJRfpET5GfSdK', 'OjKxakE8PHsQ1wjIxpzQ', 'yuXy0LPUtDAs9l4a3Z1U', '8cj976dIuMO6rDmZEGzq', 'mjuP6XQtnQrmGMDqCqFZ', 'KA0SWhNTAHRIEAU9GQJn', 'emJTsl4Fs3FyvvRKePxw', '3lpPAjnkly2cOcZCtDgN', 'JRorG8OSCNCjVGwUas97', 'eUFosT3mmRw52XFnqjB8', 'dK7OoNBJOZWjEWEHfBS9', 'VM1ictp0N6Ze0zb5kigg', '768T6rZqaOjb74Cgdr2k', 'vpKQcda6SQMegUGpuYwE', 'ojghTQCp6IfbWFvk3yAJ', '0zmIRGDjTgNiXgT0hmAj', 'J5HD9L8U7SemSOBixpGI', '4HXMEtUpZXqNVR9XNUeW', 'gGmFXXUCRJpY84EQhzVF', 'bFQeQb5S3T6qu54PB9Qd', 'o53KJDYpCAEqH61xLMOK', 'nErDWzh7NleFgxAjSRw9', 'Plyp9mJplaQEFfnuNBSe', '5MNnuR8he2zcDlTzQWmo', 'QJ8tFcAUbOHM9ic5z74q', 'pgn97lZSNHdSDTEjLTba', 'wVC9KXbWk3o0jcLJJrrM', '6XCmOZRUfE4PtHyTERBT', 'IXp1a3SyRMWvKCp0wrcJ', 'MLlMwTp1xIOdsjyWuRh3', 'pS4Mr66o8Pqm57VzGlgH', '7uyPIjmcPEiQdJULRka6', 'YJq2gNF4TjDyCP0KFJV4', 'ZETsYB2E1ecCwjKMr8nd', 'X20crOJjGzwHtxHz8wFO', 'h1FogtzxsEadFgT51wjO', 'KzUhErJhLueAOFtcxiZ3', 'NwsDSqRSCNPX8WukJrdm', 'IoWW8MIkd2gdOWdqry2G', 'rbZd7qFO276jFrnrEv7A', 'ODmSHQP6QHMSbjLu7z2C', 'WllukCTv17py4b8oqhPC', 'BKzGXrszvGW6N9ZMnijF', 'dLLWVmaeA4owdvfE0smU', 'Bgwqa6mk6jerPRjNS1DO', 'yJhm1EcSwcFmEC8V8fDZ', 'TI9w7frQkSAy4Hg3LWgZ', 'nED0XfUAZCTsFzQIjkZl', 'BxiJGmAocd9Pw3qXjMp2', 'jHDel3F4Lt6C0oIGbFiy', 'rvwW29EW2vURrTlDoMA9', 'Ej5wqxUk6L94Kb5kGp78', 'MD4zuoRz4SLtzarw0Otu', 'Ay51UQMin9HGx2z0ubUQ', 'M9EH7VyXHNdrvHGjrmeK', 'klMm8xxisztQM27uEeHE', '8Vb4AmgNwfGfRHWNABoU', 'lrnykoinPIgfSkV7BUcc', 'fN857WdTkjePg9oMMCxE', '4AEoZuvZaPOb7VBFI4Eg', 'UG5vfdZzBiRCG4YjuaOz', 'iQTx7FihK4B8yZpyG8zk', '3Oy7ZZuiBRYZTfnhSC9m', 'NaPudL5uwB0oIPkKV0Pi', 'wlNYpp7iNi6hsBAvV6v4', 'aLH7XvmNM41pB6upV1Xi', 'x3N6Wg3q1nuu2jXpSTFD', 'nIehRyYaKr72mnB9Kvpg', 'NavulshSCmVCU2DPd9lp', 'zinspGXm6b2F9fbzafVI', 'E5a0RQXtwkEDQm853WLV', 'b269ShPjUnol8UGCuRVU', 'rNbHLocGDHIvCyhEgDJX', '7pidsolbQ3o1eOvFpO56', 'MXrOjFhLerA5lKIfUTP0', 'FzHz6HZlufeUrr4EJrMb', 'tiZa0jdW7lbapIEBoBuS', 'NBAnqQZACyverwuEUisO', 'iFK61uw85GR41bXx44rW', '2fx7bEyBVWzNVtvdNP0m', '350vM79mSLeItDshxXKk', 'naFJaVEaAsKdEIBsocdZ', 'Rg6y4N7Wc3ynjfPr0vGk', 'ZOxCdxO9NwpNDSeEAdke', 'JyHVy1U8y2GDJS2XkZ3j', 'XDMCFz4nNPInRyLYnEVg', 'QJ7pGe9ohlPcJTxSfobO', '6M34u4Crnrd4ZvsBbCYo', 'zM9Bblnoh7iFrnR90Nq4', 'CSOkmxC1hIApvreR5nAA', 'XXJ8BUpjjnuVryNw0TLv', 'kyOad2Z3ld9su17VfMnW', 'wjmbcKQwsxxGT7iJuE7R', 'mhq5LE1adJ8JQiy4cZ3L', 'SoP93su4pIae4AjRJyY0', '7wQ7lVlPCkjtuvN0maPP', 'y6nf2YhQ83XitoU7Bjyf', 'D88obyaZaJnJumWcAWud', 'KoR7Qqgu8Sde4RO9hdmu', '6bWTaPzChDKEeugsY0fH', 'lPx2T0ikxDNo1nzsuDE1', 'wb2byx2vGFcyFhRWjkPf', '3eRoGK9FrMuJqQiOREPi', '05iSPcViGpy0D0s0tn6n', 'SCziRSnw454ww1nLAlar', 'BkDGXLB8e7v6YrQYDnvS', 'AjYDzfMkWPcIjqMJrOLb', 'TE71OxFJae0fGbvxbrfJ', 'pXLJ9acXKSzId3t0uTWN', '0dvRtpRqtlSwvMuuGLYJ', 'AjvDGRXxuClkEK4754dH', 'NqqClPz9fb5wUcFS26yR', 'nMS2LuAD9xqrRu00AKc3', 'noyFuo5QdIPWB1A7QGZk', 'MILYHdK4Hlnu3dgJeaZh', 'pSGkvRdEU9mBUQPWiKyO', 'nlurzTPcz9BIgBro3yL7', 'wjRcLINXFVxEaojnHjSV', 'iKTyFgiySgNJLUuwAqgg', 'IThC6SIjcTOY7U01Jcgq', 'qVgwDQmfnpDqGs33aKVh', 'HpaDcb7xb5wFavVgvb5t', 'tgCU813IxgqVDMglcmF1', '0iK3FppDMqRMEOAz3tgE', 'Iv4IQyyURBIOnUKc50zg', 'jFOXeaGJEDZUVI8crEHB', 'd58hGAmMecVyKTHsdnkZ', 'laahXmh0i9yaSlrBZZcn', '4J5Cs29uluQc58vUADgv', 'EoPqqePmexAYTuqpbEdU', 'IKW4PGY9pQnWTQUoFx3y', 'V70SK72EW5KrjDLNym4E', 'plwpJc27H6GSdJUTNnqd', 'Y5Ng9fo2kldSZ6BC1ba0', 'E6iStNjHAGdG8jvy1gvk', 'TLjgzcmu8yUyin6VYJiO', 'O7gKtgKy6ffU8FHdeNGX', '9tItpZB1a2wT0QU7TQz8', 'M8cA7WsJap5TKYpITH6F', 'DbQwSh7xLVdD0Mcjx981', 'kZMVmfEb4ZvMhrfhi60Y', 'nwcEvgbohPJ1IBduXDWI', 'yjm3IzJXTcvVdtjvERok', 'ABriSGyA4qUxO3b7hojc', 'DWoVtFzQFeh6s3fqnibV', 's6pMc5eqh4wdUHh8Hg8V', '6lwK3i9oDlc5kouiZhem', '6KhrlNnqv1qrTGtyHffG', '9pGNEb1ussGtuzG3U4SG', 'acO3gpgiit2SzU8rEJf4', '33anm88MkmMSp6x7yXJA', 'Lc7ejQiE0pCUpYUBCey4', 'KRTYS8JO5rvGTbqKyf6C', 'F9IRkza4CReKRGBluFxj', 'sf0RJgkcYHRe1uP0pKi9', 'IyCAnSvCN5UvoWuh8GAc', 'BVSH2U1yZKjxqCVB1Ped', 'xNgWD017hsk47ofXJMgO', 'zBT9zmUigbRewTmUnajE', 'yNygXNRhBdEZQwpDWJrG', 'aJVeQmNFMbWxRQlh8hYQ', 'TtkQpv9AD3t7wZqyuGyP', 'rZhUQuhPwJJzN80CpW7r', 'xjSXyhWyIqZ0ZYZtlHXO', 'n0gRiBi3fH15r1BZz33P', 'OkmLypD5h50eqItq6bIO', 'QGbwgeKt4yCYx2BO0Cid', 'GczS7vOg8q2Heit1zqi1', 'xbWf3IUcaxPF4Nr0pjNa', '7yMp9MENzavzObNyjh4s', 'IaayEwBt6qn79YTbiN1i', 'hpociPQyohgt1MZwhFzj', 'kd4mFRoznMboY1O97667', '6ilUgKKgmR5gBNlLMDf0', 'mayuKQb17odMmT0fbZdL', 'cxXBaGYQc17OjheKbdCt', '1bX2zynlrKsI41PfMxQi', '0yiFbxdsBvdJCXCBZuvp', 'zaMWamllS27CsjCFDpac', 'chQ66l2h9WjBxkFBr7Wz', '3hzwwio51hhpsYvt0ppc', 'T0OyUGdncJe3uxHfSoZk', 'j5fqBzZbLIDLSeHwatsm', 'kAVu5TgT9v3uAinkliIV', 'OmlCM88gRXnQY0d3ywHL', 'ARdLEfxFT8HxuOL3S632', 'cCVpWX0PtnTrjMKbFae5', 'qLSe6j94hcwTSlWQEbk8', 'JJQbfWfbK1vZyaylhM7z', 'Qj3y7BWZYrlPSrb71ZhH', 'c8SdyKLwTwKzMURC8TOa', 'I7Qiw3RI6E9Ro78JyrfG', 'abzHWJBr1IYdmcXpiaRT', 'OEsNgb5NUU8cH0G0ZSKP', 'I1j4K2FPG2wmqhPM510i', 'eCFrufqR1g2DUX4eNuUH', 'X49Knc5U1u4alFatdZZy', 'v3W2jy7bNtQWxzhD4g5a', '8xIkZOrdX8b4ozYsPE6s', 'l55LncnoIxGEdYMph75R', 'pv1w1fnP6qJFcHbhalYi', 'I7l1Vrwynnhr0HdrdBXH', 'xFkM2ndhi0a8xtLaGL6V', '8awugdEnVyzy4UrwAE0M', '7cu4OhC1boG6M5CXoeP0', 'zU3t3XthijVjNTdc9IeJ', 'S7CTNJiTd0NAjuu5vcrb', 'J1P7gx8h7wx0AdmIsChX', 'YrqrN6NcIonqlwVAVVt4', 'e4U6vSRyrTFc8uoyVtjR', 'jR99FXeqKNHGnrzCgBiY', 'hppsbmuwXcxqCcXg564m', 'xLXbhzIpZ552cijOGW3a', 'zMbzLUzdXie5qjSRlwJ5', 'gDqAxUVtz4JepfKS6xyF', 'KOcR7zF2IkKahFZa6BaR', 'niXm8v2UcYR9OvMnJtSE', 'pULZoEo97IkIydRIpFR1', 'sp0aMEaLur8TOJ70Sy7n', '5yysCZXi7OebfAfPsr7f', 'CKz6YG6bXvclMlSFJ2Eg', 'NEhVazoxeNGmoeM6PZMV', 'EyU8HdpW3hoXxkDrs8ng', 'otTSh5XHz9oHg5TktGgb', 'SNvbFjc1oMRA41a8u3X2', 'dU75aeTqlJJRJOp6YyS0', 'U3K4sKjCkgfSS33WM9CA', 'uWnoX6luNETEeZmj5lNa', '3nRy2oONrKWWxZL55rHE', 'SVpudIdBiHepXM2alUWp', 'bxIjixpeAG4ytZxwXX3X', 'fXkVVgHHO8sqkJ2OMrZP', 'cBoIROAnarO6Y5bf69Ww', '0VPsU6QAVsvTmkapyWZb', 't5xGLwhl2cAPWplYAW9R', 'VxjIDrK2xXCCfidorOfj', 'ZfNn8YAwp90fB9G5RA8O', 'OqsVvp4xAcUDeSR378T4', '8L8NJf1ElslxiMXclKJw', 'vXAcBhjCu3797UTm5dCv', 'JjfgkkRPcxpbtOakh4oG', '9uL4jUdQdT6LTVyVxJOk', 'TT3C7FznoETNWbSXARqZ', 'khfrwSG5TKmxeWWZTKkR', 'kcJ1iKllX5YDsez3Ooi4', 'DWZKSILFX4PIVMn8ArOn', 'kYraGwLIK1QMnJ1T6G2I', 'SNvD2lFQkMZzK5IzDBAb', 'sLyuDLtYGX2o6sMGOTUw', 'dOkh3zFHeb9xlLr8HlgX', 'fxENCLezVlOqDr0PazEU', 'NgKpmadbODXgyOfyLscj', '31bG0HHEknIXZTcLa4t8', '28V74fThbNZ0Xu7K1A8n', 'dZj0KTfCCE1toHZzx1LI', '5nVYh6gybyLt59bifgbk', 'IBM00LToLue90YSPwWKG', 'Oa0cnEIUHUBvLlflwQHi', 'JTV5zI2gCiZfQzSJIets', '5qJOTAhBT8yKt3TFbeet', 'XsDdsEZXIhxdOjIIoYEN']