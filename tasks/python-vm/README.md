## Что и как
### Файлы для игроков
Файлы, предназначающиеся для игроков -- это [vm.py](./vm.py) и [memory](./memory). Всё остальное **ни в коем случае** не должно попасть в руки игроков.

### Как генерировать
```vm.py``` для всех игроков одинаковый, тк это просто реализация интерпретатора, исполняющего выдуманный машинный код. А вот ```memory``` для каждой команды уникален. В этом файле находятся байты самой программы, которую будет исполнять ```vm.py```, и зашифрованный флаг. Чтобы сгенерировать новый ```memory``` выполните следующее:

```sh
$ python3 gen.py <flag>
```

После этого у вас будет сгенерированный ```memory``` для команды.

### Запуск таска
Возможно, это нужно добавить в описание к таску, но сам таск запускается так:
```sh
$ python3 vm.py
```
Хотя кажется, что это вполне естественно, поэтому я не вписывал это в описание