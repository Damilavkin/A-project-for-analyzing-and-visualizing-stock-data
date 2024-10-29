from datetime import datetime

import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")

    # Изменение для выбора периода или указания конкретных дат
    use_custom_dates = input("Хотите ли вы ввести конкретные даты? (да/нет): ").strip().lower()

    if use_custom_dates == 'да':
        start_date = input("Введите дату начала в формате YYYY-MM-DD: ")
        end_date = input("Введите дату окончания в формате YYYY-MM-DD: ")
        # Преобразуем введенные строки в объекты datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Получаем данные акций за конкретный период
        stock_data = dd.fetch_stock_data(ticker, start_date, end_date)
        period = f"{start_date.date()} to {end_date.date()}"
    else:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        # Получаем данные о акциях за предустановленный период
        stock_data = dd.fetch_stock_data(ticker, period)

    threshold = float(input('Введите порог (в процентах) ==> '))

    # Добавляем скользящую среднюю и технические индикаторы к данным
    stock_data = dd.add_moving_average(stock_data)
    stock_data = dd.add_technical_indicators(stock_data)

    # Вычисляем и отображаем среднюю цену закрытия
    dd.calculate_and_display_average_price(stock_data)

    # Вычисляем колебания цен и выводим уведомление, если они сильные
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Строим график данных
    dplt.create_and_save_plot(stock_data, ticker,period)

    # Экспортируем данные в CSV файл
    dd.export_data_to_csv(stock_data, "Output_to_csv")

if __name__ == "__main__":
    main()
