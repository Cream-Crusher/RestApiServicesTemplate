from dataclasses import dataclass


@dataclass
class ToolText:
    mailing_confirmation = "Подтвердите рассылку 🛫"
    mailing_confirmated = "Рассылка началась.\n\nПо окончанию мы уведомим вас о её завершении."
    mailing_end = "Рассылка была успешно проведена"
    mailing_canceled = "Рассылка была отменена"
