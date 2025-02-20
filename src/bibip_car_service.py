from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from decimal import Decimal
from datetime import datetime
import os


class Index:  # класс для создания объекта "индекс"
    def __init__(self, id: str, symbol_position: str):
        self.id: str = id
        self.symbol_position: str = symbol_position  # позиция в файле

    @staticmethod  # статический метод для создания пути к файлу, принимает путь к корневой директории и имя файла
    def dir(root_directory_path: str, models_f: str) -> str:
        return os.path.join(root_directory_path, models_f)  # возвращает полный путь к файлу

    @staticmethod  # статический метод для чтения и кэширования индексов из файла
    def index_cash(table_dir: str) -> list:
        cache_index: list = []  # пустой список для хранения индексов
        if os.path.exists(table_dir): # проверка, существует ли файл по указанному пути
            with open(table_dir, 'r') as table_file:  
                lines: list[str] = table_file.readlines()
                split_lines = [line.strip().split(',') for line in lines]  # разделение каждой строки по запятой
                return [Index(id=s_line[0], symbol_position=s_line[1]
                              ) for s_line in split_lines]  # возвращает объекты Index для каждой строки
        return cache_index  # возвращает пустой список, если файл не существует


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        self.models_f = 'models.txt'
        self.models_idx_f = 'models_index.txt'
        self.models_index = Index.index_cash(
            Index.dir(root_directory_path, self.models_f))  # загрузка индексов моделей из файла
        self.cars_f = 'cars.txt'
        self.cars_idx_f = 'cars_index.txt'
        self.cars_index = Index.index_cash(
            Index.dir(root_directory_path, self.cars_f))  # загрузка индексов автомобилей из файла
        self.sale_f = 'sales.txt'
        self.sale_idx_f = 'sales_index.txt'
        self.sales_index = Index.index_cash(
            Index.dir(root_directory_path, self.sale_f))  # загрузка индексов продаж из файла

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        with open(os.path.join(self.root_directory_path, self.models_f), 'a'
                  ) as model_file:  # открываем файл в режиме добавления ('a') для записи данных о машине
            # формируем строку с данными о машине и разделяем их запятыми
            # используем метод ljust(500) для выравнивания строки до 500 символов
            models_str: str = (
                f'{model.id},{model.name},{model.brand}'.ljust(500)
            )
            model_file.write(models_str + '\n')  # записываем сформированную строку в файл и добавляем перенос строки

        # создаем объект Index для новой машины
        # id - уникальный идентификатор машины, symbol_position - позиция в файле
        model_index: Index = Index(
            id=model.index(), symbol_position=str(len(self.models_index)))

        self.models_index.append(model_index)  # добавляем созданный объект Index в список model_index
        self.models_index.sort(key=lambda x: x.id) # сортируем список model_index по полю id

        with open(
            os.path.join(self.root_directory_path, self.models_idx_f), 'w'
        ) as idx_model_file:
            for model_index in self.models_index:  # проходим по каждому элементу в списке model_index
                idx_model_str: str = f'{
                    model_index.id},{model_index.symbol_position}'.ljust(50)
                idx_model_file.write(idx_model_str + '\n')
        return model  # возвращаем объект model, который был добавлен

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        with open(os.path.join(self.root_directory_path, self.cars_f),
                  'a') as cars_file:
            cars_str: str = (
                f'{car.vin},{car.model},'
                f'{car.price},{car.date_start},'
                f'{car.status}'.ljust(500)
            )
            cars_file.write(cars_str + '\n')

        car_index: Index = Index(
            id=car.index(), symbol_position=str(len(self.cars_index)))

        self.cars_index.append(car_index)
        self.cars_index.sort(key=lambda x: x.id)

        with open(
            os.path.join(self.root_directory_path, self.cars_idx_f), 'w'
        ) as cars_idx_file:
            for cars_index in self.cars_index:
                idx_model_str: str = (
                    f'{cars_index.id},{cars_index.symbol_position}'.ljust(50))
                cars_idx_file.write(idx_model_str + '\n')
        return car  # возвращаем объект car, который был добавлен

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        with open(  # открываем файл продаж в режиме добавления ('a') для записи данных о продаже
            os.path.join(self.root_directory_path, self.sale_f), 'a'
        ) as sale_file:
            sale_str: str = (
                f'{sale.sales_number},{sale.car_vin},'
                f'{sale.sales_date},{sale.cost}'.ljust(500)
            )
            sale_file.write(sale_str + '\n')

        sale_index: Index = Index(
            id=sale.index(), symbol_position=str(len(self.sales_index)))
        self.sales_index.append(sale_index)
        self.sales_index.sort(key=lambda x: x.id)

        with open(  # открываем файл индексов продаж в режиме записи ('w') для обновления индексов
            os.path.join(self.root_directory_path, self.sale_idx_f), 'w'
        ) as sales_idx_file:
            for sales_index in self.sales_index:  # проходим по каждому элементу в списке sales_index
                index_model_str: str = (  # формируем строку с данными индекса
                    f'{sales_index.id},{sales_index.symbol_position}'.ljust(50)
                )
                sales_idx_file.write(index_model_str + '\n')
            num_car_row: int = 0  # ищем номер соответствующей проданному автомобилю
            for car_index in self.cars_index:
                if car_index.id == sale.car_vin:
                    num_car_row: int = int(car_index.symbol_position)  # запоминаем позицию строки в файле

        with open(
            os.path.join(self.root_directory_path, self.cars_f), 'r+'
        ) as cars_file:
            cars_file.seek((501) * num_car_row)  # перемещаем указатель файла на начало строки, соответствующей проданному автомобилю
            row_value: str = cars_file.read(500)
            car_row_line: list = row_value.strip().split(',')
            cars_file.seek((500) * num_car_row)  # перемещаем указатель файла на начало строки для перезаписи
            format_str = (  # формируем новую строку с обновленным статусом автомобиля
                row_value.replace(car_row_line[4], CarStatus.sold).
                ljust(500)
            )
            cars_file.write(format_str)

        car = Car(  # создаем объект Car с обновленным статусом
            vin=str(car_row_line[0]),
            model=int(car_row_line[1]),
            price=Decimal(car_row_line[2]),
            date_start=datetime.strptime(car_row_line[3], "%Y-%m-%d %H:%M:%S"),
            status=CarStatus.sold
        )
        return car  # возвращаем объект Car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        with open(
            os.path.join(self.root_directory_path, self.cars_f), 'r'
        ) as cars_file:
            cars_line: list[str] = cars_file.readlines() # читаем все строки из файла и сохраняем их в список cars_line
            # разбиваем каждую строку на части по запятым и удаляем лишние пробелы, результат сохраняем в список split_lines
            split_lines = [line.strip().split(',') for line in cars_line] 
            return [
                Car(vin=s_line[0], model=s_line[1], price=s_line[2],
                    date_start=s_line[3], status=s_line[4])
                for s_line in split_lines if s_line[-1] == status  # фильтруем строки: оставляем только те, где статус совпадает с переданным значением
            ]  # возвращаем список объектов Car, отфильтрованных по статусу

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # инициализация переменных для хранения позиций строк в файлах
        num_model_row: int = 0
        num_sale_row: int = 0

        if not self.cars_index:
            self.cars_index = Index.index_cash(
                Index.dir(self.root_directory_path, self.cars_f))

        if not self.sales_index:
            self.sales_index = Index.index_cash(
                Index.dir(self.root_directory_path, self.sale_f))

        if not self.models_index:
            self.models_index = Index.index_cash(
                Index.dir(self.root_directory_path, self.models_f))

        cars = {  # создаем словарь cars, где ключом является VIN автомобиля, а значением — позиция строки в файле
            car_index.id: car_index.symbol_position for car_index in self.cars_index}

        if vin not in cars.keys():
            return None

        num_car_row: str = cars.get(vin)  # получаем позицию строки для переданного VIN

        with open(
            os.path.join(self.root_directory_path, self.cars_f), 'r'
        ) as cars_file:
            cars_file.seek(int(num_car_row) * (501))
            car_row_value: str = cars_file.read(500)
            car_value: list = car_row_value.strip().split(',')

        for model_index in self.models_index:  # ищем позицию строки соответствующую модели автомобиля
            if model_index.id != car_value[1]:
                continue
            num_model_row: str = model_index.symbol_position

        with open(
            os.path.join(self.root_directory_path, self.models_f), 'r'
        ) as models_file:
            models_file.seek(int(num_model_row) * 501)
            model_row_value: str = models_file.read(500)
            model_value: list = model_row_value.strip().split(',')

        for sale_index in self.sales_index:  # ищем позицию строки соответствующую продаже автомобиля
            if sale_index.id != car_value[0]:
                continue
            num_sale_row: str = sale_index.symbol_position

        if os.path.exists(os.path.join(self.root_directory_path, self.sale_f)):
            with open(
                os.path.join(self.root_directory_path, self.sale_f), 'r'
            ) as sales_file:
                sales_file.seek(int(num_sale_row) * 501)
                sale_row_value: str = sales_file.read(500)
                sale_value: list = sale_row_value.strip().split(',')

        parameters: dict = dict(  # создаем словарь с информацией об автомобиле
            vin=car_value[0],
            car_model_name=model_value[1],
            car_model_brand=model_value[2],
            price=car_value[2],
            date_start=car_value[3],
            status=car_value[4],
            sales_date=None if car_value[4] != CarStatus.sold else sale_value[2], # дата продажи (если автомобиль продан)
            sales_cost=None if car_value[4] != CarStatus.sold else sale_value[3] # стоимость продажи (если автомобиль продан)
        )
        return CarFullInfo(**parameters) # передаем конструктору класса словарь и распаковываем его

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        if not self.cars_index:
            self.cars_index = Index.index_cash(
                Index.dir(self.root_directory_path, self.cars_f))

        cars = {
            car_index.id: car_index.symbol_position for car_index in self.cars_index}
        cars_index = [Index(id=new_vin, symbol_position=car_index.symbol_position) # обновляем список заменяя старый VIN на новый
                      if car_index.id == vin else car_index for car_index in self.cars_index]
        self.cars_index = cars_index  # обновляем новым списком
        self.cars_index.sort(key=lambda x: x.id)  # сортируем список по полю id

        with open(
            os.path.join(self.root_directory_path, self.cars_idx_f), 'w'
        ) as cars_idx_file:
            for car_index in cars_index:
                cars_idx_file.write(
                    f'{car_index.id},{car_index.symbol_position}'.ljust(500))

        num_car_row = cars.get(vin)  # получаем позицию строки для старого VIN

        with open(
            os.path.join(self.root_directory_path, self.cars_f), 'r+'
        ) as cars_file:
            cars_file.seek((501) * int(num_car_row))
            row_value: str = cars_file.read(500)
            car_row_line: list = row_value.strip().split(',')
            cars_file.seek(int(num_car_row))
            cars_file.write(row_value.replace(
                car_row_line[0], new_vin).ljust(500))

        car = Car(  # создаем объект Car с обновленным VIN
            vin=new_vin,
            model=car_row_line[1],
            price=car_row_line[2],
            date_start=car_row_line[3],
            status=car_row_line[4]
        )
        return car  # возвращаем объект Car

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        car_vin = None  # инициализация переменной для хранения VIN автомобиля
        with open(
            os.path.join(self.root_directory_path, self.sale_f), 'r'
        ) as sales_read:
            file_value: list = sales_read.readlines()  # читаем все строки и сохраняем их в список
        with open(
            os.path.join(self.root_directory_path, self.sale_f), 'w'
        ) as sales_write:
            for value in file_value:  # проходим по каждой строке из file_value
                if sales_number not in value: # если номер продажи отсутствует в строке, записываем её обратно в файл
                    sales_write.write(value)
                else:
                    car_vin = value.strip().split(',')[1]  # если номер продажи найден, извлекаем VIN автомобиля из строки

        with open(
            os.path.join(self.root_directory_path, self.sale_idx_f), 'r'
        ) as sales_read_idx:
            file_value: list = sales_read_idx.readlines()
        with open(
            os.path.join(self.root_directory_path, self.sale_idx_f), 'w'
        ) as sales_write_idx:
            for value in file_value:
                if car_vin not in value:
                    sales_write_idx.write(value)

        if not self.cars_index:
            self.cars_index = Index.index_cash(
                Index.dir(self.root_directory_path, self.cars_f))

        cars = {
            car_index.id: car_index.symbol_position for car_index in self.cars_index}
        num_car_row: str = cars.get(car_vin)  # получаем позицию строки для VIN автомобиля

        with open(
            os.path.join(self.root_directory_path, self.cars_f), 'r+'
        ) as cars_file:
            cars_file.seek(int(num_car_row) * (501))
            car_row_value: str = cars_file.read(500)
            car_value: list = car_row_value.strip().split(',')
            cars_file.seek(int(num_car_row) * (501))
            cars_file.write(car_row_value.replace(
                car_value[4], CarStatus.available).ljust(500))

        car = Car(
            vin=car_value[0],
            model=car_value[1],
            price=car_value[2],
            date_start=car_value[3],
            status=car_value[4]
        )
        return car  # возвращаем объект Car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        with open(
            os.path.join(self.root_directory_path, self.sale_f), 'r'
        ) as sales_read:
            file_value: list = sales_read.readlines()

        sales_history = dict()
        for value in file_value:
            value_item: list = value.strip().split(',')
            sales_history[value_item[1]] = value_item[3]

        if not self.cars_index:
            self.cars_index = Index.index_cash(
                Index.dir(self.root_directory_path, self.cars_f))

        cars_row: list = [int(car_index.symbol_position)
                          for car_index in self.cars_index if car_index.id in sales_history.keys()]
        with open(
            os.path.join(self.root_directory_path, self.cars_f), 'r'
        ) as cars_read:
            salon_cars: dict = {
                row_value.strip().split(',')[0]: row_value.strip().split(',')[1]
                for row_number, row_value in enumerate(cars_read.readlines())
                if row_number in cars_row and row_value != '\n'
            }

        if not self.models_index:
            self.models_index = Index.index_cash(
                Index.dir(self.root_directory_path, self.models_f))
        models_row: list = [
            model_index.symbol_position
            for model_index in self.models_index
            if model_index.id in salon_cars.values()
        ]
        with open(
            os.path.join(self.root_directory_path, self.models_f), 'r'
        ) as models_read_file:
            salon_models: dict = {row_value.strip().split(',')[0]: [
                row_value.strip().split(',')[1],
                row_value.strip().split(',')[2]
                ]
                for row_number, row_value in enumerate(models_read_file)
                if str(row_number) in models_row
            }
        pivot_table: list = []  # cоздаем сводную таблицу, содержащую информацию о продажах моделей
        for car_vin, car_models in salon_cars.items():
            brand_model = salon_models.get(car_models)  # получаем данные о модели из словаря
            price = sales_history.get(car_vin)  # получаем цену продажи из словаря
            pivot_table.append([brand_model[0], brand_model[1], price])  # добавляем запись в сводную таблицу
        list_total = []  # инициализация списка для хранения итоговых данных
        group_table: list = []
        for value in salon_models.values():
            count_item = sum(i[0] == value[0] and i[1] == value[1]  # считаем количество продаж для каждой модели
                             for i in pivot_table)
            price = sum(float(i[2]) for i in pivot_table if i[0]  # считаем общую сумму продаж для каждой модели
                        == value[0] and i[1] == value[1])
            group_table.append([value[0], value[1], count_item, price])  # добавляем запись в групповую таблицу
        group_table = sorted(group_table, key=lambda x: (  # сортируем таблицу по количеству продаж и общей сумме (в порядке убывания) и выбираем топ-3
            x[2], x[3]), reverse=True)[:3]
        for value in group_table:  # формируем итоговый список
            list_total.append(ModelSaleStats(
                car_model_name=value[0], brand=value[1], sales_number=value[2]))
        return list_total[:3]  # возвращаем топ-3 моделей по продажам
