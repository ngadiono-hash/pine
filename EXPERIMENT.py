//@version=6
//@strategy_alert_message {{strategy.order.alert_message}}
strategy('TTM & MA', 'MANUAL 2.3', 
 initial_capital = 10000,
 default_qty_type = strategy.fixed, 
 default_qty_value = 1,
 margin_long = 0, 
 margin_short = 0, 
 max_bars_back = 500, 
 calc_on_order_fills = true, 
 process_orders_on_close = true, 
 calc_on_every_tick = true,
 overlay = true)
import jason5480/time_filters/5 as tif
_RED = color.red
_LIME = color.lime
_GREEN = color.teal
_BLUE = color.blue
_NAV = color.navy
_ORANGE = color.orange
_BLACK = color.black
_FUCH = color.fuchsia
_WHITE = color.white
_GRAY = color.new(color.gray, 50)
mp_font = font.family_monospace
mp_number = 1
mp_page = 20
timezone = 'Asia/Jakarta'




// 60 100 ohlc4 16 ohlc4
G0 = '══════════════  Appearance Settings  ════════════'
a_lineHMA = input.bool(true, 'MA', group = G0, inline = '1')
a_pip20 = input.bool(false, '20+', group = G0, inline = '1')
a_bgTrd = input.bool(true, 'W&L', group = G0, inline = '1')
a_candle = input.bool(true, 'MOM', group = G0, inline = '1')
a_label = input.bool(true, 'PIP', group = G0, inline = '1')
a_rvol = input.bool(false, 'VOL', group = G0, inline = '1')
a_maType = input.string('HMA', '', options = ['HMA', 'SMA', 'EMA'], group = G0, inline = '2')
G1 = '══════════════  Table Settings  ═════════════════'
smtable_on = input.bool(true, 'Sum', group = G1, inline = '1')
var_data = input.bool(false, 'Var', group = G1, inline = '1')
mptable_on = input.bool(true, 'Mon', group = G1, inline = '2')
tableSize = input.string('small', '', options = ['tiny', 'small', 'normal', 'auto'], group = G1, inline = '2')
mptable_pos = input.string('bottom-right', '', options = ['bottom-right', 'bottom-left', 'middle-right'], group = G1, inline = '2')
usefromDate = input.bool(false, title = 'From ', group = G1, inline = 'from')
fromDate = input.time(1640971800000, title = '', group = G1, inline = 'from')
usetoDate = input.bool(false, title = 'To ', group = G1, inline = 'to')
toDate = input.time(1736181000000, title = '', group = G1, inline = 'to')
dateFilter = tif.is_in_date_range(usefromDate, fromDate, usetoDate, toDate, timezone, timezone)
G2 = '══════════════  Buy Settings  ══════════════════'
// true close 0.5 1.2 false 25 5 HMA
EB = input.bool(true, 'ENABLE BUY', group = G2, inline = '1')
BATR = input.bool(false, 'ATR', group = G2, inline = '1')
BSRC = input.source(close, '', group = G2, inline = '2')
BSL = input.float(0.5, '', group = G2, inline = '2', step = 0.1, minval = 0.1, maxval = 1.0)
BMUL = input.float(1.2, '', group = G2, inline = '2', step = 0.1)
BDIS = input.float(25, '', group = G2, inline = '3', step = 5)
BLF = input.int(5, '', group = G2, inline = '3')
BFOR = input.string('HMA', '', options = ['NO', 'HMA', 'SMA', 'EMA', 'ATR'], group = G2, inline = '3')
// true hlcc4 0.5 1.3 false 30 5 HMA
EBT = input.bool(true, 'BUY CONTINUE', group = G2, inline = '1.1')
BTATR = input.bool(false, 'ATR', group = G2, inline = '1.1')
BTSRC = input.source(hlcc4, '', group = G2, inline = '2.1')
BTSL = input.float(0.5, '', group = G2, inline = '2.1', step = 0.1, minval = 0.1, maxval = 1.0)
BTMUL = input.float(1.3, '', group = G2, inline = '2.1', step = 0.1)
BTDIS = input.float(30, '', group = G2, inline = '3.1', step = 5)
BTLF = input.int(5, '', group = G2, inline = '3.1')
BTFOR = input.string('HMA', '', options = ['NO', 'HMA', 'SMA', 'EMA', 'ATR'], group = G2, inline = '3.1')
G3 = '══════════════  Sell Settings  ══════════════════'
// true ohlc4 0.5 1.3 false 15 3 HMA
ES = input.bool(true, 'ENABLE SELL', group = G3, inline = '1')
SATR = input.bool(false, 'ATR', group = G3, inline = '1')
SSRC = input.source(ohlc4, '', group = G3, inline = '2')
SSL = input.float(0.5, '', group = G3, inline = '2', step = 0.1, minval = 0.1, maxval = 1.0)
SMUL = input.float(1.3, '', group = G3, inline = '2', step = 0.1)
SDIS = input.float(15, '', group = G3, inline = '3', step = 5)
SLF = input.int(3, '', group = G3, inline = '3')
SFOR = input.string('HMA', '', options = ['NO', 'HMA', 'SMA', 'EMA', 'ATR'], group = G3, inline = '3')
// true ohlc4 0.5 1.3 false 30 3 HMA
EST = input.bool(true, 'SELL CONTINUE', group = G3, inline = '1.1')
STATR = input.bool(false, 'ATR', group = G3, inline = '1.1')
STSRC = input.source(ohlc4, '', group = G3, inline = '2.1')
STSL = input.float(0.5, '', group = G3, inline = '2.1', step = 0.1, minval = 0.1, maxval = 1.0)
STMUL = input.float(1.3, '', group = G3, inline = '2.1', step = 0.1)
STDIS = input.float(30, '', group = G3, inline = '3.1', step = 5)
STLF = input.int(3, '', group = G3, inline = '3.1')
STFOR = input.string('HMA', '', options = ['NO', 'HMA', 'SMA', 'EMA', 'ATR'], group = G3, inline = '3.1')
G4 = '══════════════  Parameter Settings  ═════════════'
LH1 = input.int(60, '', group = G4, inline = '1', step = 10) // MA fast length
LH2 = input.int(100, '', group = G4, inline = '1', step = 10) // MA fast length
Lsrc = input.source(ohlc4, '', group = G4, inline = '1') // source MA
TTM = input.int(16, '', group = G4, inline = '2')
Tsrc = input.source(ohlc4, '', group = G4, inline = '2')
// rvolTh = input.float(1, '', step = 0.1, group = G4, inline = '2') // Threshold Avg ATR
rvolTh = 1
// LV1 = input.int(14, '', group = G4, inline = '3') // ATR fast length
// LV2 = input.int(21, '', group = G4, inline = '3') // ATR slow length
LV1 = 14
LV2 = 21
// threshold = input.float(2, '', step = 0.1, group = G4, inline = '3') // Threshold Avg Candle
threshold = 2
atrFunc = ta.atr(LV1)
// MAIN BACKEND /////////////////////////////////
gmt_offset = 7 * 3600
newTradeClosed = strategy.closedtrades != strategy.closedtrades[1]
lastTradeDir = strategy.closedtrades.size(strategy.closedtrades - 1)
lastTradeLong = strategy.closedtrades.size(strategy.closedtrades - 1) > 0
lastTradeShort = strategy.closedtrades.size(strategy.closedtrades - 1) < 0
lastEntryPrice = strategy.closedtrades.entry_price(strategy.closedtrades - 1)
lastEntryTime = strategy.closedtrades.entry_time(strategy.closedtrades - 1) + gmt_offset
lastExitPrice = strategy.closedtrades.exit_price(strategy.closedtrades - 1)
lastExitTime = strategy.closedtrades.exit_time(strategy.closedtrades - 1) + gmt_offset
lastEntryBar = strategy.closedtrades.entry_bar_index(strategy.closedtrades - 1)
lastExitBarIn = strategy.closedtrades.exit_bar_index(strategy.closedtrades - 1)
lastExitBar = na(lastExitBarIn) ? 0 : lastExitBarIn
lastExitId = strategy.closedtrades.exit_id(strategy.closedtrades - 1)
orderUp = strategy.position_size > 0
orderDn = strategy.position_size < 0
noOrder = strategy.opentrades == 0
LOSE = strategy.losstrades != strategy.losstrades[1]
WIN = strategy.wintrades != strategy.wintrades[1]
ratioPercent(e, v) =>
    e * (v / 100)
numToPips(e) => // convert num to pips
    if syminfo.ticker == 'XAUUSD'
        e * 0.1
    else if str.endswith(syminfo.ticker, 'JPY')
        e * 0.01
    else if str.endswith(syminfo.ticker, 'USD') and syminfo.ticker != 'XAUUSD'
        e * 0.0001
    else
        na
pipsToStr(e) => // convert pips TV to TF
    if syminfo.ticker == 'XAUUSD'
        e * 10
    else if str.endswith(syminfo.ticker, 'JPY')
        e * 100
    else if str.endswith(syminfo.ticker, 'USD') and syminfo.ticker != 'XAUUSD'
        e * 10000
    else
        na
filters(s, l1, l2, m, isGreater) =>
    float v1 = switch m
        'HMA' => ta.hma(s, l1)
        'SMA' => ta.sma(s, l1)
        'EMA' => ta.ema(s, l1)
    float v2 = switch m
        'HMA' => ta.hma(s, l2)
        'SMA' => ta.sma(s, l2)
        'EMA' => ta.ema(s, l2)
    isGreater ? v1 >= v2 : v1 <= v2
generateMA(t,s,l) => switch t
    'SMA'  => ta.sma(s,l)
    'EMA'  => ta.ema(s,l)
    'HMA'  => ta.hma(s,l)
// Volatility .. Experiment
atr1 = ta.atr(LV1)
atr2 = ta.atr(LV2)
rvol = atr1 > atr2
// plot(atr1, title = 'atr1')
// plot(atr2 * rvolTh, title = 'atr2')
vol_color = rvol ? _LIME : _BLACK
plotshape(a_rvol ? true : false, 'Volatility', style = shape.circle, location = location.top, color = vol_color, size = size.tiny)
// Big Candle  ..Experiment
body_size = math.abs(close - open)
total_size = high - low
avg_body_size = ta.hma(body_size, LV1)
avg_total_size = ta.hma(total_size, LV1)
large_body = body_size > avg_body_size * threshold
large_total = total_size > avg_total_size * threshold
//color_large = large_body or large_total ? _BLUE : na
//plotcandle(open, high, low, close, color = color_large, title="Large Candlestick")
// MOMENTUM
mom = ta.linreg(Tsrc - math.avg(math.avg(ta.highest(high, TTM), ta.lowest(low, TTM)), ta.sma(Tsrc, TTM)), TTM, 0)
iff_1 = mom > nz(mom[1]) ? color.new(_GREEN, 20) : color.new(_RED, 60)
iff_2 = mom < nz(mom[1]) ? color.new(_RED, 20) : color.new(_GREEN, 60)
mom_color = mom > 0 ? iff_1 : iff_2
cross_up = ta.crossover(mom, nz(mom[1]))
cross_dn = ta.crossunder(mom, nz(mom[1]))
// FILTER MA FORMATION
fastMA = generateMA(a_maType, Lsrc, LH1)
slowMA = generateMA(a_maType, Lsrc, LH2)
fastMA_color = fastMA > fastMA[1] ? _GREEN : _RED
slowMA_color = slowMA > slowMA[1] ? _GREEN : _RED
spread = math.abs(fastMA - slowMA)
spread_prev = spread[5]
spread_trend = na(spread_prev) ? na : spread - spread_prev
isNarrowing = spread_trend < 0

b1_for = BFOR == 'NO' ? true : filters(Lsrc, LH1, LH2, BFOR, true)
s1_for = SFOR == 'NO' ? true : filters(Lsrc, LH1, LH2, SFOR, false)
b2_for = BTFOR == 'NO' ? true : filters(Lsrc, LH1, LH2, BTFOR, true)
s2_for = STFOR == 'NO' ? true : filters(Lsrc, LH1, LH2, STFOR, false)
barcolor(a_candle ? mom_color : na, title = 'Candle Color', editable = false)
// DECLARE VARIABLE TRADE
type Suitable
    bool long
    bool short
Suitable SG = Suitable.new(false, false)
type PendingOrder
    float en
    float sl
    float tp
    float act
    bool stat
    int bar
var PendingOrder PB = PendingOrder.new(na, na, na, na, false, 0)
var PendingOrder PS = PendingOrder.new(na, na, na, na, false, 0)
type PerTradeWL
    int wins
    int loss
var PerTradeWL B1 = PerTradeWL.new(0, 0)
var PerTradeWL B2 = PerTradeWL.new(0, 0)
var PerTradeWL S1 = PerTradeWL.new(0, 0)
var PerTradeWL S2 = PerTradeWL.new(0, 0)
type PerTradeStat
    int signalMonth
    int signalYear
    int tradeMonth
    int tradeYear
    int lossStreak
    int maxLossStreak
    int tradeLong
    int tradeLongWins
    int tradeShort
    int tradeShortWins
    int tradeBars
    int totalTrade
var PerTradeStat ST = PerTradeStat.new(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
// COUNT TRADE
type WinRate
    float total
    float long
    float short
var WinRate WR = WinRate.new(0, 0, 0)

// var int ST.tradeBars = 0
// var int ST.totalTrade = 0
var B_prep = false
var S_prep = false


// ENTRY
entryLong(e, a, d, m, x, i) =>
    ST.signalMonth += 1
    SG.long := true
    PB.stat := true
    PB.bar := bar_index
    PB.en := e + numToPips(d)
    PB.act := PB.en
    if a
        PB.sl := PB.en - atrFunc * m * x
        PB.tp := PB.en + atrFunc * m * x * 2
    else
        PB.sl := PB.en - ratioPercent(PB.en, m * x)
        PB.tp := PB.en + ratioPercent(PB.en, 1 * x)
    if close < PB.en
        strategy.entry(i, strategy.long, stop = PB.en, alert_message = 'Buy Stop Triggered')
    else
        strategy.entry(i, strategy.long, limit = PB.en, alert_message = 'Buy Limit Triggered')
entryShort(e, a, d, m, x, i) =>
    ST.signalMonth += 1
    SG.short := true
    PS.stat := true
    PS.bar := bar_index
    PS.en := e - numToPips(d)
    PS.act := PS.en
    if a
        PS.sl := PS.en + atrFunc * m * x
        PS.tp := PS.en - atrFunc * m * x * 2
    else
        PS.sl := PS.en + ratioPercent(PS.en, m * x)
        PS.tp := PS.en - ratioPercent(PS.en, 1 * x)
    if close > PS.en
        strategy.entry(i, strategy.short, stop = PS.en, alert_message = 'Sell Stop Triggered')
    else
        strategy.entry(i, strategy.short, limit = PS.en, alert_message = 'Sell Limit Triggered')

is_valid_bar(enable, filter) => enable and filter and barstate.isconfirmed and dateFilter and noOrder and bar_index > lastExitBar

B1_confirm = is_valid_bar(EB, b1_for) and cross_up and not PS.stat
S1_confirm = is_valid_bar(ES, s1_for) and cross_dn and not PB.stat
B2_confirm = lastTradeLong and dateFilter and EBT and WIN and b2_for
S2_confirm = lastTradeShort and dateFilter and EST and WIN and s2_for

if B1_confirm
    entryLong(BSRC, BATR, BDIS, BSL, BMUL, 'B1')
if S1_confirm
    entryShort(SSRC, SATR, SDIS, SSL, SMUL, 'S1')
   
if strategy.closedtrades.profit(strategy.closedtrades - 1) > 0
    if is_valid_bar(EBT, b2_for) and lastTradeLong and not PB.stat
        entryLong(BTSRC, BTATR, BTDIS, BTSL, BTMUL, 'B2')
    if is_valid_bar(EST, s2_for) and lastTradeShort and not PS.stat
        entryShort(STSRC, STATR, STDIS, STSL, STMUL, 'S2')

// CANCEL
cancelOrderB(f) =>
    if bar_index - PB.bar >= f
        if noOrder and PB.stat
            strategy.cancel_all()
            alert('Order Expired', alert.freq_once_per_bar)
            PB.stat := false
            PB.bar := na
            PB.act := na
cancelOrderS(f) =>
    if bar_index - PS.bar >= f
        if noOrder and PS.stat
            strategy.cancel_all()
            alert('Order Expired', alert.freq_once_per_bar)
            PS.stat := false
            PS.bar := na
            PS.act := na
cancelOrderB(BLF)
cancelOrderB(BTLF)
cancelOrderS(SLF)
cancelOrderS(STLF)
// EXIT
if orderDn
    PS.stat := false
if orderUp
    PB.stat := false
exitOrder(i, s, t) =>
    strategy.exit(i, from_entry = i, stop = s, limit = t, comment_loss = 'L', comment_profit = 'T', alert_profit = 'PROFIT', alert_loss = 'LOSE')
exitOrder('S1', PS.sl, PS.tp)
exitOrder('S2', PS.sl, PS.tp)
exitOrder('B1', PB.sl, PB.tp)
exitOrder('B2', PB.sl, PB.tp)

// PLOTING
plotshape(cross_up, 'Buy Signal 1', location = location.belowbar, color = SG.long ? _GREEN : _GRAY, style = shape.circle)
plotshape(cross_dn, 'Sell Signal 1', location = location.abovebar, color = SG.short ? _RED : _GRAY, style = shape.circle)
// LINE ORDER
plot(PB.stat ? PB.act : na, 'Order Line Buy', color = color.new(_FUCH, 0), style = plot.style_steplinebr, editable = false)
plot(a_pip20 and PB.stat ? PB.act + numToPips(20) : na, 'Line20', color = color.new(_BLACK, 60), style = plot.style_steplinebr, editable = false)
plot(a_pip20 and PB.stat ? PB.act - numToPips(20) : na, 'Line20', color = color.new(_BLACK, 60), style = plot.style_steplinebr, editable = false)
plot(PS.stat ? PS.act : na, 'Order Line Sell', color = color.new(_FUCH, 0), style = plot.style_steplinebr, editable = false)
plot(a_pip20 and PS.stat ? PS.act + numToPips(20) : na, 'Line20', color = color.new(_BLACK, 60), style = plot.style_steplinebr, editable = false)
plot(a_pip20 and PS.stat ? PS.act - numToPips(20) : na, 'Line20', color = color.new(_BLACK, 60), style = plot.style_steplinebr, editable = false)
// TP SL PENDING ORDER
plot(SG.short ? PS.sl : na, 'Sell Signal SL', color = _ORANGE, style = plot.style_steplinebr, linewidth = 1, editable = false)
plot(SG.short ? PS.tp : na, 'Sell Signal TP', color = _BLUE, style = plot.style_steplinebr, linewidth = 1, editable = false)
plot(SG.long ? PB.sl : na, 'Buy 1 Signal SL', color = _ORANGE, style = plot.style_steplinebr, linewidth = 1, editable = false)
plot(SG.long ? PB.tp : na, 'Buy 1 Signal TP', color = _BLUE, style = plot.style_steplinebr, linewidth = 1, editable = false)
// PLOT BUY ACTIVE
pb1 = plot(orderUp ? PB.en : na, 'Buy Entry Active', color = _BLACK, style = plot.style_steplinebr, editable = false)
pb2 = plot(orderUp ? PB.sl : na, 'Buy SL Active', color = _RED, style = plot.style_steplinebr, editable = false)
pb3 = plot(orderUp ? PB.tp : na, 'Buy TP Active', color = _GREEN, style = plot.style_steplinebr, editable = false)
// PLOT SELL ACTIVE
ps1 = plot(orderDn ? PS.en : na, 'Sell Entry Active', color = _BLACK, style = plot.style_steplinebr, editable = false)
ps2 = plot(orderDn ? PS.sl : na, 'Sell SL Active', color = _RED, style = plot.style_steplinebr, editable = false)
ps3 = plot(orderDn ? PS.tp : na, 'Sell TP Active', color = _GREEN, style = plot.style_steplinebr, editable = false)
// PLOT MOVING AVERAGE
plot(a_lineHMA ? fastMA : na, 'Hull MA 1', color = color.new(fastMA_color, 80), linewidth = 2, editable = false)
plot(a_lineHMA ? slowMA : na, 'Hull MA 2', color = color.new(slowMA_color, 60), linewidth = 3, editable = false)
bgcolor(a_bgTrd and LOSE ? color.new(_RED, 90) : na, title = 'BG Loss', editable = false)
bgcolor(a_bgTrd and WIN ? color.new(_GREEN, 90) : na, title = 'BG Win', editable = false)
fill(pb1, pb2, color = color.new(_RED, 80))
fill(pb1, pb3, color = color.new(_GREEN, 80))
fill(ps1, ps2, color = color.new(_RED, 80))
fill(ps1, ps3, color = color.new(_GREEN, 80))
// TABLE /////////////////////////////////////
table_pos(p) =>
    switch p
        'bottom-right' => position.bottom_right
        'bottom-left' => position.bottom_left
        'middle-right' => position.middle_right
table_size(e) =>
    switch e
        'auto'   => size.auto
        'normal' => size.normal 
        'small'  => size.small
        'tiny'   => size.tiny
mp_size = table_size(tableSize)
mp_pos = table_pos(mptable_pos)
percentage(a, b) => a / b * 100
pipsBG(e) =>
    e >= 200 ? color.new(_GREEN, 70) : e >= 0 and e < 200 ? color.new(_BLUE, 70) : e <= -0.1 and e > -100 ? color.new(_ORANGE, 70) : color.new(_RED, 70)
avgPipsBG(e) =>
    e >= 200 ? color.new(_GREEN, 60) : e >= 0 and e < 200 ? color.new(_ORANGE, 60) : color.new(_RED, 60)
netBG(e) =>
    e >= 2400 ? color.new(_GREEN, 60) : e >= 1000 and e < 2400 ? color.new(_BLUE, 60) : e <= 999.9 and e > 0 ? color.new(_ORANGE, 60) : color.new(_RED, 60)
totalBG(e) =>
    e >= 0 ? color.new(_GREEN, 60) : color.new(_RED, 60)
winrateBG(e) =>
    e >= 60 ? color.new(_GREEN, 60) : e >= 50 and e < 60 ? color.new(_BLUE, 60) : e <= 49.9 and e > 40 ? color.new(_ORANGE, 60) : color.new(_RED, 60)
pfBG(e) =>
    e >= 2.0 ? color.new(_GREEN, 60) : e >= 1.5 and e < 2.0 ? color.new(_BLUE, 60) : e <= 1.499 and e > 0 ? color.new(_ORANGE, 60) : color.new(_RED, 60)
f_src(e) =>
    switch e
        open  => 'open'
        high  => 'high'
        low   => 'low'
        close => 'close'
        ohlc4 => 'ohlc4'
        hlcc4 => 'hlcc4'
        hl2   => 'hl2'
        hlc3  => 'hlc3'
// DECLARE TABLE DATA VARIABLE
type StrategyReturn
    float pips
    float worst
    float best
    int timestamp
    int trade
    int signal
    int count
var array<StrategyReturn> M_Returns = array.new<StrategyReturn>(0)
var array<StrategyReturn> Y_Returns = array.new<StrategyReturn>(0)
var array<int> activeMonth = array.new_int(0)
var table sm_table = table(na)
var table mp_table = table(na)
current_month = month(time, timezone)
previous_month = month(time[1], timezone)
current_year = year(time, timezone)
previous_year = year(time[1], timezone)
new_month = current_month != previous_month
new_year = current_year != previous_year
bgcolor(a_label and new_month ? color.new(_BLUE, 60) : na, title = 'New Month', editable = false)
bgcolor(a_label and new_year ? color.new(_ORANGE, 60) : na, title = 'New Year', editable = false)
var bool firstEntryTime = false
if not firstEntryTime and not na(strategy.opentrades.entry_time(0))
    firstEntryTime := true
// PIPS STORE
var float onePips = 0
var float GProfit = 0 // GrossProfit
var float GLoss = 0 // GrossLoss
var float GPLong = 0 // GrossProfit Long
var float GLLong = 0 // GrossLoss Long
var float GPShort = 0 // GrossProfit Short
var float GLShort = 0 // GrossLoss Short
var float accMonthlyPips = 0
var float accYearlyPips = 0
var float netPips = 0
var float factorPips = 0
var float factorPercent = 0
var float peakEquity = strategy.equity
var float maxDrawdown = 0
var float drawdown = 0
// BEST & WORST PIPS
var float highestPips = 0
var float yearlyPipsHigh = 0
var float monthlyPipsHigh = 0
var float currentYearlyDDpips = 0
var float currentMonthlyDDpips = 0
var float yearlyMaxDDpips = 0
var float monthlyMaxDDpips = 0
var float bestAccYearlyPips = 0
var float bestAccMonthlyPips = 0

// CHECK BAR CLOSEDTRADES
if barstate.isconfirmed and newTradeClosed
    if not array.includes(activeMonth, current_month)
        array.push(activeMonth, current_month)
    // AVERAGE BAR CLOSEDTRADES
    lastTradeBars = lastEntryBar - lastExitBar
    ST.tradeBars += math.abs(lastTradeBars)
    ST.totalTrade += 1
    ST.tradeMonth += 1
    // PIPS CALCULATE
    if lastTradeLong // LONG
        onePips := lastExitPrice - lastEntryPrice
        ST.tradeLong += 1
        if onePips > 0 // WIN
            ST.lossStreak := 0
            ST.tradeLongWins += 1
            GProfit := GProfit + pipsToStr(onePips) // GP
            GPLong := GPLong + pipsToStr(onePips) // GPL
            B1.wins := lastExitId == 'B1' ? B1.wins + 1 : B1.wins + 0
            B2.wins := lastExitId == 'B2' ? B2.wins + 1 : B2.wins + 0
        else if onePips < 0 // LOSE
            ST.lossStreak += 1
            B1.loss := lastExitId == 'B1' ? B1.loss + 1 : B1.loss + 0
            B2.loss := lastExitId == 'B2' ? B2.loss + 1 : B2.loss + 0
            GLoss := GLoss + math.abs(pipsToStr(onePips)) // GL
            GLLong := GLLong + math.abs(pipsToStr(onePips)) // GLL
    else if lastTradeShort // SHORT
        onePips := lastEntryPrice - lastExitPrice
        ST.tradeShort += 1
        if onePips > 0 // WIN
            ST.lossStreak := 0
            ST.tradeShortWins += 1
            GProfit := GProfit + pipsToStr(onePips) // GP
            GPShort := GPShort + pipsToStr(onePips) // GPS
            S1.wins := lastExitId == 'S1' ? S1.wins + 1 : S1.wins + 0
            S2.wins := lastExitId == 'S2' ? S2.wins + 1 : S2.wins + 0
        else if onePips < 0// LOSE
            ST.lossStreak += 1
            S1.loss := lastExitId == 'S1' ? S1.loss + 1 : S1.loss + 0
            S2.loss := lastExitId == 'S2' ? S2.loss + 1 : S2.loss + 0            
            GLoss := GLoss + math.abs(pipsToStr(onePips)) // GL
            GLShort := GLShort + math.abs(pipsToStr(onePips)) // GLS
    netPips := GProfit - GLoss
    if highestPips < netPips 
        highestPips := netPips
    if ST.maxLossStreak < ST.lossStreak
        ST.maxLossStreak := ST.lossStreak
    
    // ACCUMULATION
    accMonthlyPips := pipsToStr(onePips) + accMonthlyPips[1]
    accYearlyPips := accYearlyPips + pipsToStr(onePips)
    // DRAWDOWN PIPS
    if accMonthlyPips > bestAccMonthlyPips
        bestAccMonthlyPips := accMonthlyPips
    if accMonthlyPips > monthlyPipsHigh
        monthlyPipsHigh := accMonthlyPips
    if accYearlyPips > bestAccYearlyPips
        bestAccYearlyPips := accYearlyPips
    if accYearlyPips > yearlyPipsHigh
        yearlyPipsHigh := accYearlyPips
    if accYearlyPips - yearlyPipsHigh < 0
        currentYearlyDDpips := accYearlyPips - yearlyPipsHigh
        if currentYearlyDDpips < yearlyMaxDDpips
            yearlyMaxDDpips := currentYearlyDDpips
    if accMonthlyPips - monthlyPipsHigh < 0
        currentMonthlyDDpips := accMonthlyPips - monthlyPipsHigh
        if currentMonthlyDDpips < monthlyMaxDDpips
            monthlyMaxDDpips := currentMonthlyDDpips
    // WINRATE
    WR.total := percentage(strategy.wintrades, strategy.closedtrades)
    WR.long := percentage(ST.tradeLongWins, ST.tradeLong)
    WR.short := percentage(ST.tradeShortWins, ST.tradeShort)        
    if a_label
        a = lastTradeDir > 0 ? '\nTotalLong : ' + str.tostring(ST.tradeLong) : '\nTotalShort : ' + str.tostring(ST.tradeShort)
        b = 'EQ: ' + str.tostring(netPips) + '\nTotalTrade : ' + str.tostring(strategy.closedtrades) + ' (' + str.tostring(WR.total, '#.##') + '%)' + a 
        c = onePips > 0 ? high + high * 0.01 : low - low * 0.01
        d = onePips > 0 ? label.style_label_down : label.style_label_up
        label.new(bar_index, c, tooltip = b, text = str.tostring(pipsToStr(onePips)), color = onePips > 0 ? _GREEN : _RED, textcolor = _WHITE, style = d)
    // DRAWDOWN EQUITY
    peakEquity := math.max(peakEquity, strategy.equity)
    drawdown := (peakEquity - strategy.equity) / peakEquity * 100
    maxDrawdown := math.max(maxDrawdown, drawdown)
// STORE & RESET MONTHLY DATA

if not barstate.isfirst and new_month and firstEntryTime or barstate.islastconfirmedhistory
    StrategyReturn mr = StrategyReturn.new(accMonthlyPips, monthlyMaxDDpips, bestAccMonthlyPips, time[1] + gmt_offset, ST.tradeMonth, ST.signalMonth)
    M_Returns.push(mr)
    ST.tradeYear += ST.tradeMonth
    ST.signalYear += ST.signalMonth
    ST.tradeMonth := 0
    ST.signalMonth := 0
    accMonthlyPips := 0
    monthlyMaxDDpips := 0
    bestAccMonthlyPips := 0
    monthlyPipsHigh := 0
    currentMonthlyDDpips := 0
// STORE & RESET YEARLY DATA
if not barstate.isfirst and new_year and firstEntryTime or barstate.islastconfirmedhistory
    StrategyReturn yr = StrategyReturn.new(accYearlyPips, yearlyMaxDDpips, bestAccYearlyPips, time[1] + gmt_offset, ST.tradeYear, ST.signalYear, array.size(activeMonth))
    Y_Returns.push(yr)
    ST.tradeYear := 0
    ST.signalYear := 0
    accYearlyPips := 0
    yearlyMaxDDpips := 0
    yearlyPipsHigh := 0
    currentYearlyDDpips := 0
    bestAccYearlyPips := 0
    array.clear(activeMonth)
// PAGE TABLE
if Y_Returns.size() < mp_page
    mp_page := Y_Returns.size()
startIndex = math.max(math.min(Y_Returns.size() - 1, Y_Returns.size() - 1 - (mp_page + 1) * mp_number), mp_page - 1)
endIndex = math.max(startIndex - mp_page, 0)
mp_page := endIndex <= mp_page ? endIndex : mp_page
// DRAW TABLE
if barstate.islastconfirmedhistory
    avgBarsInTrades = ST.tradeBars / ST.totalTrade
    start_time = strategy.closedtrades.entry_time(0) + gmt_offset
    entryFirst = firstEntryTime ? str.tostring(dayofmonth(start_time)) + '/' + str.tostring(month(start_time)) + '/' + str.tostring(year(start_time)) : 'NA'
    end_time = lastExitTime
    exitLast = str.tostring(dayofmonth(end_time)) + '/' + str.tostring(month(end_time)) + '/' + str.tostring(year(end_time))
    time_diff = end_time - start_time
    time_diff_years = time_diff / 31536000000.0
    final_value = strategy.netprofit + strategy.initial_capital
    cagr = (math.pow(final_value / strategy.initial_capital, 1 / time_diff_years) - 1) * 100
    percentReturn = strategy.netprofit / strategy.initial_capital * 100
    lastMonthRowIndex = startIndex < 5 ? 5 : startIndex
    factorPips := GProfit / GLoss
    factorPercent := strategy.grossprofit / strategy.grossloss

    mp_table := table.new(mp_pos, columns = 20, rows = Y_Returns.size() + 5, border_width = 1)
    // MONTHLY TABLE HEADER
    if mptable_on
        mp_table.cell(0,  0, 'Year', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(1,  0, 'Jan', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(2,  0, 'Feb', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(3,  0, 'Mar', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(4,  0, 'Apr', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(5,  0, 'May', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(6,  0, 'Jun', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(7,  0, 'Jul', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(8,  0, 'Aug', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(9,  0, 'Sep', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(10, 0, 'Oct', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(11, 0, 'Nov', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(12, 0, 'Dec', bgcolor = _GRAY, text_size = mp_size)
        mp_table.cell(13, 0, '++Pips', bgcolor = color.new(_NAV, 50), text_size = mp_size)
        mp_table.cell(14, 0, 'Best', bgcolor = color.new(_BLUE, 50), text_size = mp_size)
        mp_table.cell(15, 0, 'Worst', bgcolor = color.new(_RED, 50), text_size = mp_size)
        mp_table.cell(16, 0, '/Month', bgcolor = _GRAY, text_size = mp_size)

        // COLUMN TOTAL YEARLY
        for year_index = startIndex to Y_Returns.size() == 0 ? na : endIndex by 1
            StrategyReturn YR = Y_Returns.get(year_index)
            mp_table.cell(0, year_index + 1, str.tostring(year(YR.timestamp)), bgcolor = _GRAY, text_size = mp_size)
            // COLUMN TOTAL MONTHLY
            for month_index = 0 to M_Returns.size() - 1 by 1
                StrategyReturn MR = M_Returns.get(month_index)
                yearOfMonth = year(MR.timestamp)
                monthColumn = month(MR.timestamp)
                if yearOfMonth == year(YR.timestamp)
                    a = 'Worst: ' + str.tostring(MR.worst) + '\nBest: ' + str.tostring(MR.best) + '\nTrades: ' + str.tostring(MR.trade) + '/' + str.tostring(MR.signal)
                    mp_table.cell(monthColumn, year_index + 1, str.tostring(MR.pips), tooltip = a, bgcolor = pipsBG(MR.pips), text_size = mp_size, text_font_family = mp_font)
            mp_table.cell(13, year_index + 1, str.tostring(YR.pips, '#.##'), tooltip = str.tostring(YR.signal) + '/' + str.tostring(YR.trade), bgcolor = netBG(YR.pips), text_font_family = mp_font, text_size = mp_size)
            mp_table.cell(13, Y_Returns.size() + 1, str.tostring(netPips, '#.##'), bgcolor = _GRAY, text_font_family = mp_font, text_size = mp_size)
            mp_table.cell(14, year_index + 1, str.tostring(YR.best, '#.#'), bgcolor = color.new(_BLUE, 60), text_font_family = mp_font, text_size = mp_size)
            mp_table.cell(15, year_index + 1, str.tostring(YR.worst, '#.#'), tooltip = str.tostring(math.round(YR.worst / YR.pips * 100)) + ' %', bgcolor = color.new(_RED, 60), text_font_family = mp_font, text_size = mp_size)
            mp_table.cell(16, year_index + 1, str.tostring(YR.pips/YR.count, '#.#'), tooltip = str.tostring(YR.pips, '#.#') + '/' + str.tostring(YR.count), bgcolor = avgPipsBG(YR.pips/YR.count), text_font_family = mp_font, text_size = mp_size)
    // POPULATE ALL SETTINGS VARIABLE
    gap = strategy.closedtrades - ST.tradeLong - ST.tradeShort
    set_b = str.format('{0} {1} {2} {3} {4} {5} {6} {7}\n{8} {9} {10} {11} {12} {13} {14} {15}',
     str.tostring(EB), str.tostring(f_src(BSRC)), str.tostring(BSL), str.tostring(BMUL), str.tostring(BATR), str.tostring(BDIS), str.tostring(BLF), BFOR, str.tostring(EBT), str.tostring(f_src(BTSRC)), str.tostring(BTSL), str.tostring(BTMUL), str.tostring(BTATR), str.tostring(BTDIS), str.tostring(BTLF), BTFOR)
    set_s = str.format('\n{0} {1} {2} {3} {4} {5} {6} {7}\n{8} {9} {10} {11} {12} {13} {14} {15}',
     str.tostring(ES), str.tostring(f_src(SSRC)), str.tostring(SSL), str.tostring(BTMUL), str.tostring(SATR), str.tostring(SDIS), str.tostring(SLF), SFOR, str.tostring(EST), str.tostring(f_src(STSRC)), str.tostring(STSL), str.tostring(STMUL), str.tostring(STATR), str.tostring(STDIS), str.tostring(STLF), STFOR)
    set_p = str.format('\n{0} {1} {2} {3} {4}',
     str.tostring(LH1), str.tostring(LH2), str.tostring(f_src(Lsrc)), str.tostring(TTM), str.tostring(f_src(Tsrc)))
    sm_table := table.new(position.top_right, columns = 4, rows = 20, border_color = _GRAY, border_width = 1)
    sm_table.merge_cells(0, 9, 3, 9)
    // SUMMARY TABLE
    if smtable_on
        sm_table.cell(0,  0, 'Trade', bgcolor = gap > 0 ? _RED : na, tooltip = str.tostring(gap), text_size = mp_size)
        sm_table.cell(0,  1, 'Rate', text_size = mp_size)
        sm_table.cell(0,  2, 'PF Pips', text_size = mp_size)
        sm_table.cell(0,  3, str.tostring(highestPips), bgcolor = color.new(_GREEN, 70), tooltip = 'Highest Pips', text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(0,  4, 'Start', text_size = mp_size)
        sm_table.cell(0,  5, 'P/Trade', text_size = mp_size, tooltip = 'Avg pips per trade')
        sm_table.cell(0,  6, 'P/Month', text_size = mp_size, tooltip = 'Avg pips per month')
        sm_table.cell(0,  7, 'T/Month', text_size = mp_size, tooltip = 'Avg trade per month')
        sm_table.cell(0,  8, str.format('{0} : {1}', B1.wins, B1.loss), tooltip = 'B1', text_size = mp_size)
        if var_data 
            sm_table.cell(0,  9, str.tostring(set_b + set_s + set_p), bgcolor = color.new(_GRAY, 70), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  0, str.tostring(strategy.closedtrades), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  1, str.tostring(WR.total, '#.##') + '%', tooltip = str.format('{0} : {1}', strategy.wintrades, strategy.losstrades), bgcolor = winrateBG(WR.total), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  2, str.tostring(factorPips, '#.###'), bgcolor = pfBG(factorPips), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  3, str.tostring(netPips, '#.##'), bgcolor = netPips == highestPips ? color.new(_GREEN, 70) : color.new(_RED, 70), tooltip = str.tostring('Current Pips'), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  4, usefromDate ? entryFirst : na, text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  5, str.tostring(netPips/ST.totalTrade, '#.##'), tooltip = str.tostring(netPips) +'/'+ str.tostring(ST.totalTrade), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  6, str.tostring(netPips/M_Returns.size(), '#.##'), tooltip = str.tostring(netPips) +'/'+ str.tostring(M_Returns.size()), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  7, str.tostring(math.ceil(ST.totalTrade/M_Returns.size())), tooltip = str.tostring(ST.totalTrade) +'/'+ str.tostring(M_Returns.size()), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  8, str.format('{0} : {1}', B2.wins, B2.loss), tooltip = 'B2', text_size = mp_size)
        sm_table.cell(2,  0, str.tostring(ST.tradeLong), bgcolor = ST.tradeLong - B1.wins - B1.loss - B2.wins - B2.loss != 0 ? _RED : na, text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(2,  1, str.tostring(WR.long, '#.##') + '%', tooltip = str.format('{0} : {1}', ST.tradeLongWins, ST.tradeLong - ST.tradeLongWins), bgcolor = winrateBG(WR.long), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(2,  2, 'RR', text_size = mp_size)
        sm_table.cell(2,  3, '$'+str.tostring(final_value, '#.#'), text_font_family = mp_font, tooltip = 'EV : ' + str.tostring(strategy.initial_capital), text_size = mp_size)
        sm_table.cell(2,  4, 'End', text_size = mp_size)
        sm_table.cell(2,  5, 'CAGR', text_size = mp_size)
        sm_table.cell(2,  6, 'MaxLS', text_size = mp_size)
        sm_table.cell(2,  7, 'AvgBar', text_size = mp_size)
        sm_table.cell(2,  8, str.format('{0} : {1}', S1.wins, S1.loss), tooltip = 'S1', text_size = mp_size)
        sm_table.cell(3,  0, str.tostring(ST.tradeShort), bgcolor = ST.tradeShort - S1.wins - S1.loss - S2.wins - S2.loss != 0 ? _RED : na, text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  1, str.tostring(WR.short, '#.##') + '%', tooltip = str.format('{0} : {1}', ST.tradeShortWins, ST.tradeShort - ST.tradeShortWins), bgcolor = winrateBG(WR.short), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  2, str.tostring(factorPercent, '#.###'), bgcolor = pfBG(factorPercent), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  3, str.tostring(percentReturn, '#.##') + '%', text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  4, usetoDate ? exitLast : na, text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  5, str.tostring(cagr, '#.##') + '%', text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  6, str.tostring(ST.maxLossStreak), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  7, str.tostring(math.ceil(avgBarsInTrades)), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  8, str.format('{0} : {1}', S2.wins, S2.loss), tooltip = 'S2', text_size = mp_size)
// END 648 ///////////////////////////////////////////