//@version=5
strategy(title = 'Squeeze Momentum Strategy with TP & SL',
         shorttitle = 'SQZ Strategy',
         overlay = true,
         pyramiding = 0,
         default_qty_type = strategy.percent_of_equity,
         default_qty_value = 100,
         initial_capital = 10000,
         commission_type=strategy.commission.percent, 
         commission_value=0.0,
         process_orders_on_close=false,
         use_bar_magnifier=false)

import jason5480/time_filters/5 as tif

gp0 = "Backtesting Settings"
gp1 = "Squeeze Momentum Settings"
gp2 = "Strategy Settings"
gp3 = "Hull Settings"

type1 = "1. Momentum"
type2 = "2. Momentum and Zero Point"
type3 = "3. Zero Point"

usefromDate = input.bool(true, title = 'From', inline = 'From Date', group = gp0)
fromDate = input.time(defval = timestamp('1 Jan 2022 00:00'), title = '', inline = 'From Date', group = gp0)
usetoDate = input.bool(false, title = 'To ', inline = 'To Date', group = gp0)
toDate = input.time(defval = timestamp('31 Aug 2024 00:00'), title = '', inline = 'To Date', group = gp0)
bool dateFilterApproval = tif.is_in_date_range(usefromDate, fromDate, usetoDate, toDate)

strategy_logic = input.string(type1, "Switch Strategy", options = [type1, type2, type3], group = gp2)

longDealsEnabled = input.bool(true, title = 'Enable Longs', group = gp2)
long_stoploss_value = input.float(0.5, title='  SL %', minval=0.01, step=0.01,group=gp2, inline='2')
long_takeprofit_value = input.float(1, title='  TP %', minval=0.01, step=0.01,group=gp2, inline='2')

shortDealsEnabled = input.bool(true, title = 'Enable Shorts', group = gp2)
short_stoploss_value = input.float(0.5, title='  SL %', minval=0.01, step=0.01,group=gp2, inline='3')//100
short_takeprofit_value = input.float(1, title='  TP %', minval=0.01,step=0.01, group=gp2, inline='3')

// Condition of SL-TP Percentage
long_stoploss_percentage = close * (long_stoploss_value / 100) / syminfo    .mintick
long_takeprofit_percentage = close * (long_takeprofit_value / 100) / syminfo.mintick
short_stoploss_percentage = close * (short_stoploss_value / 100) / syminfo.mintick
short_takeprofit_percentage = close * (short_takeprofit_value / 100) / syminfo.mintick

// Condition of SL-TP Levels
long_stoploss_price = strategy.position_avg_price * (1 - long_stoploss_value / 100)
long_takeprofit_price = strategy.position_avg_price * (1 + long_takeprofit_value / 100)
short_stoploss_price = strategy.position_avg_price * (1 + short_stoploss_value / 100)
short_takeprofit_price = strategy.position_avg_price * (1 - short_takeprofit_value / 100)

length = input(20, title='BB Length', group=gp1)
src = input(ohlc4, title="Source BB", group=gp1)
mult = input(2.0, title='BB MultFactor', group = gp1)
lengthKC = input(20, title='KC Length', group = gp1)
mult_kc = input(1.5, title='KC MultFactor', group = gp1)
squeeze_filter = input.bool(false, "Entry only when Squeeze On", group = gp1)

// Calculate BB
ma_1 = ta.sma(src, length)
ma_2 = ta.sma(src, lengthKC)
range_ma = ta.sma(high - low, lengthKC)

dev = mult * ta.stdev(src, length)

upper_bb = ma_1 + dev
lower_bb = ma_1 - dev

upper_kc = ma_2 + range_ma * mult_kc
lower_kc = ma_2 - range_ma * mult_kc

sqz_on = lower_bb > lower_kc and upper_bb < upper_kc
sqz_off = lower_bb < lower_kc and upper_bb > upper_kc
no_sqz = sqz_on == false and sqz_off == false
sqz_filter = squeeze_filter ? sqz_off : true
val = ta.linreg(src - math.avg(math.avg(ta.highest(hl2, lengthKC), ta.lowest(low, lengthKC)), ta.sma(hl2, lengthKC)), lengthKC, 0)

// HULL FILTER
length1 = input.int(50, title="HMA 1", group=gp3)
length2 = input.int(100, title="HMA 2", group=gp3)
filterHMAcolor = input.bool(false, title="Filter with hull color?")
filterHMApos = input.bool(true, title="Filter with hull position?")
color_up = color.teal
color_down = color.red

hmaFunc(src, length) => ta.hma(src, length)
hma1 = hmaFunc(close, length1)
hma2 = hmaFunc(close, length2)
color1 = hma1 > hma1[2] ? color_up : color_down
color2 = hma2 > hma2[2] ? color_up : color_down
plot(hma1, title="HMA 1", color=color1, linewidth=2)
plot(hma2, title="HMA 2", color=color2, linewidth=3)

HMAcolor_up = filterHMAcolor ? color1 == color_up : true
HMAcolor_down = filterHMAcolor ? color1 == color_down : true
HMAup = filterHMApos ? hma1 > hma2 : true
HMAdown = filterHMApos ? hma1 < hma2 : true
//
long_default = ta.crossover(val,nz(val[1]))
short_default = ta.crossunder(val,nz(val[1]))

longCondition = switch strategy_logic
    type1 => ta.crossover(val,nz(val[1])) and sqz_filter
    type2 =>
        ta.crossover(val,nz(val[1])) and val<0 and sqz_filter
    type3 => ta.crossover(val,nz(val[1])) and val<0 and sqz_filter
    
shortCondition = switch strategy_logic
    type1 => ta.crossunder(val,nz(val[1])) and sqz_filter
    type2 => ta.crossunder(val,nz(val[1])) and val>0 and sqz_filter
    type3 => ta.crossunder(val,nz(val[1])) and val>0 and sqz_filter


// Entries Condition
if longCondition and longDealsEnabled and dateFilterApproval and HMAcolor_up and HMAup
    strategy.entry('Long', strategy.long)
    strategy.exit('Long Exit', from_entry='Long', loss=long_stoploss_percentage, profit=long_takeprofit_percentage, comment_loss="SL", comment_profit="TP")

if shortCondition and shortDealsEnabled and dateFilterApproval and HMAcolor_down and HMAdown
    strategy.entry('Short', strategy.short)
    strategy.exit('Short Exit', from_entry='Short', loss=short_stoploss_percentage, profit=short_takeprofit_percentage, comment_loss="SL", comment_profit="TP")


// Entries Confirmed
plot(strategy.position_size>0 ? long_stoploss_price : na, color=color.new(#ff0000, 0), style=plot.style_linebr, linewidth=1, title='Long SL Level')
plot(strategy.position_size>0 ? long_takeprofit_price : na, color=color.new(#008000, 0), style=plot.style_linebr, linewidth=1, title='Long TP Level')

//plot(strategy.position_size > 0 ? long_stoploss_price : na, color=color.orange, style=plot.style_circles)
//plot(strategy.position_size > 0 ? long_takeprofit_price : na, color=color.blue, style=plot.style_circles)

plot(strategy.position_size<0 ? short_stoploss_price : na, color=color.new(#ff0000, 0), style=plot.style_linebr, linewidth=1, title='Short SL Level')
plot(strategy.position_size<0 ? short_takeprofit_price : na, color=color.new(#008000, 0), style=plot.style_linebr, linewidth=1, title='Short TP Level')

barcolor(close>=open? color.new(color.green,80):color.new(color.red,80))