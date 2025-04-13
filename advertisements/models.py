from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core.exceptions import ValidationError

# Create your models here.

User = get_user_model()


def validate_kg_phone(value):
    if value.startswith("+996") and len(value) == 13 and value[4:].isdigit():
        return
    raise ValidationError(_('Номер телефона должен начинаться с +996 и содержать ровно 9 цифр.'))

class Complectation(models.Model):
    body_kit = models.BooleanField(_("обвес"), null=True, blank=True)
    tinting = models.BooleanField(_("тонировка"), null=True, blank=True)
    spoiler = models.BooleanField(_("спойлер"), null=True, blank=True)
    alloy_wheels = models.BooleanField(_("литые диски"), null=True, blank=True)
    luke = models.BooleanField(_("люк"), null=True, blank=True)
    winch = models.BooleanField(_("лебёдка"), null=True, blank=True)
    roof_rails = models.BooleanField(_("рейлинги"), null=True, blank=True)
    trunk = models.BooleanField(_("багажник"), null=True, blank=True)
    tow_bar = models.BooleanField(_("фаркоп"), null=True, blank=True)
    panoramic_roof = models.BooleanField(_("панорамная крыша"), null=True, blank=True)
    velours = models.BooleanField(_("велюр"), null=True, blank=True)
    leather = models.BooleanField(_("кожа"), null=True, blank=True)
    curtains = models.BooleanField(_("шторки"), null=True, blank=True)
    alcantara = models.BooleanField(_("алькантара"), null=True, blank=True)
    combined = models.BooleanField(_("комбинированный салон"), null=True, blank=True)
    wood = models.BooleanField(_("дерево"), null=True, blank=True)
    CD = models.BooleanField(_("CD"), null=True, blank=True)
    DVD = models.BooleanField(_("DVD"), null=True, blank=True)
    MP3 = models.BooleanField(_("MP3"), null=True, blank=True)
    USB = models.BooleanField(_("USB"), null=True, blank=True)
    subwoofer = models.BooleanField(_("сабвуфер"), null=True, blank=True)
    ABS = models.BooleanField(_("антиблокировочная система ABS"), null=True, blank=True)
    traction_control_system = models.BooleanField(_("антипробуксовочная система"), null=True, blank=True)
    stability_control_system = models.BooleanField(_("система курсовой устойчивости"), null=True, blank=True)
    airbags = models.BooleanField(_("подушки безопасности"), null=True, blank=True)
    parking_sensor = models.BooleanField(_("парктроник"), null=True, blank=True)
    rear_view_camera = models.BooleanField(_("камера заднего вида"), null=True, blank=True)
    camera_360 = models.BooleanField(_("камера 360"), null=True, blank=True)
    full_power_accessories = models.BooleanField(_("полный электропакет"), null=True, blank=True)
    signaling = models.BooleanField(_("сигнализация"), null=True, blank=True)
    car_plant = models.BooleanField(_("автозавод"), null=True, blank=True)
    conditioner = models.BooleanField(_("кондиционер"), null=True, blank=True)
    climate_control = models.BooleanField(_("климат контроль"), null=True, blank=True)
    gas_cylinder_equipment = models.BooleanField(_("газобалонное оборудование"), null=True, blank=True)
    cruise_control = models.BooleanField(_("круиз-котроль"), null=True, blank=True)
    heated_front_seats = models.BooleanField(_("подогрев передних сидений"), null=True, blank=True)
    heated_all_seats = models.BooleanField(_("подогрев всех сидений"), null=True, blank=True)
    heated_mirrors = models.BooleanField(_("обогрев зеркал"), null=True, blank=True)
    xenon = models.BooleanField(_("ксенон"), null=True, blank=True)
    bixenon = models.BooleanField(_("биксенон"), null=True, blank=True)
    headlight_washer = models.BooleanField(_("отмыватель фар"), null=True, blank=True)
    air_suspension = models.BooleanField(_("пневмоподвеска"), null=True, blank=True)
    seat_memory = models.BooleanField(_("память сидений"), null=True, blank=True)
    steering_memory = models.BooleanField(_("память руля"), null=True, blank=True)
    rain_sensor = models.BooleanField(_("датчик дождя"), null=True, blank=True)
    light_sensor = models.BooleanField(_("датчик света"), null=True, blank=True)
    onboard_computer = models.BooleanField(_("бортовой компьютер"), null=True, blank=True)
    headlight_range_control = models.BooleanField(_("корректор фар"), null=True, blank=True)
    central_locking = models.BooleanField(_("центральный замок"), null=True, blank=True)
    keyless_entry = models.BooleanField(_("бесключевой доступ"), null=True, blank=True)
    heated_steering_wheel = models.BooleanField(_("подогрев руля"), null=True, blank=True)
    seat_ventilation = models.BooleanField(_("вентиляция сидений"), null=True, blank=True)
    laser_headlights = models.BooleanField(_("лазерные фары"), null=True, blank=True)
    LED_headlights = models.BooleanField(_("светодиодные фары"), null=True, blank=True)

    created_at = models.DateTimeField(_("Время создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Время обновления"), auto_now=True)


class OtherBenefits(models.Model):
    recently_imported = models.BooleanField(_("свежепригнан"), null=True, blank=True)
    tax_paid = models.BooleanField(_("налог уплачен"), null=True, blank=True)
    technical_inspection_passed = models.BooleanField(_("техосмотр пройден"), null=True, blank=True)
    does_not_require_investment = models.BooleanField(_("вложений не требует"), null=True, blank=True)

    created_at = models.DateTimeField(_("Время создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Время обновления"), auto_now=True)
    


class Advertisement(models.Model):
    COLOR_CHOICES = [
        ('#000000', 'черный'),
        ('#C0C0C0', 'серебристый'),
        ('#FFFFFF', 'белый'),
        ('#808080', 'серый'),
        ('#F5F5DC', 'бежевый'),
        ('#30D5C8', 'бирюзовый'),
        ('#800000', 'бордовый'),
        ('#CD7F32', 'бронза'),
        ('#DE3163', 'вишня'),
        ('#87CEEB', 'голубой'),
        ('#FFFF00', 'жёлтый'),
        ('#008000', 'зеленый'),
        ('#FFD700', 'золотистый'),
        ('#A52A2A', 'коричневый'),
        ('#FF0000', 'красный'),
        ('#FFA500', 'оранжевый'),
        ('#FFC0CB', 'розовый'),
        ('#0000FF', 'синий'),
        ('#C8A2C8', 'сиреневый'),
        ('#800080', 'фиолетовый'),
        ('#7FFFD4', 'хамелеон'), 
        ('#580F41', 'баклажан'),
    ]

    STATE_CHOICES = {
        ('good', 'хорошее'),
        ('great', 'отличное'),
        ('bad', 'аварийное / не на ходу'),
        ('new', 'новое'),
    }

    AVAILABILITY_IN_KYRGYZSTAN_CHOICES = {
        ('yes', 'в наличии'),
        ('with order', 'на заказ'),
        ('in road', 'в пути'),
    }

    COUNTRY_OF_REGISTRATION_CHOICES = {
        ('kyrgyzstan', 'Кыргызстан'),
        ('not registered', 'Не стоит на учете')
    }

    POSSIBILITY_OF_EXCHANGE_CHOICES = {
        ('consider the options', 'рассмотрю варианты'),
        ('with additional payment by the buyer', 'с доплатой покупателя'),
        ('with seller surcharge', 'с доплатой продавца'),
        ('key to key', 'ключ на ключ'),
        ('do not offer exchange', 'обмен не предлагать'),
        ('exchange for real estate', 'обмен на недвижимость'),
        ('exchange only', 'только обмен'),
    }

    CURRENCY_CHOICES ={
        ('som', 'сом'),
        ('USD', 'долл. США'),
    }

    REGION_CHOICES = {
        ('chui', 'Чуйская область'),
        ('ik', 'Иссык-Кульская область'),
        ('talas', 'Таласская область'),
        ('naryn', 'Нарынская область'),
        ('jalal-abad', 'Джалал-Абадская область'),
        ('osh', 'Ошская область'),
        ('batken', 'Баткенская область'),
    }

    CITY_CHOICES = {
        ('bishkek', 'Бишкек'),
        ('osh', 'Ош')
    }

    PERMISSION_TO_COMMENT_CHOICES = {
        ('nobody', 'никто'),
        ('authenticated', 'зарегистрированные пользователи')
    }

    UNITS_OF_MILEAGE_CHOICES = {
        ('km', 'км'),
        ('mile', 'миль')
    }

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='advertisements',
        verbose_name=_('Владелец')
    )
    mark = models.CharField(_('Марка авто'))
    model = models.CharField(_('Модель авто'))
    year_of_manufacture = models.IntegerField(_('Год выпуска'))
    generation = models.IntegerField(_('Поколение авто'))
    notice = models.CharField(_('Тип кузова'))
    engine_type = models.CharField(_('Тип двигателя'))
    drive = models.CharField(_('Привод'))
    transmission = models.CharField(_('Коробка передач'))
    modification = models.CharField(_('Модификация авто'), null=True, blank=True)
    steering_wheel = models.CharField(_('Руль'))

    color = models.CharField(_('Цвет'), choices=COLOR_CHOICES)
    complectation = models.OneToOneField(
        Complectation,
        on_delete=models.SET_NULL,
        related_name="advertisement",
        null=True,
        blank=True,
        verbose_name=_("Комплектация")
    )
    state = models.CharField(_('Состояние'), choices=STATE_CHOICES)
    mileage = models.IntegerField(_('Пробег'))
    units_of_mileage = models.CharField(_("Еденицы измерения пробега"), choices=UNITS_OF_MILEAGE_CHOICES)
    availability_in_kyrgyzstan = models.CharField(_('Наличие в Кыргызстане'), choices=AVAILABILITY_IN_KYRGYZSTAN_CHOICES)
    customs_in_kyrgyzstan = models.BooleanField(_('Растаможен в Кыргызстане'), null=True, blank=True)
    urgently = models.BooleanField(_("Срочно"), null=True, blank=True)
    country_of_registration = models.CharField(_('Страна регистрации'), choices=COUNTRY_OF_REGISTRATION_CHOICES)
    possibility_of_exchange = models.CharField(_('Возможность обмена'), choices=POSSIBILITY_OF_EXCHANGE_CHOICES, null=True, blank=True)
    possibility_of_installments = models.BooleanField(_('Возможность рассрочки'), null=True, blank=True)
    other = models.OneToOneField(
        OtherBenefits,
        on_delete=models.SET_NULL,
        related_name="advertisement",
        null=True,
        blank=True,
        verbose_name=_("Прочее")
    )

    currency = models.CharField(_('Валюта'), choices=CURRENCY_CHOICES, default='USD')
    price = models.IntegerField(_('Цена'))
    region = models.CharField(_('Регион'), choices=REGION_CHOICES)
    city = models.CharField(_('Город'), choices=CITY_CHOICES)
    permission_to_comment = models.CharField(_('Кто может комментировать'), choices=PERMISSION_TO_COMMENT_CHOICES, null=True, blank=True)
    description = models.TextField(_('Описание'), max_length=500, null=True, blank=True)

    phone_number = models.CharField(_("Номер телефона"), validators=[validate_kg_phone])

    created_at = models.DateTimeField(_("Время создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Время обновления"), auto_now=True)



class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_('Объявление')
    )
    image = models.ImageField(_('Изображение'), upload_to='advertisement/')

    created_at = models.DateTimeField(_("Время создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Время обновления"), auto_now=True)


