import matplotlib.pyplot as plt
import pandas as pd


def calculate_statistics(data):
    """
    Рассчитывает и возвращает статистические индикаторы для цены закрытия.

    Args:
        data (pd.DataFrame): DataFrame с историческими данными акций.

    Returns:
        dict: Словарь со статистическими индикаторами.
    """
    statistics = {
        'mean': data['Close'].mean(),
        'std_dev': data['Close'].std(),
        'median': data['Close'].median(),
        'max': data['Close'].max(),
        'min': data['Close'].min(),
    }
    return statistics

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
    plt.style.use(style)
    plt.figure(figsize=(12, 12))

    # График цен
    plt.subplot(3, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')

    # Скользящая средняя (при наличии в данных)
    if 'Moving_Average' in data.columns:
        plt.plot(data.index, data['Moving_Average'], label='Moving Average', color='orange')

    # Добавляем стандартное отклонение
    mean = data['Close'].mean()
    std_dev = data['Close'].std()
    upper_bound = mean + std_dev
    lower_bound = mean - std_dev

    plt.fill_between(data.index, upper_bound, lower_bound, color='grey', alpha=0.3, label='±1 Standard Deviation')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # График RSI (при наличии в данных)
    if 'RSI' in data.columns:
        plt.subplot(3, 1, 2)
        plt.plot(data.index, data['RSI'], label='RSI', color='purple')
        plt.axhline(70, color='red', linestyle='--')
        plt.axhline(30, color='green', linestyle='--')
        plt.title(f"{ticker} Индекс относительной силы (RSI)")
        plt.xlabel("Дата")
        plt.ylabel("RSI")
        plt.legend()

    # График MACD (при наличии в данных)
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


def create_interactive_plot(data, ticker):
    import plotly.graph_objects as go

    # Вычисление среднего значения
    mean_close = data['Close'].mean()
    print(f"Среднее значение цены закрытия: {mean_close:.2f}")

    # Создание интерактивного графика
    fig = go.Figure()

    # Добавляем линию для цен закрытия
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Цена закрытия', line=dict(color='blue')))

    # Добавляем линию для среднего значения
    fig.add_trace(go.Scatter(x=data.index, y=[mean_close]*len(data), mode='lines', name='Среднее значение', line=dict(color='orange', dash='dash')))

    # Название графика
    fig.update_layout(title=f"{ticker} Цена акций",
                      xaxis_title='Дата',
                      yaxis_title='Цена',
                      legend_title='Легенда')

    # Показываем график
    fig.show()


