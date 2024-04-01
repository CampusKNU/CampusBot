from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
	KeyboardButton,
	Message,
	ReplyKeyboardMarkup,
	InlineKeyboardMarkup,
	InlineKeyboardButton,
	ReplyKeyboardRemove,
)
from datetime import datetime
from src.database.db_manager import db_session, save_event, get_event_by_id, get_events, update_event
from ..utils.utils import get_info_text, is_valid_date
from src.bot import bot

router = Router()

class EventModel:
	TITLE = "title"
	DESCRIPTION = "description"
	LINK = "link"
	PHOTO_ID = "photo"
	STATUS = "status"
	DATE = "date"

	fields_name = {
		TITLE: "Назва",
		DESCRIPTION: "Опис", 
		LINK: "Посилання",
		PHOTO_ID: "Фото",
		STATUS: "Статус",
		DATE: "Дата",
	}


class EventCreationState(StatesGroup):
	TITLE = State()
	DESCRIPTION = State()
	LINK = State()
	PHOTO_ID = State()
	STATUS = State()
	DATE = State()
	TO_CREATED = State()


class EventUpdateState(StatesGroup):
	NEW_DATA = State()
	

class MenuButtons: 
	EVENTS = "Найближчі події 📆"
	ADD_EVENTS = "Додати подію 🖇"
	CHANGE_EVENT = "Змінити подію 📝"


class ExitButtons:
	EXIT_EVENT_REGISTRATION = "Відмінити реєстрацію події ❌"
	EXIT_EVENT_CHANGING = "Відмінити зміну події ❌"


@router.message(lambda message: message.text in menu_callback_function.keys())
async def button_handler(message: Message, state: FSMContext):
	text = message.text
	#logger.info(f'Received menu button request "{text}" from user {message.chat.id})')
	if text in menu_callback_function:
		if text == MenuButtons.ADD_EVENTS:
			await menu_callback_function[text](message, state)
		else:
			await menu_callback_function[text](message)

#@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
	await message.answer(f"Hello, {message.from_user.full_name}!", parse_mode=ParseMode.HTML)

@router.message(CommandStart())
async def menu(message, text="Меню"):
	custom_keyboard = []
	user_id = message.from_user.id
	for button_text in menu_callback_function.keys():
		custom_keyboard.append([types.KeyboardButton(text=button_text)])
	custom_keyboard = types.ReplyKeyboardMarkup(keyboard=custom_keyboard)
	await message.answer(text, reply_markup=custom_keyboard, parse_mode=ParseMode.HTML)


@router.callback_query(F.data.startswith("events_list"))
async def events_list_callback_handler(callback_query: CallbackQuery):
	return await events_list(callback_query.message)


async def sent_change_menu(message: Message, text):
	custom_keyboard = [[KeyboardButton(text=ExitButtons.EXIT_EVENT_REGISTRATION)]]
	reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard)
	
	try:
		await message.edit_text(text, reply_markup=reply_markup)
	except Exception as e:
		await message.answer(text, reply_markup=reply_markup)


async def events_list(message: Message):
	upcoming_events = get_events()
	if upcoming_events:
		events_message = f"{MenuButtons.EVENTS}:\n"
		buttons = []
		for event in upcoming_events:
			buttons.append([
				InlineKeyboardButton(text=f"{event.title} - {event.date}\n", callback_data=f"get_info_{event.id}")
				])
	else:
		events_message = "Поки немає запланованих подій 😔"
		try:
			await message.edit_text(events_message)
		except Exception as e:
			await message.answer(events_message)
		

	inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
	try:
		await message.edit_text(events_message, reply_markup=inline_keyboard)
	except Exception as e:
		await message.answer(events_message, reply_markup=inline_keyboard)


@router.callback_query(F.data.startswith("change_"))
async def change_field(callback_query: CallbackQuery, state: FSMContext):
	_, field, event_id = callback_query.data.split("_")
	event = get_event_by_id(event_id)
	if field == EventModel.PHOTO_ID:
		await callback_query.message.edit_text("Теперішнє фото:")
		await bot.send_photo(chat_id=callback_query.message.chat.id, photo=event.photo_id)
		await callback_query.message.answer("Надішли нове фото")
		await state.set_state(EventUpdateState.PHOTO_ID)
		await sent_change_menu(callback_query.message, "Надішли нове фото")
	else:
		current_field_value = event.__dict__[field]
		await callback_query.message.edit_text(f"Теперішнє значення поля <b>{EventModel.fields_name[field]}</b> - {current_field_value}\n"
									  + "Введіть нове значення: ", parse_mode=ParseMode.HTML)
	await state.update_data(field=field)
	await state.update_data(event_id=event_id)
	await state.set_state(EventUpdateState.NEW_DATA)


@router.message(EventUpdateState.NEW_DATA)
async def set_new_data(message: Message, state: FSMContext):
	state_data = await state.get_data()
	field = state_data["field"]
	event_id = state_data["event_id"]
	new_data = None
	
	if field == EventModel.PHOTO_ID:
		if message.photo:
			new_data = message.photo[-1].file_id
		else:
			await message.answer("Некорректні дані. Надішліть фото")
	elif field == EventModel.DATE:
		if is_valid_date(message.text):
			new_data = is_valid_date(message.text)
		else:
			await message.answer("Введіть дату у форматі dd.mm.yyyy, наприклад 20.11.2013")
	else:
		new_data = message.text
	
	if new_data is not None:
		if update_event(event_id, **{field: new_data}):
			await menu(message, f"Поле <b>{EventModel.fields_name[field]}</b> оновлено")
			await get_info_about_event(message, event_id=event_id)
		else:
			await state.clear()
			await message.answer("Даної події не знайдено")



@router.callback_query(F.data.startswith("select_"))
async def change_event_info(callback_query: CallbackQuery):
	event_id = callback_query.data[len("select_"):]
	buttons = []
	event = get_event_by_id(event_id)
	if event:
		for field in EventModel.fields_name.values():
			buttons.append(InlineKeyboardButton(text=field, callback_data=f"change_" + 
												f"{[key for key in EventModel.fields_name.keys() if EventModel.fields_name[key] == field][0]}_{event_id}"))
		buttons_chunked = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
		keyboard_markup = InlineKeyboardMarkup(inline_keyboard=buttons_chunked)
		await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
		await sent_change_menu(callback_query.message, "📝")
		event_info = get_info_text(event)
		await callback_query.message.answer(event_info, reply_markup=keyboard_markup, parse_mode=ParseMode.HTML)
	else:
		await callback_query.answer("Event not found")


async def select_event(message: Message):
	upcoming_events = get_events()
	if upcoming_events:
		events_message = f"Виберіть подію, яку хочете змінити:\n"
		buttons = []
		for event in upcoming_events:
			buttons.append([
				InlineKeyboardButton(text=f"{event.title} - {event.date}\n", callback_data=f"select_{event.id}")
			])
	else:
		events_message = "Поки немає запланованих подій 😔"
		try:
			await message.edit_text(events_message)
		except Exception as e:
			await message.answer(events_message)

	inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
	try:
		await message.edit_text(events_message, reply_markup=inline_keyboard)
	except Exception as e:
		await message.answer(events_message, reply_markup=inline_keyboard)




@router.callback_query(F.data.startswith("get_info_"))
async def get_info_handler(callback_query: CallbackQuery):
	event_id = int(callback_query.data[len("get_info_"):])
	await get_info_about_event(callback_query.message, event_id)



async def get_info_about_event(message: Message, event_id):
	event = get_event_by_id(event_id)

	info_text = get_info_text(event)

	buttons = [
		[
			InlineKeyboardButton(text=MenuButtons.EVENTS, callback_data="events_list")
		]
	]
	keyboard_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
	try:
		await message.edit_text(info_text, reply_markup=keyboard_markup, parse_mode=ParseMode.HTML)
	except Exception as e:
		await message.answer(info_text, reply_markup=keyboard_markup, parse_mode=ParseMode.HTML)


async def add_event(message: Message, state: FSMContext):
	message.answer("Реєстрація нової події")
	await send_event_registration_menu(message, text='Введіть назву події')
	await state.set_state(EventCreationState.TITLE)
	

@router.message(lambda message: message.text == ExitButtons.EXIT_EVENT_REGISTRATION)
async def end_registration(message: Message, state: FSMContext):
	await state.clear()

	await menu(message)


async def send_event_registration_menu(message: Message, text=''):
	custom_keyboard = [[KeyboardButton(text=ExitButtons.EXIT_EVENT_REGISTRATION)]]
	reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True)
	
	await message.answer(text, reply_markup=reply_markup)


@router.message(EventCreationState.TITLE)
async def set_title(message: Message, state: FSMContext):
	await state.update_data(title=message.text)
	await message.answer("Введіть опис події")
	await state.set_state(EventCreationState.DESCRIPTION)

@router.message(EventCreationState.DESCRIPTION)
async def set_description(message: Message, state: FSMContext):
	await state.update_data(description=message.text)
	await message.answer("Введіть посилання на подію")
	await state.set_state(EventCreationState.LINK)

@router.message(EventCreationState.LINK)
async def set_link(message: Message, state: FSMContext):
	await state.update_data(link=message.text)
	await message.answer("Надішліть фото події")
	await state.set_state(EventCreationState.PHOTO_ID)


@router.message(EventCreationState.PHOTO_ID)
async def set_photo(message: Message, state: FSMContext):
	if message.photo:
		await state.update_data(photo_id=message.photo[-1].file_id)
		await message.answer("Введіть статус події")
		await state.set_state(EventCreationState.STATUS)
	else:
		await message.answer("Некорректні данні. Надішліть фото")
		

@router.message(EventCreationState.STATUS)
async def set_status(message: Message, state: FSMContext):
	await state.update_data(status=message.text)
	await message.answer("Введіть дату події")
	await state.set_state(EventCreationState.DATE)
	

@router.message(EventCreationState.DATE)
async def set_date(message: Message, state: FSMContext):
	if is_valid_date(message.text):
		date = is_valid_date(message.text)
		await state.update_data(date=date)
		data = await state.get_data()
		save_event(data)
		await message.answer("Подія створена ✔️")
		await menu(message)
	else:
		await message.answer("Введіть дату у форматі dd.mm.yyyy, наприклад 20.11.2013")
		

menu_callback_function = {
	MenuButtons.EVENTS: events_list,
	MenuButtons.ADD_EVENTS: add_event,
	MenuButtons.CHANGE_EVENT: select_event,
}