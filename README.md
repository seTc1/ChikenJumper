# **Chiken Jumper**

`Chicken Jumper` - это увлекательная аркадная игра, в которой ваша задача - провести курочку до семян. Каждая клетка на игровом поле имеет своё значение, которое влияет на здоровье курочки. Будьте внимательны и продумывайте маршруты для курочки, чтобы успешно пройти игру.

![ChikenSprite](https://i.imgur.com/sGNx1EZ.png)
# Управление

`W A S D` - Передвижение курицы.
`R` - Рестарт уровня.

Каждый ход отнимает у курицы `еденцицу здоровья` независимо от клетки на которую она наступила! 
Курица должна дойти до конца уровня живая.

# Техническое задание

Проект представляет собой аркадную игру, в которой задача игрока это дойти от точки `A` до точки `B` и не потерять все жизни персонажа.

### Задачи для проекта

-  Чтение и отрисовка уровней из файлов уровней
-  Отрисовка игрока и здоровья
-  Главное меню
-  Меню победы
-  Добавление анимации и звуков для действий в игре

Постройка уровней происходит в файлах `Level.data` которые строятся по принципу наименований спрайтов в папке `Textures`. У клетки с текстурой дороги может находится значение которое будет иметь клетка в игре. Так же в файле отмечается начальная точка появления игрока и конечная точка.

![InGameScene](https://i.imgur.com/dZXZpuG.png)



