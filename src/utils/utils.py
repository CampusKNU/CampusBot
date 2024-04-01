from datetime import datetime

def get_info_text(event):
    if event:
        formatted_message = f"<b>Назва:</b> {event.title}\n"
        formatted_message += f"<b>Опис:</b> {event.description}\n"
        formatted_message += f"<b>Посилання:</b> {event.link}\n"
        formatted_message += f"<b>Статус:</b> {event.status}\n"
        formatted_message += f"<b>Дата:</b> {event.date.strftime('%d.%m.%Y')}\n"
        #formatted_message += f"Created: {event.to_created.strftime('%d.%m.%Y %H:%M')}\n"
        return formatted_message
    else:
        return "Event not found or provided event is None."
    

def is_valid_date(date_str):
    try:
        date_format = "%d.%m.%Y"
        result = datetime.strptime(date_str, date_format)
        return result
    except ValueError:
        return False