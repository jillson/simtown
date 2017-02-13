
# Stable point = where supply = demand

# This is a non-linear (but hopefully continous) demand curve
#
#   if price <= 1:
#      demand = population + rich + food reserve $/price
#   if price == 1, we have a very big jump in demand... should there be some smoothing?
#   if 1 < price <= 2:
#      demand = min(population*2, population + rich (rich want twice as much)
#   if price > 2
#      demand = 2 * (population - rich)/price  + (10 * rich / price =  2 * (population + 9 * rich) / price
# Oops, but the ruler wants a reasonable chance to keep his people fed:
#if price > 2:
     supply = min(reserve, amount to get price back down to 2)

Examples:
Assume population = 100, food_reserve_$ = 100 (at start), and 90 have 2 gp / person (and will buy up to 2 units of food) and 10 have 10 gp / person (and will also buy up to 2 units of food).

For price < 1, the demand is min(90 * 2, 90 * 2 / P) + min(10 * 2, 10 * 10 / P) +  100 / P
For 5 > price >= 1, the demand is 90 * 2 / P + 20
For price >= 5, the demand is 90 * 2 / P + 100 / P

Supply = 1000:
Price < 1, demand would be 200 + 100/p
p = 1/8 (.125) (poor and rich get 2 units, remaining 800 bought and stored for future)

Supply = 110
If price were < 1, demand would be 180 + 20 + 100/P --> too big
If price were 1, the demand would be 200 --> still too big
If price were >= 5, the demand would be 20 + 36 --> too small, ergo
demand must be between 1 and 5:
(180/P) + 20 = 110
180/P = 90
P = 2 --> poor get 1 unit each, rich get 2 units

Supply = 50
price = 5 --> demand is 180 / 5 + 100 / 5 = 56
280 / P = 50
price = 5.6 (poor get 2/5.6 each, rich get 10/5.6 each)
However, assuming there is stuff in storage, supply would be artificially increased to 110 (60) to get the price back to 2

Supply = 100
180/P + 20 = 100
180/P = 80
p = 18/8 = 9/4 = 2.25
Again, supply would be bumped up to 110

Supply = 200
180/P + 20 = 200
P = 1 --> need a way to make this be "stable" (or just have someone only buy to get the price up to 1
