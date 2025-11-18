from typing import Dict, Optional, Callable, List
import asyncio

from aiogram.fsm.context import FSMContext


def make_update_progress(loop, state: FSMContext) -> Callable:
    """
    Возвращает функцию для отслеживания прогресса скачивания.

    Args:
        loop (_type_): цикл событий
        state (FSMContext): состояние В FSM для обновление прогресса
    """

    def update_progress(
        data_state: bool = None,
    ) -> True:
        data: Dict = asyncio.run_coroutine_threadsafe(state.get_data(), loop).result()
        asyncio.run_coroutine_threadsafe(
            state.update_data(counter_progress=data.get("counter_progress", 0) + 1),
            loop,
        ).result()

        # Дополнительная опция для необходимого состояния
        if data_state:
            asyncio.run_coroutine_threadsafe(
                state.update_data(data_state=data_state),
                loop,
            ).result()

        return True

    return update_progress


def async_make_update_progress(state: FSMContext):
    """
    Возвращает функцию для отслеживания асинхронного прогресса скачивания.

    Args:
        loop (_type_): цикл событий
        state (FSMContext): состояние В FSM для обновление прогресса
    """

    async def update_progress(data_state: int = None):
        data: Dict = await state.get_data()

        if data.get("cancel"):
            return False

        await state.update_data(counter_progress=data.get("counter_progress", 0) + 1)

        if data_state is not None:
            await state.update_data(data_state=data_state)

        return True

    return update_progress
