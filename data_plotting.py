import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, filename=None):
    """
    Создает и сохраняет график цен акций с указанием цены закрытия и скользящей средней.

    Args:
        data (pd.DataFrame): DataFrame с историческими данными о ценах акций.
                             Должен содержать колонки 'Close' и 'Moving_Average'.
        ticker (str): Тикер акций, которые отображаются на графике.
        period (str): Период, за который были получены данные (например, '1mo').
        filename (str, optional): Имя файла для сохранения графика.
                                  Если не указано, будет автоматически сгенерировано.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))

    # Проверяем, есть ли информация о дате в данных
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        # Преобразуем колонку 'Date' в datetime, если это необходимо
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])

        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    # Настройка заголовка и меток графика
    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # Генерация имени файла, если оно не было задано
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    # Сохранение графика
    plt.savefig(filename)
    plt.close()  # Закрываем текущее окно графика после сохранения
    print(f"График сохранен как {filename}")
