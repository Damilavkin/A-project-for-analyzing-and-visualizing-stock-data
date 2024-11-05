from datetime import datetime

import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")

    use_custom_dates = input("Хотите ли вы ввести конкретные даты? (да/нет): ").strip().lower()

    if use_custom_dates == 'да':
        start_date = input("Введите дату начала в формате YYYY-MM-DD: ")
        end_date = input("Введите дату окончания в формате YYYY-MM-DD: ")
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        stock_data = dd.fetch_stock_data(ticker, start_date, end_date)
        period = f"{start_date.date()} to {end_date.date()}"
    else:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        stock_data = dd.fetch_stock_data(ticker, period)

    # Добавляем скользящую среднюю и технические индикаторы
    stock_data = dd.add_moving_average(stock_data)
    stock_data = dd.add_technical_indicators(stock_data)

    # Расчет и вывод статистических индикаторов
    statistics = dplt.calculate_statistics(stock_data)
    print("Статистические индикаторы:")
    print(f"Средняя цена закрытия: {statistics['mean']:.2f}")
    print(f"Стандартное отклонение: {statistics['std_dev']:.2f}")
    print(f"Медиана: {statistics['median']:.2f}")
    print(f"Максимум: {statistics['max']:.2f}")
    print(f"Минимум: {statistics['min']:.2f}")

    # Строим график данных
    chosen_style = input("Выберите стиль графика (например, 'ggplot', 'seaborn-darkgrid', 'bmh'): ")
    dplt.create_and_save_plot(stock_data, ticker, period, style=chosen_style)

    # Экспортируем данные в CSV файл
    dd.export_data_to_csv(stock_data, "Output_to_csv")


if __name__ == "__main__":
    main()
