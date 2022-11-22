import pandas as pd
from random import randrange
import datetime


def random_date(start, l):
    current = start
    while l >= 0:
        curr = current + datetime.timedelta(minutes=randrange(30))
        yield curr
        l -= 1


def add_session(watch_df):
    watch_df = watch_df.rename_axis('id').reset_index()
    watch_df.sort_values(by=['customer_id', 'timestamp'], inplace=True)

    # В колонке ’divergence’ для каждого просмотра отдельного пользователя посчитаем
    # разницу между временем просмотра товара и временем просмотра предыдущего товара.
    # Если просмотр был первым для пользователя,
    # то значение в колонке ’divergence’ будет NaT, т.к. нет предыдущего значения.
    watch_df['divergence'] = watch_df.groupby('customer_id')['timestamp'].diff(1)

    # Создадим вспомогательный датафрейм ’sessions_begin_df’.
    # Этот датафрейм будет содержать просмотры, которые будут считаться первыми в сессиях.
    sessions_begin_df = watch_df[(watch_df['divergence'].isnull()) | (watch_df['divergence'] > '180 seconds')]
    sessions_begin_df['session_id'] = sessions_begin_df['id']

    # С помощью функции merge_asof объединим данные основного и вспомогательного датафреймов
    # по ближайшему соответствию ключей.
    watch_df.sort_values(by=['timestamp'], inplace=True)
    sessions_begin_df.sort_values(by=['timestamp'], inplace=True)

    watch_df = pd.merge_asof(watch_df, sessions_begin_df[['timestamp', 'customer_id', 'session_id']],
                             on='timestamp', by='customer_id')
    return watch_df.drop(columns=['divergence', 'id'], axis=1)


def main():
    start_date = datetime.datetime(2022, 11, 22, 13, 00)

    random_data = {"customer_id": pd.Series([1, 1, 2, 2, 3, 2, 1, 3, 4, 4, 3, 2, 4, 1, 4]),
                   "product_id": pd.Series([7, 8, 9, 6, 7, 8, 9, 6, 7, 8, 9, 6, 6, 6, 7]),
                   "timestamp": pd.Series([x for x in random_date(start_date, 14)])}

    watch_df = pd.DataFrame(random_data)

    watch_df = add_session(watch_df)

    print(watch_df)


if __name__ == '__main__':
    main()
