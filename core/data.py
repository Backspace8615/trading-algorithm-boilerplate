import api.GraphData as api
import api.fetch as fetch
import core.order as order
import utils.variables as utils


def init_graph_data(account):
    config = fetch.get_settings()

    if config["mostRecent"] == False:
        df, ticker = fetch.get_df_selected_tf(
            config["ticker"], config["interval"], config["startDate"], config["endDate"]
        )
    else:
        df, ticker = fetch.get_df_recent(
            config["ticker"], config["interval"], config["timePeriod"]
        )

    ma_period = config["maPeriod"]
    rsi_period = config["rsiPeriod"]
    atr_period = config["atrPeriod"]
    std_dev_period = config["stdDevPeriod"]

    cutoff_period = max(ma_period, rsi_period, atr_period, std_dev_period)

    datetimes = df.index.to_series()
    closes = df.iloc[:, 0]
    highs = df.iloc[:, 1]
    lows = df.iloc[:, 2]
    opens = df.iloc[:, 3]
    rsi = []
    sma = []
    atr = []
    std_dev = []
    entries = []
    exits = []
    ongoing_balance = []

    data_obj = api.GraphData(
        account,
        ticker,
        datetimes,
        closes,
        highs,
        lows,
        opens,
        ma_period,
        rsi_period,
        atr_period,
        std_dev_period,
        cutoff_period,
        sma,
        rsi,
        atr,
        std_dev,
        entries,
        exits,
        ongoing_balance,
    )

    data_obj.calc_rsi()
    data_obj.calc_atr()
    data_obj.calc_sma()
    data_obj.calc_std_dev()

    datetimes = df.index.to_series()[cutoff_period:]
    data_obj.closes = df.iloc[:, 0][cutoff_period:]
    data_obj.highs = df.iloc[:, 1][cutoff_period:]
    data_obj.lows = df.iloc[:, 2][cutoff_period:]
    data_obj.opens = df.iloc[:, 3][cutoff_period:]

    valid = account.check_balance()
    if valid == False:
        print(
            "\nError: Base order value cannot be greater than starting amount. Please restart the server.\n"
        )
        quit()

    if config["addCsv"] == True:
        number = utils.generate_number(4)
        df.to_csv(f"{data_obj.ticker}_{number}.csv")

    data_obj.entries, data_obj.exits = order.indicators(account, data_obj)

    account.win_rate = (
        ((account.profitable_trades / account.completed_trades) * 100)
        if account.completed_trades > 0
        else -1
    )

    perc = ""
    if account.win_rate == -1:
        win_rate = "N/A"
    else:
        win_rate = round(account.win_rate, 2)
        perc = "%"

    profit_colour = "\033[0m"
    if account.profit > 0:
        profit_colour = "\033[32m"
    elif account.profit < 0:
        profit_colour = "\033[31m"
    reset_colour = "\033[0m"

    print(
        "\n=====================================================================================\n"
    )
    print(
        f"Made {(account.completed_trades)} trades | Win rate: {win_rate}{perc} | {profit_colour}Return: {(((account.balance_absolute / config['initialBalance']) - 1) * 100):.2f}%{reset_colour} | {profit_colour}Profit: ${account.profit:.2f}{reset_colour}\n"
    )

    return data_obj


def init_sim_data(account):
    config = fetch.get_settings()

    df, ticker = fetch.get_df_selected_tf(
        config["ticker"], config["interval"], config["startDate"], config["endDate"]
    )

    ma_period = config["maPeriod"]
    rsi_period = config["rsiPeriod"]
    atr_period = config["atrPeriod"]
    std_dev_period = config["stdDevPeriod"]

    cutoff_period = max(ma_period, rsi_period, atr_period, std_dev_period)

    datetimes = df.index.to_series()
    closes = df.iloc[:, 0]
    highs = df.iloc[:, 1]
    lows = df.iloc[:, 2]
    opens = df.iloc[:, 3]
    rsi = []
    sma = []
    atr = []
    std_dev = []
    entries = []
    exits = []
    ongoing_balance = []

    data_obj = api.GraphData(
        account,
        ticker,
        datetimes,
        closes,
        highs,
        lows,
        opens,
        ma_period,
        rsi_period,
        atr_period,
        std_dev_period,
        cutoff_period,
        sma,
        rsi,
        atr,
        std_dev,
        entries,
        exits,
        ongoing_balance,
    )

    data_obj.calc_rsi()
    data_obj.calc_atr()
    data_obj.calc_sma()
    data_obj.calc_std_dev()

    datetimes = df.index.to_series()[cutoff_period:]
    closes = df.iloc[cutoff_period:, 0]
    highs = df.iloc[cutoff_period:, 1]
    lows = df.iloc[cutoff_period:, 2]
    opens = df.iloc[cutoff_period:, 3]

    data_obj.entries, data_obj.exits = order.indicators(account, data_obj)

    account.profit = account.balance_absolute - config["initialBalance"]

    valid = account.check_balance()
    if valid == False:
        print(
            "\nError: Base order value cannot be greater than starting amount. Please restart the server.\n"
        )
        quit()

    return data_obj


def init_backtest_data(all_backtests, account, i):
    config = fetch.get_settings()

    df, ticker = fetch.get_df_selected_tf(
        all_backtests[i]["ticker"],
        config["interval"],
        config["startDate"],
        config["endDate"],
    )

    ma_period = all_backtests[i]["ma_period"]
    rsi_period = all_backtests[i]["rsi_period"]
    atr_period = all_backtests[i]["atr_period"]
    std_dev_period = all_backtests[i]["std_dev_period"]

    cutoff_period = max(ma_period, rsi_period, atr_period, std_dev_period)

    datetimes = df.index.to_series()
    closes = df.iloc[:, 0]
    highs = df.iloc[:, 1]
    lows = df.iloc[:, 2]
    opens = df.iloc[:, 3]
    rsi = []
    sma = []
    atr = []
    std_dev = []
    entries = []
    exits = []
    ongoing_balance = []

    data_obj = api.GraphData(
        account,
        ticker,
        datetimes,
        closes,
        highs,
        lows,
        opens,
        ma_period,
        rsi_period,
        atr_period,
        std_dev_period,
        cutoff_period,
        sma,
        rsi,
        atr,
        std_dev,
        entries,
        exits,
        ongoing_balance,
    )

    data_obj.calc_rsi()
    data_obj.calc_atr()
    data_obj.calc_sma()
    data_obj.calc_std_dev()

    datetimes = df.index.to_series()[cutoff_period:]
    closes = df.iloc[cutoff_period:, 0]
    highs = df.iloc[cutoff_period:, 1]
    lows = df.iloc[cutoff_period:, 2]
    opens = df.iloc[cutoff_period:, 3]

    data_obj.entries, data_obj.exits = order.indicators(account, data_obj)

    account.profit = account.balance_absolute - config["initialBalance"]

    valid = account.check_balance()
    if valid == False:
        print(
            "\nError: Base order value cannot be greater than starting amount. Please restart the server.\n"
        )
        quit()

    return data_obj
