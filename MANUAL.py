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
GS = 'Sell Settings'
GB = 'Buy Settings'
GP = 'Parameter Settings'
GA = 'Appearance'
GPT = 'Performance Table'
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
// APPEARANCE
pip20 = input.bool(false, '20+', group = GA, inline = '1')
bgTrd = input.bool(true, 'W&L', group = GA, inline = '1')
candle = input.bool(true, 'MOM', group = GA, inline = '1')
labPips = input.bool(true, 'PIP', group = GA, inline = '1')
load = input.bool(false, 'LOA', group = GA, inline = '1')
lineMA = input.bool(false, 'MA', group = GA, inline = '1')
a_rvol = input.bool(false, 'VOL', group = GA, inline = '1')
maType = input.string('HMA', '', options = ['HMA', 'SMA', 'EMA'], group = GA, inline = '2')
// TABLE
mptable_pos = input.string('Bottom Right', '', options = ['Bottom Right', 'Middle Right'], group = GA, inline = '2')
smtable_on = input.bool(true, 'Summary', group = GPT, inline = '1')
mptable_on = input.bool(true, 'Monthly', group = GPT, inline = '1')
allTableSize = input.string('normal', '', options = ['tiny', 'small', 'normal', 'auto'], group = GPT, inline = '1')
// DATE FILTER
timezone = 'Asia/Jakarta'
usefromDate = input.bool(false, title = 'From ', group = GPT, inline = 'from')
fromDate = input.time(1640971800000, title = '', group = GPT, inline = 'from')
usetoDate = input.bool(false, title = 'To ', group = GPT, inline = 'to')
toDate = input.time(1736181000000, title = '', group = GPT, inline = 'to')
dateFilter = tif.is_in_date_range(usefromDate, fromDate, usetoDate, toDate, timezone, timezone)
// INPUT BUY 
EB = input.bool(true, 'ENABLE BUY', group = GB, inline = '1')
B_BACK = input.bool(false, 'ENABLE BACK', group = GB, inline = '1')
BSRC = input.source(close, '', group = GB, inline = '2')
BSL = input.float(0.5, '', group = GB, inline = '2', step = 0.1, minval = 0.1, maxval = 1.0)
BATR = input.bool(false, 'ATR', group = GB, inline = '2')
BDIS = input.float(25, '', group = GB, inline = '3', step = 5)
BLF = input.int(4, '', group = GB, inline = '3')
BFOR = input.string('HMA', '', options = ['NO', 'HMA', 'SMA', 'EMA'], group = GB, inline = '3')
// INPUT TRAIL BUY
EBT = input.bool(true, 'BUY CONTINUE', group = GB, inline = '1.1')
BTSRC = input.source(hlcc4, '', group = GB, inline = '2.1')
BTSL = input.float(0.5, '', group = GB, inline = '2.1', step = 0.1, minval = 0.1, maxval = 1.0)
BTATR = input.bool(false, 'ATR', group = GB, inline = '2.1')
BTDIS = input.float(30, '', group = GB, inline = '3.1', step = 5)
BTLF = input.int(4, '', group = GB, inline = '3.1')
BTFOR = input.string('HMA', '', options = ['NO', 'HMA', 'SMA', 'EMA'], group = GB, inline = '3.1')
// INPUT SELL
ES = input.bool(true, 'ENABLE SELL', group = GS, inline = '1')
S_BACK = input.bool(false, 'ENABLE BACK', group = GS, inline = '1')
SSRC = input.source(ohlc4, '', group = GS, inline = '2')
SSL = input.float(0.5, '', group = GS, inline = '2', step = 0.1, minval = 0.1, maxval = 1.0)
SATR = input.bool(false, 'ATR', group = GS, inline = '2')
SDIS = input.float(15, '', group = GS, inline = '3', step = 5)
SLF = input.int(3, '', group = GS, inline = '3')
SFOR = input.string('HMA', '', options = ['NO', 'HMA', 'SMA', 'EMA'], group = GS, inline = '3')
// INPUT TRAIL SELL
EST = input.bool(true, 'SELL CONTINUE', group = GS, inline = '1.1')
STSRC = input.source(ohlc4, '', group = GS, inline = '2.1')
STSL = input.float(0.5, '', group = GS, inline = '2.1', step = 0.1, minval = 0.1, maxval = 1.0)
STATR = input.bool(false, 'ATR', group = GS, inline = '2.1')
STDIS = input.float(40, '', group = GS, inline = '3.1', step = 5)
STLF = input.int(3, '', group = GS, inline = '3.1')
STFOR = input.string('HMA', '', options = ['NO', 'HMA', 'SMA', 'EMA'], group = GS, inline = '3.1')
// INPUT PARAMETER [60, 100, 16, 1]
LH1 = input.int(60, '', group = GP, inline = 'hull', step = 10)
LH2 = input.int(100, '', group = GP, inline = 'hull', step = 10)
Lsrc = input.source(ohlc4, '', group = GP, inline = 'hull')
TTM = input.int(16, '', group = GP, inline = 'bb')
MULT = input.float(1, '', step = 0.1, group = GP, inline = 'bb')
Tsrc = input.source(ohlc4, '', group = GP, inline = 'bb')
LV1 = input.int(5, '', group = GP, inline = 'vol')
LV2 = input.int(14, '', group = GP, inline = 'vol')
rvolTh = input.float(1.0, '', group = GP, inline = 'vol')
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
lastExitBar = strategy.closedtrades.exit_bar_index(strategy.closedtrades - 1)
orderUp = strategy.position_size > 0
orderDn = strategy.position_size < 0
noOrder = strategy.opentrades == 0
LOSE = strategy.losstrades > strategy.losstrades[1]
WIN = strategy.wintrades > strategy.wintrades[1]
atrFunc = ta.atr(14)
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
f_cal(s, l1, l2, m, isGreater) =>
    float v1 = switch m
        'HMA' => ta.hma(s, l1)
        'SMA' => ta.sma(s, l1)
        'EMA' => ta.ema(s, l1)
    float v2 = switch m
        'HMA' => ta.hma(s, l2)
        'SMA' => ta.sma(s, l2)
        'EMA' => ta.ema(s, l2)
    isGreater ? v1 > v2 : v1 < v2

atr1 = ta.atr(LV1)
atr2 = ta.atr(LV2)
rvol = atr1 > (atr2 * rvolTh)
vol_color = rvol ? _LIME : _GRAY
drawMA(t,s,l) =>
    switch t
        'SMA'  => ta.sma(s,l)
        'EMA'  => ta.ema(s,l)
        'HMA'  => ta.hma(s,l)
// MOMENTUM
mom = ta.linreg(Tsrc - math.avg(math.avg(ta.highest(high, TTM), ta.lowest(low, TTM)), ta.sma(Tsrc, TTM)), TTM, 0)
iff_1 = mom > nz(mom[1]) ? color.new(_GREEN, 0) : color.new(_RED, 50)
iff_2 = mom < nz(mom[1]) ? color.new(_RED, 0) : color.new(_GREEN, 50)
mom_color = mom > 0 ? iff_1 : iff_2
cross_up = ta.crossover(mom, nz(mom[1]))
cross_dn = ta.crossunder(mom, nz(mom[1]))
// FILTER MA FORMATION
fastMA = drawMA(maType, Lsrc, LH1)
slowMA = drawMA(maType, Lsrc, LH2)
fastMA_color = fastMA > fastMA[1] ? _GREEN : _RED
slowMA_color = slowMA > slowMA[1] ? _GREEN : _RED
b1_for = BFOR == 'NO' ? true : f_cal(Lsrc, LH1, LH2, BFOR, true)
s1_for = SFOR == 'NO' ? true : f_cal(Lsrc, LH1, LH2, SFOR, false)
b2_for = BTFOR == 'NO' ? true : f_cal(Lsrc, LH1, LH2, BTFOR, true)
s2_for = STFOR == 'NO' ? true : f_cal(Lsrc, LH1, LH2, STFOR, false)
barcolor(candle ? mom_color : na, title = 'Candle Color', editable = false)
// DECLARE VARIABLE TRADE
type Suitable
    bool conf
    bool long
    bool short
    float atr
Suitable SG = Suitable.new(false, false, false, na)
type PendingOrder
    string id
    float en
    float sl
    float tp
    float act
    bool stat
    int bar
var PendingOrder PB = PendingOrder.new('', na, na, na, na, false, 0)
var PendingOrder PS = PendingOrder.new('', na, na, na, na, false, 0)
var int signalMonthly = 0
var int signalYearly = 0
var B2_prep = false
var S2_prep = false
B1_confirm = barstate.isconfirmed and dateFilter and EB and cross_up and b1_for and noOrder and not WIN and not LOSE
S1_confirm = barstate.isconfirmed and dateFilter and ES and cross_dn and s1_for and noOrder and not WIN and not LOSE

B2_confirm = lastTradeLong and dateFilter and EBT and WIN and b2_for
S2_confirm = lastTradeShort and dateFilter and EST and WIN and s2_for
// ENTRY
entryLong(e, a, d, m, i) =>
    SG.long := true
    PB.stat := true
    PB.bar := bar_index
    PB.en := e + numToPips(d)
    PB.act := PB.en
    if a
        PB.sl := PB.en - atrFunc * m * MULT
        PB.tp := PB.en + atrFunc * m * 1
    else
        PB.sl := PB.en - ratioPercent(PB.en, m * MULT)
        PB.tp := PB.en + ratioPercent(PB.en, 1 * MULT)
    if close < PB.en
        strategy.entry(i, strategy.long, stop = PB.en, alert_message = 'Buy Stop Triggered')
    else
        strategy.entry(i, strategy.long, limit = PB.en, alert_message = 'Buy Limit Triggered')
entryShort(e, a, d, m, i) =>
    SG.short := true
    PS.stat := true
    PS.bar := bar_index
    PS.en := e - numToPips(d)
    PS.act := PS.en
    if a
        PS.sl := PS.en + atrFunc * m * MULT
        PS.tp := PS.en - atrFunc * m * 1
    else
        PS.sl := PS.en + ratioPercent(PS.en, m * MULT)
        PS.tp := PS.en - ratioPercent(PS.en, 1 * MULT)
    if close > PS.en
        strategy.entry(i, strategy.short, stop = PS.en, alert_message = 'Sell Stop Triggered')
    else
        strategy.entry(i, strategy.short, limit = PS.en, alert_message = 'Sell Limit Triggered')
if B1_confirm
    entryLong(BSRC, BATR, BDIS, BSL, 'B1')
    signalMonthly := signalMonthly + 1
if B2_confirm
    B2_prep := true
if B2_prep and not WIN and noOrder
    entryLong(BTSRC, BTATR, BTDIS, BTSL, 'B2')
    B2_prep := false
    signalMonthly := signalMonthly + 1
if S1_confirm
    entryShort(SSRC, SATR, SDIS, SSL, 'S1')
    signalMonthly := signalMonthly + 1
if S2_confirm
    S2_prep := true
if S2_prep and not WIN and noOrder
    entryShort(STSRC, STATR, STDIS, STSL, 'S2')
    S2_prep := false
    signalMonthly := signalMonthly + 1
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
    strategy.exit(i, from_entry = i, stop = s, limit = t, comment_loss = '', comment_profit = '', alert_profit = 'PROFIT', alert_loss = 'LOSE')
exitOrder('S1', PS.sl, PS.tp)
exitOrder('S2', PS.sl, PS.tp)
exitOrder('B1', PB.sl, PB.tp)
exitOrder('B2', PB.sl, PB.tp)
// PLOTING
plot(SG.atr, 'atr', color = _BLACK, style = plot.style_steplinebr)
plotshape(SG.long, 'Buy Signal 1', location = location.belowbar, color = _GREEN, style = shape.triangleup, editable = false)
plotshape(SG.short, 'Sell Signal 1', location = location.abovebar, color = _RED, style = shape.triangledown, editable = false)
// LINE ORDER
plot(PB.stat ? PB.act : na, 'Order Line Buy', color = color.new(_FUCH, 0), style = plot.style_steplinebr, editable = false)
plot(pip20 and PB.stat ? PB.act + numToPips(20) : na, 'Line20', color = color.new(_BLACK, 60), style = plot.style_steplinebr, editable = false)
plot(pip20 and PB.stat ? PB.act - numToPips(20) : na, 'Line20', color = color.new(_BLACK, 60), style = plot.style_steplinebr, editable = false)
plot(PS.stat ? PS.act : na, 'Order Line Sell', color = color.new(_FUCH, 0), style = plot.style_steplinebr, editable = false)
plot(pip20 and PS.stat ? PS.act + numToPips(20) : na, 'Line20', color = color.new(_BLACK, 60), style = plot.style_steplinebr, editable = false)
plot(pip20 and PS.stat ? PS.act - numToPips(20) : na, 'Line20', color = color.new(_BLACK, 60), style = plot.style_steplinebr, editable = false)
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
// PLOT MOVING AVERAGE & VOL
plotshape(a_rvol ? true : false, 'Volatility', style = shape.square , location = location.top, color = vol_color, size = size.small)
plot(lineMA ? fastMA : na, 'Hull MA 1', color = color.new(fastMA_color, 80), linewidth = 2, editable = false)
plot(lineMA ? slowMA : na, 'Hull MA 2', color = color.new(slowMA_color, 60), linewidth = 3, editable = false)
bgcolor(bgTrd and LOSE ? color.new(_RED, 90) : na, title = 'BG Loss', editable = false)
bgcolor(bgTrd and WIN ? color.new(_GREEN, 90) : na, title = 'BG Win', editable = false)
fill(pb1, pb2, color = color.new(_RED, 80))
fill(pb1, pb3, color = color.new(_GREEN, 80))
fill(ps1, ps2, color = color.new(_RED, 80))
fill(ps1, ps3, color = color.new(_GREEN, 80))
// TABLE /////////////////////////////////////
var table sm_table = table(na)
var table mp_table = table(na)
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
table_pos(p) =>
    switch p
        'Bottom Right' => position.bottom_right
        'Middle Right' => position.middle_right
table_size(e) =>
    switch e
        'auto'   => size.auto
        'normal' => size.normal 
        'small'  => size.small
        'tiny'   => size.tiny
mp_size = table_size(allTableSize)
mp_pos = table_pos(mptable_pos)
// DECLARE TABLE DATA VARIABLE
type StrategyReturn
    float pips
    float worst
    float best
    int timestamp
    int trade
    int signal
    int count
var array<int> activeMonth = array.new_int(0)
var array<StrategyReturn> M_Returns = array.new<StrategyReturn>(0)
var array<StrategyReturn> Y_Returns = array.new<StrategyReturn>(0)
current_month = month(time, timezone)
previous_month = month(time[1], timezone)
current_year = year(time, timezone)
previous_year = year(time[1], timezone)
new_month = current_month != previous_month
new_year = current_year != previous_year
bgcolor(labPips and new_month ? color.new(_BLUE, 60) : na, title = 'New Month', editable = false)
bgcolor(labPips and new_year ? color.new(_ORANGE, 60) : na, title = 'New Year', editable = false)
var bool firstEntryTime = false
// PIPS STORE
var float onePips = 0
var float grossProfitPips = 0
var float grossLossPips = 0
var float grossProfitLongPips = 0
var float grossLossLongPips = 0
var float grossProfitShortPips = 0
var float grossLossShortPips = 0
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
var float currentYearlyDDpips = 0
var float yearlyMaxDDpips = 0
var float bestAccYearlyPips = 0
var float bestAccMonthlyPips = 0
var float currentMonthlyDDpips = 0
var float monthlyMaxDDpips = 0
var float monthlyPipsHigh = 0
// COUNT TRADE
var int tradeMonthly = 0
var int tradeYearly = 0
var int totalLongTrade = 0
var int totalLongTradeWins = 0
var int totalShortTrade = 0
var int totalShortTradeWins = 0
var float totalWinRate = 0
var float longWinRate = 0
var float shortWinRate = 0
var int totalBarsInTrades = 0
var int traded = 0
// CHECK BAR CLOSEDTRADES
if newTradeClosed
    if not array.includes(activeMonth, current_month)
        array.push(activeMonth, current_month)
    // AVERAGE BAR CLOSEDTRADES
    lastTradeBars = lastEntryBar - lastExitBar
    totalBarsInTrades := totalBarsInTrades + math.abs(lastTradeBars)
    traded := traded + 1
    // PIPS CALCULATE
    if lastTradeLong // LONG
        onePips := lastExitPrice - lastEntryPrice
        totalLongTrade := totalLongTrade + 1
        if onePips > 0 // WIN
            totalLongTradeWins := totalLongTradeWins + 1
            grossProfitPips := grossProfitPips + pipsToStr(onePips) // GP
            grossProfitLongPips := grossProfitLongPips + pipsToStr(onePips) // GPL
        else // LOSE
            grossLossPips := grossLossPips + math.abs(pipsToStr(onePips)) // GL
            grossLossLongPips := grossLossLongPips + math.abs(pipsToStr(onePips)) // GLL
    else if lastTradeShort // SHORT
        onePips := lastEntryPrice - lastExitPrice
        totalShortTrade := totalShortTrade + 1
        if onePips > 0 // WIN
            totalShortTradeWins := totalShortTradeWins + 1
            grossProfitPips := grossProfitPips + pipsToStr(onePips) // GP
            grossProfitShortPips := grossProfitShortPips + pipsToStr(onePips) // GPS
        else // LOSE
            grossLossPips := grossLossPips + math.abs(pipsToStr(onePips)) // GL
            grossLossShortPips := grossLossShortPips + math.abs(pipsToStr(onePips)) // GLS
    netPips := grossProfitPips - grossLossPips
    if highestPips < netPips 
        highestPips := netPips
    // ACCUMULATION
    tradeMonthly := tradeMonthly + 1
    accMonthlyPips := pipsToStr(onePips) + accMonthlyPips[1]
    accYearlyPips := accYearlyPips + pipsToStr(onePips)
    // DRAWDOWN PIPS
    // 
    if accMonthlyPips > bestAccMonthlyPips
        bestAccMonthlyPips := accMonthlyPips
    // 
    if accMonthlyPips > monthlyPipsHigh
        monthlyPipsHigh := accMonthlyPips
    // 
    if accYearlyPips > bestAccYearlyPips
        bestAccYearlyPips := accYearlyPips
    // 
    if accYearlyPips > yearlyPipsHigh
        yearlyPipsHigh := accYearlyPips
    // 
    if accYearlyPips - yearlyPipsHigh < 0
        currentYearlyDDpips := accYearlyPips - yearlyPipsHigh
        if currentYearlyDDpips < yearlyMaxDDpips
            yearlyMaxDDpips := currentYearlyDDpips
    //
    if accMonthlyPips - monthlyPipsHigh < 0
        currentMonthlyDDpips := accMonthlyPips - monthlyPipsHigh
        if currentMonthlyDDpips < monthlyMaxDDpips
            monthlyMaxDDpips := currentMonthlyDDpips
    // WINRATE
    totalWinRate := strategy.wintrades / strategy.closedtrades * 100
    longWinRate := nz(totalLongTradeWins / totalLongTrade * 100)
    shortWinRate := nz(totalShortTradeWins / totalShortTrade * 100)        
    if labPips
        a = lastTradeDir > 0 ? '\nTotalLong : ' + str.tostring(totalLongTrade) : '\nTotalShort : ' + str.tostring(totalShortTrade)
        b = 'EQ: ' + str.tostring(netPips) + '\nTotalTrade : ' + str.tostring(strategy.closedtrades) + ' (' + str.tostring(totalWinRate, '#.##') + '%)' + a 
        c = onePips > 0 ? high + high * 0.01 : low - low * 0.01
        d = onePips > 0 ? label.style_label_down : label.style_label_up
        label.new(bar_index, c, tooltip = b, text = str.tostring(pipsToStr(onePips)), color = onePips > 0 ? _GREEN : _RED, textcolor = _WHITE, style = d)
    // DRAWDOWN EQUITY
    peakEquity := math.max(peakEquity, strategy.equity)
    drawdown := (peakEquity - strategy.equity) / peakEquity * 100
    maxDrawdown := math.max(maxDrawdown, drawdown)
// STORE & RESET MONTHLY DATA
var count_month = 0
if not firstEntryTime and not na(strategy.opentrades.entry_time(0))
    firstEntryTime := true
if not barstate.isfirst and new_month and firstEntryTime or barstate.islastconfirmedhistory
    StrategyReturn mr = StrategyReturn.new(accMonthlyPips, monthlyMaxDDpips, bestAccMonthlyPips, time[1] + gmt_offset, tradeMonthly, signalMonthly)
    M_Returns.push(mr)
    tradeYearly += tradeMonthly
    signalYearly += signalMonthly
    tradeMonthly := 0
    signalMonthly := 0
    accMonthlyPips := 0
    monthlyMaxDDpips := 0
    bestAccMonthlyPips := 0
    monthlyPipsHigh := 0
    currentMonthlyDDpips := 0
// STORE & RESET YEARLY DATA
if not barstate.isfirst and new_year and firstEntryTime or barstate.islastconfirmedhistory
    StrategyReturn yr = StrategyReturn.new(accYearlyPips, yearlyMaxDDpips, bestAccYearlyPips, time[1] + gmt_offset, tradeYearly, signalYearly, array.size(activeMonth))
    Y_Returns.push(yr)
    tradeYearly := 0
    signalYearly := 0
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
    avgBarsInTrades = totalBarsInTrades / traded + 1
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
    factorPips := grossProfitPips / grossLossPips
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
            mp_table.cell(13, Y_Returns.size() + 1, str.tostring(netPips), bgcolor = _GRAY, text_font_family = mp_font, text_size = mp_size)
            mp_table.cell(14, year_index + 1, str.tostring(YR.best, '#.#'), bgcolor = color.new(_BLUE, 60), text_font_family = mp_font, text_size = mp_size)
            mp_table.cell(15, year_index + 1, str.tostring(YR.worst, '#.#'), tooltip = str.tostring(math.round(YR.worst / YR.pips * 100)) + ' %', bgcolor = color.new(_RED, 60), text_font_family = mp_font, text_size = mp_size)
            mp_table.cell(16, year_index + 1, str.tostring(YR.pips/YR.count, '#.#'), tooltip = str.tostring(YR.pips, '#.#') + '/' + str.tostring(YR.count), bgcolor = avgPipsBG(YR.pips/YR.count), text_font_family = mp_font, text_size = mp_size)
    // POPULATE ALL SETTINGS VARIABLE
    set_b = str.format('{0} {1} {2} {3} {4} {5} {6}\n{7} {8} {9} {10} {11} {12} {13}', 
     str.tostring(EB), str.tostring(f_src(BSRC)), str.tostring(BSL), str.tostring(BATR), str.tostring(BDIS), str.tostring(BLF), BFOR, str.tostring(EBT), str.tostring(f_src(BTSRC)), str.tostring(BTSL), str.tostring(BTATR), str.tostring(BTDIS), str.tostring(BTLF), BTFOR)
    set_s = str.format('\n{0} {1} {2} {3} {4} {5} {6}\n{7} {8} {9} {10} {11} {12} {13}',
     str.tostring(ES), str.tostring(f_src(SSRC)), str.tostring(SSL), str.tostring(SATR), str.tostring(SDIS), str.tostring(SLF), SFOR, str.tostring(EST), str.tostring(f_src(STSRC)), str.tostring(STSL), str.tostring(STATR), str.tostring(STDIS), str.tostring(STLF), STFOR)
    set_p = str.format('\n{0} {1} {2} {3} {4} {5}',
     str.tostring(LH1), str.tostring(LH2), str.tostring(f_src(Lsrc)), str.tostring(TTM), str.tostring(MULT), str.tostring(f_src(Tsrc)))
    sm_table := table.new(position.top_right, columns = 4, rows = 20, border_color = _GRAY, border_width = 1)
    sm_table.merge_cells(0, 8, 3, 8)
    // SUMMARY TABLE
    if smtable_on
        sm_table.cell(0,  0, 'Trade', text_size = mp_size)
        sm_table.cell(0,  1, 'Rate', text_size = mp_size)
        sm_table.cell(0,  2, 'PF Pips', text_size = mp_size)
        sm_table.cell(0,  3, str.tostring(highestPips), bgcolor = color.new(_GREEN, 70), tooltip = 'Highest Pips', text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(0,  4, 'Start', text_size = mp_size)
        sm_table.cell(0,  5, 'P/Trade', text_size = mp_size, tooltip = 'Avg pips per trade')
        sm_table.cell(0,  6, 'P/Month', text_size = mp_size, tooltip = 'Avg pips per month')
        sm_table.cell(0,  7, 'T/Month', text_size = mp_size, tooltip = 'Avg trade per month')
        sm_table.cell(0,  8, str.tostring(set_b + set_s + set_p), bgcolor = color.new(_GRAY, 70), text_font_family = mp_font, text_size = mp_size)

        sm_table.cell(1,  0, str.tostring(strategy.closedtrades), tooltip = str.tostring(strategy.closedtrades - totalLongTrade - totalShortTrade), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  1, str.tostring(totalWinRate, '#.##') + '%', bgcolor = winrateBG(totalWinRate), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  2, str.tostring(factorPips, '#.###'), bgcolor = pfBG(factorPips), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  3, str.tostring(netPips), bgcolor = netPips == highestPips ? color.new(_GREEN, 70) : color.new(_RED, 70), tooltip = str.tostring('Current Pips'), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  4, usefromDate ? entryFirst : na, text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  5, str.tostring(netPips/strategy.closedtrades, '#.##'), tooltip = str.tostring(netPips) +'/'+ str.tostring(strategy.closedtrades), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  6, str.tostring(netPips/M_Returns.size(), '#.##'), tooltip = str.tostring(netPips) +'/'+ str.tostring(M_Returns.size()), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(1,  7, str.tostring(math.ceil(strategy.closedtrades/M_Returns.size())), tooltip = str.tostring(strategy.closedtrades) +'/'+ str.tostring(M_Returns.size()), text_font_family = mp_font, text_size = mp_size)

        sm_table.cell(2,  0, str.tostring(totalLongTrade), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(2,  1, str.tostring(longWinRate, '#.##') + '%', bgcolor = winrateBG(longWinRate), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(2,  2, 'PF %', text_size = mp_size)
        sm_table.cell(2,  3, '$'+str.tostring(final_value, '#.#'), text_font_family = mp_font, tooltip = 'EV : ' + str.tostring(strategy.initial_capital), text_size = mp_size)
        sm_table.cell(2,  4, 'End', text_size = mp_size)
        sm_table.cell(2,  5, 'CAGR', text_size = mp_size)
        sm_table.cell(2,  6, 'MaxDD', text_size = mp_size)
        sm_table.cell(2,  7, 'AvgBar', text_size = mp_size)

        sm_table.cell(3,  0, str.tostring(totalShortTrade), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  1, str.tostring(shortWinRate, '#.##') + '%', bgcolor = winrateBG(shortWinRate), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  2, str.tostring(factorPercent, '#.###'), bgcolor = pfBG(factorPercent), text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  3, str.tostring(percentReturn, '#.##') + '%', text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  4, usetoDate ? exitLast : na, text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  5, str.tostring(cagr, '#.##') + '%', text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  6, str.tostring(maxDrawdown, '#.##') + '%', text_font_family = mp_font, text_size = mp_size)
        sm_table.cell(3,  7, str.tostring(math.ceil(avgBarsInTrades)), text_font_family = mp_font, text_size = mp_size)
// END 620 ///////////////////////////////////////////