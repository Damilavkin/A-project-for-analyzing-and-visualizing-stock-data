import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    """
    Создает и сохраняет график цен акций с указанием цены закрытия,
    скользящей средней, RSI и MACD.

    Args:
        data (pd.DataFrame): DataFrame с историческими данными акций.
        ticker (str): Тикер акций для отображения на графике.
        period (str): Период, за который получены данные.
        filename (str, optional): Имя файла для сохранения графика.
        style (str): Стиль графика (по умолчанию 'default').

    Returns:
        None
    """
    # Устанавливаем стиль графика
    plt.style.use(style)
    plt.figure(figsize=(12, 12))

    # График цен
    plt.subplot(3, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')

    if 'Moving_Average' in data.columns:
        plt.plot(data.index, data['Moving_Average'], label='Moving Average', color='orange')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # График RSI
    if 'RSI' in data.columns:
        plt.subplot(3, 1, 2)
        plt.plot(data.index, data['RSI'], label='RSI', color='purple')
        plt.axhline(70, color='red', linestyle='--')
        plt.axhline(30, color='green', linestyle='--')
        plt.title(f"{ticker} Индекс относительной силы (RSI)")
        plt.xlabel("Дата")
        plt.ylabel("RSI")
        plt.legend()

    # График MACD
    if 'MACD' in data.columns and 'Signal' in data.columns:
        plt.subplot(3, 1, 3)
        plt.plot(data.index, data['MACD'], label='MACD', color='blue')
        plt.plot(data.index, data['Signal'], label='Signal', color='orange')
        plt.title(f"{ticker} MACD")
        plt.xlabel("Дата")
        plt.ylabel("MACD")
        plt.legend()

    # Генерация имени файла, если оно не было задано
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    # Сохранение графика
    plt.savefig(filename)
    plt.close()
    print(f"График сохранен как {filename}")