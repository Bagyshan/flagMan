import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import datetime
import time
from collections import defaultdict
from config.settings import CARS_BASE_TOKEN


class CarMarksAPIView(APIView):
    """
    Возвращает список марок (marks)
    """
    def get(self, request):
        response = requests.get("https://cars-base.ru/api/cars/")
        if response.status_code == 200:
            return Response(response.json())
        return Response({"error": "Ошибка при запросе к cars-base.ru"}, status=status.HTTP_502_BAD_GATEWAY)





@extend_schema(
    parameters=[
        OpenApiParameter(name='mark', required=True, type=str, description='Марка авто'),
    ],
    description='Получить список моделей по марке'
)
class CarModelsAPIView(APIView):
    """
    Возвращает список моделей по марке (mark)
    """
    def get(self, request):
        mark = request.query_params.get("mark")
        if not mark:
            return Response({"error": "mark is required"}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(f"https://cars-base.ru/api/cars/{mark}")
        if response.status_code == 200:
            return Response(response.json())
        return Response({"error": "Ошибка при запросе к cars-base.ru"}, status=status.HTTP_502_BAD_GATEWAY)
    



@extend_schema(
    parameters=[
        OpenApiParameter(name='mark', required=True, type=str, description='Марка авто'),
        OpenApiParameter(name='model', required=True, type=str, description='Модель авто'),
    ],
    description='Получить список годов по марке и модели'
)
class CarYearAPIView(APIView):
    def get(self, request):
        mark = request.query_params.get("mark")
        model = request.query_params.get("model")
        if not mark or not model:
            return Response({"error": "mark and model are required"}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(f"https://cars-base.ru/api/cars/{mark}/{model}?key={CARS_BASE_TOKEN}")

        if response.status_code != 200:
            return Response({"error": "Ошибка при запросе к cars-base"}, status=status.HTTP_502_BAD_GATEWAY)

        data = response.json()

        # Извлечение только notice из каждой конфигурации
        start_year = 100000
        end_year = 0
        start = time.time()
        years_set = set()

        for car in data:
            if car.get("year-stop") == None:
                years_set.update(range(car.get("year-start"), datetime.now().year + 1))
            else:
                years_set.update(range(car.get("year-start"), car.get("year-stop") + 1))

        final_lsit = sorted(years_set)
        end = time.time()
        print(f"Время выполнения: {end - start:.8f} секунд")
        # for item in data:
        #     if item.get("year-start") < start_year:
        #         start_year = item.get("year-start")
        #     if item.get("year-stop") == None:
        #         end_year = datetime.now().year
        #         continue
        #     if item.get("year-stop") > end_year and item.get("year-stop") != None:
        #         end_year = item.get("year-stop")
        
        # list_of_years = []
        # for i in range(start_year, end_year + 1):
        #     list_of_years.append(i)

        return Response(final_lsit)




@extend_schema(
    parameters=[
        OpenApiParameter(name='mark', required=True, type=str, description='Марка авто'),
        OpenApiParameter(name='model', required=True, type=str, description='Модель авто'),
        OpenApiParameter(name='year', required=True, type=int, description='Год выпуска авто')
    ],
    description='Получить список поколений по марке и модели'
)
class CarGenerationsAPIView(APIView):
    """
    Возвращает список поколений по mark и model
    """
    def get(self, request):
        mark = request.query_params.get("mark")
        model = request.query_params.get("model")
        year = request.query_params.get("year")
        try:
            year = int(year)
        except ValueError:
            return Response({"error": "year must be an integer"}, status=400)
        if not mark or not model:
            return Response({"error": "mark and model are required"}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(f"https://cars-base.ru/api/cars/{mark}/{model}?key={CARS_BASE_TOKEN}")
        
        if response.status_code != 200:
            return Response({"error": "Ошибка при запросе к cars-base"}, status=status.HTTP_502_BAD_GATEWAY)

        data = response.json()

        list_of_generations = []
        for car in data:
            if car.get("year-start") <= year and (car.get("year-stop") == None or car.get("year-stop") >= year):
                list_of_generations.append(car)

        return Response(list_of_generations)
            
    





# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='mark', required=True, type=str),
#         OpenApiParameter(name='model', required=True, type=str),
#         OpenApiParameter(name='generation', required=True, type=str),
#     ],
#     description="Получить список полей `notice` у всех конфигураций"
# )
# class CarNoticeListAPIView(APIView):
#     def get(self, request):
#         mark = request.query_params.get("mark")
#         model = request.query_params.get("model")
#         generation = request.query_params.get("generation")


#         if not mark or not model or not generation:
#             return Response(
#                 {"error": "Параметры mark, model и generation обязательны"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         url = f"https://cars-base.ru/api/cars/{mark}/{model}/{generation}?key=117da441a"
#         response = requests.get(url)

#         if response.status_code != 200:
#             return Response({"error": "Ошибка при запросе к cars-base"}, status=status.HTTP_502_BAD_GATEWAY)

#         data = response.json()

#         # Извлечение только notice из каждой конфигурации
#         notices = set(item.get("notice") for item in data if "notice" in item)
#         notices_list = list(notices)

#         return Response(notices)
    

# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='mark', required=True, type=str),
#         OpenApiParameter(name='model', required=True, type=str),
#         OpenApiParameter(name='generation', required=True, type=str),
#     ],
#     description="Получить список полей `steering-wheel` у всех конфигураций"
# )
# class CarSteeringWheelsListAPIView(APIView):
#     def get(self, request):
#         mark = request.query_params.get("mark")
#         model = request.query_params.get("model")
#         generation = request.query_params.get("generation")


#         if not mark or not model or not generation:
#             return Response(
#                 {"error": "Параметры mark, model и generation обязательны"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         url = f"https://cars-base.ru/api/cars/{mark}/{model}/{generation}?key=117da441a"
#         response = requests.get(url)

#         if response.status_code != 200:
#             return Response({"error": "Ошибка при запросе к cars-base"}, status=status.HTTP_502_BAD_GATEWAY)

#         data = response.json()

#         # Извлечение только notice из каждой конфигурации
#         steering_wheels = set(item.get("steering-wheel") for item in data if "steering-wheel" in item)
#         steering_wheels_list = list(steering_wheels)

#         return Response(steering_wheels_list)



# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='mark', required=True, type=str),
#         OpenApiParameter(name='model', required=True, type=str),
#         OpenApiParameter(name='generation', required=True, type=str),
#     ],
#     description="Получить список полей `engine-type` у всех конфигураций"
# )
# class CarEngineTypeListAPIView(APIView):
#     """
#     Возвращает список уникальных значений engine-type
#     из конфигураций, полученных по API cars-base
#     """

#     def get(self, request):
#         mark = request.query_params.get("mark")
#         model = request.query_params.get("model")
#         generation = request.query_params.get("generation")

#         if not mark or not model or not generation:
#             return Response({"error": "mark, model и generation обязательны"}, status=status.HTTP_400_BAD_REQUEST)

#         url = f"https://cars-base.ru/api/cars/{mark}/{model}/{generation}?key=117da441a"
#         try:
#             response = requests.get(url)
#             data = response.json()
#         except Exception as e:
#             return Response({"error": "Ошибка запроса к API"}, status=status.HTTP_502_BAD_GATEWAY)

#         engine_types = set()

#         for config in data:
#             for mod in config.get("modifications", []):
#                 specs = mod.get("specifications", {})
#                 engine = specs.get("engine-type")
#                 if engine:
#                     engine_types.add(engine)

#         return Response(sorted(engine_types))
    


# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='mark', required=True, type=str),
#         OpenApiParameter(name='model', required=True, type=str),
#         OpenApiParameter(name='generation', required=True, type=str),
#     ],
#     description="Получить список полей `transmission` у всех конфигураций"
# )
# class CarTransmissionListAPIView(APIView):
#     """
#     Возвращает список уникальных значений engine-type
#     из конфигураций, полученных по API cars-base
#     """

#     def get(self, request):
#         mark = request.query_params.get("mark")
#         model = request.query_params.get("model")
#         generation = request.query_params.get("generation")

#         if not mark or not model or not generation:
#             return Response({"error": "mark, model и generation обязательны"}, status=status.HTTP_400_BAD_REQUEST)

#         url = f"https://cars-base.ru/api/cars/{mark}/{model}/{generation}?key=117da441a"
#         try:
#             response = requests.get(url)
#             data = response.json()
#         except Exception as e:
#             return Response({"error": "Ошибка запроса к API"}, status=status.HTTP_502_BAD_GATEWAY)

#         engine_types = set()

#         for config in data:
#             for mod in config.get("modifications", []):
#                 specs = mod.get("specifications", {})
#                 engine = specs.get("transmission")
#                 if engine:
#                     engine_types.add(engine)

#         return Response(sorted(engine_types))
    


# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='mark', required=True, type=str),
#         OpenApiParameter(name='model', required=True, type=str),
#         OpenApiParameter(name='generation', required=True, type=str),
#     ],
#     description="Получить список полей `drive` у всех конфигураций"
# )
# class CarDriveListAPIView(APIView):
#     """
#     Возвращает список уникальных значений engine-type
#     из конфигураций, полученных по API cars-base
#     """

#     def get(self, request):
#         mark = request.query_params.get("mark")
#         model = request.query_params.get("model")
#         generation = request.query_params.get("generation")

#         if not mark or not model or not generation:
#             return Response({"error": "mark, model и generation обязательны"}, status=status.HTTP_400_BAD_REQUEST)

#         url = f"https://cars-base.ru/api/cars/{mark}/{model}/{generation}?key=117da441a"
#         try:
#             response = requests.get(url)
#             data = response.json()
#         except Exception as e:
#             return Response({"error": "Ошибка запроса к API"}, status=status.HTTP_502_BAD_GATEWAY)

#         engine_types = set()

#         for config in data:
#             for mod in config.get("modifications", []):
#                 specs = mod.get("specifications", {})
#                 engine = specs.get("drive")
#                 if engine:
#                     engine_types.add(engine)

#         return Response(sorted(engine_types))
    


# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='mark', required=True, type=str),
#         OpenApiParameter(name='model', required=True, type=str),
#         OpenApiParameter(name='generation', required=True, type=str),
#     ],
#     description="Получить список полей `modification-name` у всех конфигураций"
# )
# class CarModificationNameListAPIView(APIView):
#     """
#     Возвращает список уникальных значений engine-type
#     из конфигураций, полученных по API cars-base
#     """

#     def get(self, request):
#         mark = request.query_params.get("mark")
#         model = request.query_params.get("model")
#         generation = request.query_params.get("generation")

#         if not mark or not model or not generation:
#             return Response({"error": "mark, model и generation обязательны"}, status=status.HTTP_400_BAD_REQUEST)

#         url = f"https://cars-base.ru/api/cars/{mark}/{model}/{generation}?key=117da441a"
#         try:
#             response = requests.get(url)
#             data = response.json()
#         except Exception as e:
#             return Response({"error": "Ошибка запроса к API"}, status=status.HTTP_502_BAD_GATEWAY)

#         engine_types = set()

#         for config in data:
#             for mod in config.get("modifications", []):
#                 # specs = mod.get("specifications", {})
#                 engine = mod.get("group-name")
#                 if engine:
#                     engine_types.add(engine)

#         return Response(sorted(engine_types))



# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='mark', required=True, type=str, description='Марка авто'),
#         OpenApiParameter(name='model', required=True, type=str, description='Модель авто'),
#         OpenApiParameter(name='generation', required=True, type=str, description='Поколение авто'),
#         OpenApiParameter(name='notice', required=True, type=str, description='Тип кузова'),
#         OpenApiParameter(name='engine-type', required=False, type=str, description='Двигатель'),
#         OpenApiParameter(name='transmission', required=False, type=str, description='Коробка передач'),
#         OpenApiParameter(name='drive', required=False, type=str, description='Привод'),
#         OpenApiParameter(name='modification-name', required=False, type=str, description='Модификация'),
#         OpenApiParameter(name='steering-wheel', required=False, type=str, description='Руль'),
#     ],
#     description='Получить список конфигурация по марке, модели и поколению'
# )
# class CarOtherConfigurationsAPIView(APIView):

#     def filter_car_data(data, notice=None, engine_type=None, drive=None, transmission=None, modification_name=None ,steering_wheel=None):
#         filtered = []

#         for car in data:
#             # фильтрация по верхнеуровневым полям
#             if notice and car.get("notice") != notice:
#                 continue
#             if steering_wheel and car.get("steering-wheel") != steering_wheel:
#                 continue

#             # фильтрация модификаций
#             mods = []
#             for mod in car.get("modifications", []):
#                 specs = mod.get("specifications", {})

#                 if modification_name and mod.get("group-name") != modification_name:
#                     continue
#                 if engine_type and specs.get("engine-type") != engine_type:
#                     continue
#                 if drive and specs.get("drive") != drive:
#                     continue
#                 if transmission and specs.get("transmission") != transmission:
#                     continue

#                 mods.append(mod)

#             # добавляем, если остались подходящие модификации
#             if mods:
#                 car_copy = car.copy()
#                 car_copy["modifications"] = mods
#                 filtered.append(car_copy)

#         return filtered

#     """
#     Возвращает список конфигураций по mark, model и generation
#     """
#     def get(self, request):
#         mark = request.query_params.get("mark")
#         model = request.query_params.get("model")
#         generation = request.query_params.get("generation")
#         notice = request.query_params.get("notice")
#         engine_type = request.query_params.get("engine-type")
#         transmission = request.query_params.get("transmission")
#         drive = request.query_params.get("drive")
#         modification_name = request.query_params.get("modification-name")
#         steering_wheel = request.query_params.get("steering-wheel")

#         if not mark or not model or not generation or not notice:
#             return Response({"error": "mark, model, generation and notice are required"}, status=status.HTTP_400_BAD_REQUEST)

#         url = f"https://cars-base.ru/api/cars/{mark}/{model}/{generation}?key=117da441a"
#         response = requests.get(url)

#         if response.status_code != 200:
#             return Response({"error": "Ошибка при запросе к cars-base"}, status=status.HTTP_502_BAD_GATEWAY)

#         data = response.json()

#         filtered = CarOtherConfigurationsAPIView.filter_car_data(
#             data,
#             notice=notice,
#             engine_type=engine_type,
#             drive=drive,
#             transmission=transmission,
#             modification_name=modification_name,
#             steering_wheel=steering_wheel
#         )

#         return Response(filtered)



@extend_schema(
    parameters=[
        OpenApiParameter(name='mark', required=True, type=str, description='Марка авто'),
        OpenApiParameter(name='model', required=True, type=str, description='Модель авто'),
        OpenApiParameter(name='generation', required=True, type=str, description='Поколение авто'),
        OpenApiParameter(name='notice', required=False, type=str, description='Тип кузова'),
        OpenApiParameter(name='engine-type', required=False, type=str, description='Двигатель'),
        OpenApiParameter(name='transmission', required=False, type=str, description='Коробка передач'),
        OpenApiParameter(name='drive', required=False, type=str, description='Привод'),
        OpenApiParameter(name='modification-name', required=False, type=str, description='Модификация'),
        OpenApiParameter(name='steering-wheel', required=False, type=str, description='Руль'),
    ],
    description='Получить фильтруемые поля конфигураций по mark, model и generation'
)
class CarOtherConfigurationsAPIView(APIView):

    def get(self, request):
        mark = request.query_params.get("mark")
        model = request.query_params.get("model")
        generation = request.query_params.get("generation")

        # фильтрующие параметры
        notice = request.query_params.get("notice")
        engine_type = request.query_params.get("engine-type")
        transmission = request.query_params.get("transmission")
        drive = request.query_params.get("drive")
        modification_name = request.query_params.get("modification-name")
        steering_wheel = request.query_params.get("steering-wheel")

        if not mark or not model or not generation:
            return Response({"error": "mark, model и generation обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        url = f"https://cars-base.ru/api/cars/{mark}/{model}/{generation}?key={CARS_BASE_TOKEN}"
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Ошибка при запросе к cars-base"}, status=status.HTTP_502_BAD_GATEWAY)

        data = response.json()

        # Словарь уникальных значений
        result = defaultdict(set)

        for car in data:
            if notice and car.get("notice") != notice:
                continue
            if steering_wheel and car.get("steering-wheel") != steering_wheel:
                continue

            result["notice"].add(car.get("notice"))
            result["steering_wheel"].add(car.get("steering-wheel"))

            for mod in car.get("modifications", []):
                specs = mod.get("specifications", {})

                if modification_name and mod.get("group-name") != modification_name:
                    continue
                if engine_type and specs.get("engine-type") != engine_type:
                    continue
                if drive and specs.get("drive") != drive:
                    continue
                if transmission and specs.get("transmission") != transmission:
                    continue

                result["modification_name"].add(mod.get("group-name"))
                result["engine_type"].add(specs.get("engine-type"))
                result["drive"].add(specs.get("drive"))
                result["transmission"].add(specs.get("transmission"))

        # Преобразуем множества в списки и удалим пустые
        result_json = {k: list(filter(None, v)) for k, v in result.items() if v}

        return Response(result_json)
    




{
    "notice": [
        "седан",
        "универсал"
        ],
    "engine_type": [
        "бензин"
    ],
    "drive": [
        "полный",
        "задний"
    ],
    "transmission": [
        "автоматическая",
        "механическая"
    ]
}