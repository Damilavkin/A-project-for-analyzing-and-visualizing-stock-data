import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    if 'Close' not in data.columns:
        print("Колонка 'Close' не найдена в данных.")
        return

    average_price = data['Close'].mean()
    print(f"Средняя цена закрытия акций за период: {average_price:.2f}")


def notify_if_strong_fluctuations(data, threshold):
    if 'Close' not in data.columns:
        print("Колонка 'Close' не найдена в данных.")
        return
    min_price = data['Close'].min()
    max_price = data['Close'].max()

    print(f'Минимальная цена {min_price}')
    print(f'Максимальная цена {max_price}')

    difference = max_price - min_price
    percentage_fluctuation = (difference / min_price) * 100

    if percentage_fluctuation > threshold:
        print(f'Уведомление: Разница превышает порог на {percentage_fluctuation - threshold}%')
    else:
        print(f'Разница не превышает порог: колебание составило {percentage_fluctuation}%')


def export_data_to_csv(data, filename):
    try:
        data.to_csv(filename, index=False)
        print(f'Данные успешно экспортированы в {filename}.')
    except Exception as e:
        print(f'Ошибка при экспорте данных: {e}')