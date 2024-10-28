import pandas as pd
import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    """
    Извлекает исторические данные о ценах акций для указанного тикера.

    Args:
        ticker (str): Тикер акций (например, 'AAPL' для Apple).
        period (str): Период, за который будут извлечены данные (например, '1mo', '1y' и т.д.).

    Returns:
        pd.DataFrame: DataFrame с историческими данными о ценах акций.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    """
    Добавляет колонку со скользящей средней значений закрытия акций.

    Args:
        data (pd.DataFrame): DataFrame с историческими данными о ценах акций.
        window_size (int): Размер окна для расчета скользящей средней.

    Returns:
        pd.DataFrame: DataFrame с добавленной колонкой 'Moving_Average'.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия акций за указанный период.

    Args:
        data (pd.DataFrame): DataFrame с историческими данными о ценах акций.

    Returns:
        None
    """
    if 'Close' not in data.columns:
        print("Колонка 'Close' не найдена в данных.")
        return

    average_price = data['Close'].mean()
    print(f"Средняя цена закрытия акций за период: {average_price:.2f}")


def notify_if_strong_fluctuations(data, threshold):
    """
    Проверяет, есть ли сильные колебания цен на акции, и выводит уведомление.

    Args:
        data (pd.DataFrame): DataFrame с историческими данными о ценах акций.
        threshold (float): Пороговое значение для сильных колебаний в процентах.

    Returns:
        None
    """
    if 'Close' not in data.columns:
        print("Колонка 'Close' не найдена в данных.")
        return

    min_price = data['Close'].min()
    max_price = data['Close'].max()

    print(f'Минимальная цена: {min_price}')
    print(f'Максимальная цена: {max_price}')

    difference = max_price - min_price
    percentage_fluctuation = (difference / min_price) * 100

    if percentage_fluctuation > threshold:
        print(f'Уведомление: Разница превышает порог на {percentage_fluctuation - threshold:.2f}%')
    else:
        print(f'Разница не превышает порог: колебание составило {percentage_fluctuation:.2f}%')


def export_data_to_csv(data, filename):
    """
    Экспортирует данные DataFrame в CSV файл.

    Args:
        data (pd.DataFrame): Данные для экспорта.
        filename (str): Имя выходного файла для сохранения.

    Returns:
        None
    """
    try:
        data.to_csv(filename, index=False)
        print(f'Данные успешно экспортированы в {filename}.')
    except Exception as e:
        print(f'Ошибка при экспорте данных: {e}')


def calculate_rsi(data, window=14):
    """
    Вычисляет индекс относительной силы (RSI) для заданных данных.

    Args:
        data (pd.Series): Серия цен закрытия.
        window (int): Период для расчета RSI.

    Returns:
        pd.Series: Серия значений RSI.
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Вычисляет MACD для заданных данных.

    Args:
        data (pd.Series): Серия цен закрытия.
        short_window (int): Период для краткосрочной скользящей средней.
        long_window (int): Период для долгосрочной скользящей средней.
        signal_window (int): Период для сигнальной линии.

    Returns:
        pd.DataFrame: DataFrame с MACD и сигналом.
    """
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()

    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()

    return pd.DataFrame({'MACD': macd, 'Signal': signal})


def add_technical_indicators(stock_data):
    """
    Добавляет технические индикаторы (RSI и MACD) к данным акций.

    Args:
        stock_data (pd.DataFrame): DataFrame с историческими данными акций.

    Returns:
        pd.DataFrame: DataFrame с добавленными колонками 'RSI', 'MACD' и 'Signal'.
    """
    stock_data['RSI'] = calculate_rsi(stock_data['Close'])
    macd_df = calculate_macd(stock_data['Close'])
    stock_data = pd.concat([stock_data, macd_df], axis=1)

    return stock_data
