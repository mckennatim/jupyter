[<--energy](./energy.ipynb)
    
     scp -r root@apps.sitebuilt.net:/home/jupyter/public_html/ /home/jupyter/
     the one source of truth is on apps.sitebuilt


### alt calcs - annual fuel use, degree days and heating load
To check on the Manual J heatLoss calculations, below you will find links to equivalent calculations in which design load is calculated from 
from historic averages of gallons of oil burned, degree days for Boston and the BTU per fuel unit. 

##### refs
* [intel cloud jupyter](https://console.cloud.intel.com)

* Heat Loss Calculations and Principles - pdf in /onedrive/energy
* degree-days Boston [current](https://massenergymarketers.org/resources/degree-days/boston/) - [23yr table](https://www.weather.gov/wrh/Climate?wfo=box) -  [query and API](https://www.degreedays.net)
* [projecting heating costs from btu/hr and degree days](https://forum.heatinghelp.com/discussion/131998/calculating-heating-costs-math-problem)
* [calculating home energy tutorial](http://hyperphysics.phy-astr.gsu.edu/hbase/thermo/heatloss.html)

#### For 255 chestnut Ave apt3 1-4
##### verifying manual J heatLoss
In general

(1)$$\frac{units}{yr} = \frac{heatLoss \frac{Btu}{hr} * 24\frac{hr}{day} * Degree \frac{T-day}{yr}}{\frac{Btu}{unit} * \Delta T * eff. }$$

solving for heatLoss@5F 

(1a)$$heatLoss \frac{Btu}{hr} = \frac{ \frac{units}{yr} * \frac{Btu}{unit} * \Delta T * eff.  }{24 \frac{hr}{day} * degree \frac{T-day}{yr}}$$

The heatLoss @ 5F was derived from manual J calculations.

To establish the relationship between the `historic fuel use` and `heatLoss @ 5`&deg;F we tweaked boiler efficiency until we got gallons to agree to historic averages.

(2)$$onePipeSteamBoilerOil\frac{units}{yr} = \frac{HeatLoss \frac{Btu}{hr} * 24\frac{hr}{day} * Degree \frac{T-day}{yr}}{Design \Delta T * Efficiency * \frac{Btu}{unit}}$$


```python
costPerKwh =.27
BtuPerKw = 3412
ElKwhPerYr = 1433 # actual fuel use for apt 3 2022-2023
costPerGal = 4.50
heatLoss = 13000 # apt manual J
deltaT = 65
degreeDays =4883 # used in calcs below
dd2021 = 5071
dd2122 = 5004
dd2223 = 4883 # degree days 2022-23
dd1823 = 5263 # 5 yr avg. degree day 2018 - 2023
dd9212 = 5714 # 20 year average 
effOil = .80 #of onepipe steam oil burner
BtuPerGal = 139000
galPerYr =(heatLoss * 24 * degreeDays)/(deltaT * effOil *BtuPerGal)

print(f"{galPerYr =:.0f} gal/yr @ {effOil = :.0%}")
```

    galPerYr =211 gal/yr @ effOil = 80%
    

This seems to be an reasonable efficiency value for The 35 year old Burnham a one-pipe steam oil fired system . So the calculated manual J heatLoss appears to be accurate. 

##### Predicting heat pump efficiency given electrical use for apt given heatLoss and degreeDays
For Apt 3 winter 22-23...

(3)$$heatPump\frac{kwh}{yr} = \frac{HeatLoss \frac{Btu}{hr} * 24\frac{hr}{day} * Degree \frac{T-day}{yr}}{ \Delta T * eff. * \frac{Btu}{kw}}$$

Solving for efficiency

(3a)$$eff = \frac{HeatLoss \frac{Btu}{hr} * 24\frac{hr}{day} * Degree \frac{T-day}{yr}}{heatPump\frac{kwh}{yr} * \Delta T * \frac{Btu}{kw}}$$


```python
effHP = (heatLoss * 24 * degreeDays)/(ElKwhPerYr * deltaT * BtuPerKw)

print(f"Apt 3 HeatPump electricity use 22-23 = {ElKwhPerYr:,.0f} kw/yr \
  \nimplies a heat pump efficiiency of {effHP:.1f} using \
  heatLoss @ 5F of {heatLoss:,.0f} Btu/hr")
```

    Apt 3 HeatPump electricity use 22-23 = 1,433 kw/yr   
    implies a heat pump efficiiency of 4.8 using   heatLoss @ 5F of 13,000 Btu/hr
    

Knowing how many `kwh` apt3 used in a year, we can predict total `Btu/yr`. (Not sure what the efficiency number (effHP) represents relative to COP or HSPF)




#### Heat Pump Efficiency


[Heating seasonal performance factor HSPF](https://en.wikipedia.org/wiki/Heating_seasonal_performance_factor#:~:text=The%20higher%20the%20HSPF%20rating,a%20US%20Energy%20Tax%20Credit.)

(4)$$HSPF = \frac{Btu}{watt-hr} = \frac{Btu}{(1000*kwh)}$$

Solving fro kwh

(5)$$ kwh = \frac{Btu}{(1000*HSPF)}$$

Solving for Btu

(6) $$\frac{Btu}{yr} = 1000 * \frac{Kwh}{yr} * HSPF$$ 

Here we used HSP and fuel use to estimate total energy use in a year  Btu/yr. So for apt 3 in 22-23




```python
HSPF = 10.4 # for LV181HV4
HSPFresist =3.4 # for electric resistance heat (100% efficient)
EffComparedToResist = HSPF/HSPFresist
EffComparedToOil = HSPF/(effOil * HSPFresist)
apt3BtuPerYr = 1000 * ElKwhPerYr * HSPF
print(f"using {HSPF = }, apt3BtuPerYr = {apt3BtuPerYr:,.0f} Btu when ElKwhPerYr = {ElKwhPerYr:,.0f}kwh \
  \nEffComparedToResist:  is {EffComparedToResist:.1f}\
 times more efficient than elec.resistance \
  \nEffComparedToOil:  is {EffComparedToOil:.1f}\
 times more efficient than oil")
```

    using HSPF = 10.4, apt3BtuPerYr = 14,903,200 Btu when ElKwhPerYr = 1,433kwh   
    EffComparedToResist:  is 3.1 times more efficient than elec.resistance   
    EffComparedToOil:  is 3.8 times more efficient than oil
    

Another way to get Btu/yr is to estimate it from heatLoss @5F and degree days.

(7)$$\frac{Btu}{yr} = heatLoss \frac{Btu}{hr}*24 \frac{hr}{day} * \frac{1}{ \Delta T}*Degree \frac{T-days}{yr}$$



```python
#heatLoss = 10000 //try a different heatLoss @5F

apt3BtuYr =heatLoss * 24 / deltaT * degreeDays
ratio = apt3BtuYr/apt3BtuPerYr 
print(f"By (7) using heatLoss@5F={heatLoss:,.0f} and {degreeDays=}: apt3BtuYr = {apt3BtuYr:,.0f} btu/yr \
  \nBy (6) using {ElKwhPerYr = :,.0f} and { HSPF=} {apt3BtuPerYr = :,.0f} Btu/yr\
  \nSo the apt3BtuYr(7)/apt3BtuPerYr(6) {ratio = :.2f}")

```

    By (7) using heatLoss@5F=13,000 and degreeDays=4883: apt3BtuYr = 23,438,400 btu/yr   
    By (6) using ElKwhPerYr = 1,433 and  HSPF=10.4 apt3BtuPerYr = 14,903,200 Btu/yr  
    So the apt3BtuYr(7)/apt3BtuPerYr(6) ratio = 1.57
    

Coefficient of performance

(8)$$COP = \frac{Btu}{kw*3412\frac{Btu}{kw}}$$ 


```python
COPa = apt3BtuYr / (ElKwhPerYr * 3412)
COPb = apt3BtuPerYr / (ElKwhPerYr * 3412)

print(f"With {heatLoss = :,.0f} Btu/hr & {ElKwhPerYr = :,.0f} kwh \
  \n{COPa =  :.1f} with {apt3BtuYr = :,.0f} \
  \n{COPb =  :.1f} with {apt3BtuPerYr = :,.0f} ")
```

    With heatLoss = 13,000 Btu/hr & ElKwhPerYr = 1,433 kwh   
    COPa =  4.8 with apt3BtuYr = 23,438,400   
    COPb =  3.0 with apt3BtuPerYr = 14,903,200 
    

##### apt3 predicted costs comapared to actual costs for 2023

(5)$$ kwh = \frac{Btu}{(1000*HSPF)}$$


```python
apt3predKwh = apt3BtuYr/ (1000 * HSPF)
apt3predCost = apt3predKwh * costPerKwh
apt3actualCost = ElKwhPerYr * costPerKwh

print(f"Uing {HSPF =} \nPREDICTED: {apt3BtuYr = :,.0f} Btu/yr\n\
  {apt3predKwh =:,.0f} kwh and apt3predCost = ${apt3predCost:,.2f} \
    \nACTUAL {apt3BtuPerYr = :,.0f} Btu/yr \
    \n  {ElKwhPerYr = :,.0f} kwh  and apt3actualCost = ${apt3actualCost:,.2f}")
```

    Uing HSPF =10.4 
    PREDICTED: apt3BtuYr = 23,438,400 Btu/yr
      apt3predKwh =2,254 kwh and apt3predCost = $608.50     
    ACTUAL apt3BtuPerYr = 14,903,200 Btu/yr     
      ElKwhPerYr = 1,433 kwh  and apt3actualCost = $386.91
    

The PREDICTED energy used in a year (Btu/yr) used manual J heatLoss@5F, degree days. The manual J calcs were verified by heatLoss@5F calculated from fuel use

There is an inconsistency between PREDICTED annual energy use and cost compared to ACTUAL energy use and cost. This is not resolved. It is a good thing that the predictions were higher than actual, and it was also a good thing that the predicted energy use and cost was lower than the energy use and cost using oil. So the moral is using the prediction model is OK and you can maybe beat the predictions with good design and equipment selection.

#### 12 parley vale

1. Predict building heatLoss @5F from historic natural gas prices and degree days
2. Estimate building total Btu/yr from HeatLoss @ 5F and degree days
3. Estimate how many kwh a new heat pump system will need to provide total Btu/hr using HSPF
4. Compare new system \$/yr to old system \$/yr

#####  heat loss in stairways

[Understanding Thermal Comfort Impact and Air Movement
Around Open Stairs Through the Use of CFD Modeling](https://scholarworks.uark.edu/cgi/viewcontent.cgi?article=6015&context=etd)

##### 1. Predicting heatLoss @ 5F from hhistoric gas use
from
(1)$$\frac{units}{yr} = \frac{HeatLoss \frac{Btu}{hr} * 24\frac{hr}{day} * Degree \frac{T-day}{yr}}{Design \Delta T * Efficiency * \frac{Btu}{unit}}$$

we get

(9)$$heatLoss \frac{Btu}{hr} = \frac{ \frac{units}{yr} * \frac{Btu}{unit} * \Delta T * eff.  }{24 \frac{hr}{day} * degree \frac{T-day}{yr}}$$

So for 2023, 2022 and 2021 we can get a reasonable guess at heatLoss @5F for 12 Parley Vale.


```python
BtuPerTherm = 100000
gasEff =.9
costPerTherm = 2.33
th12p23 = 595
th12p22 = 680
th12p21 = 608
heatLoss12p23 =  (th12p23 * BtuPerTherm * deltaT * gasEff)/(24 * dd2223)
heatLoss12p22 =  (th12p22 * BtuPerTherm * deltaT * gasEff)/(24 * dd2122)
heatLoss12p21 =  (th12p21 * BtuPerTherm * deltaT * gasEff)/(24 * dd2021)

print(f"{heatLoss12p23 =:,.0f} Btu/hr \
  \n{heatLoss12p22 =:,.0f} btu/hr \
  \n{heatLoss12p21 =:,.0f} btu/hr")
```

    heatLoss12p23 =29,701 Btu/hr   
    heatLoss12p22 =33,124 btu/hr   
    heatLoss12p21 =29,225 btu/hr
    


##### 2. Predicting Btu/yr from heatLoss Btu/hr @5F and degreeDays
 
(7)$$\frac{Btu}{yr} = heatLoss \frac{Btu}{hr}*24 \frac{hr}{day} * \frac{1}{ \Delta T}*Degree \frac{T-days}{yr}$$


```python
Btuyr23dd = heatLoss12p23 * 24 / deltaT * dd2223 # 2023
Btuyr22dd = heatLoss12p22 * 24 / deltaT * dd2122 # 2022
Btuyr21dd = heatLoss12p21 * 24 / deltaT * dd2021 # 2021
print(f"2023 {Btuyr23dd = :,.0f} Btu/yr \
      \n2024 {Btuyr22dd = :,.0f} Btu/yr \
      \n2021 {Btuyr21dd = :,.0f} Btu/yr \n")
```

    2023 Btuyr23dd = 53,550,000 Btu/yr       
    2024 Btuyr22dd = 61,200,000 Btu/yr       
    2021 Btuyr21dd = 54,720,000 Btu/yr 
    
    

##### 3. predicted heat pump kwh from HSPF
(5)$$ kwh = \frac{Btu}{(1000*HSPF)}$$


```python

kwh23=Btuyr23dd/(1000 * HSPF)
kwh22=Btuyr22dd/(1000 * HSPF)
kwh21=Btuyr21dd/(1000 * HSPF)
elCost23 =kwh23*costPerKwh
elCost22 =kwh22*costPerKwh
elCost21 =kwh21*costPerKwh
gasCost23 =th12p23 * costPerTherm
gasCost22 =th12p22 * costPerTherm
gasCost21 =th12p21 * costPerTherm

print(f"Assuming {HSPF=} and {costPerKwh = } and {costPerTherm = } \
  \n 2023  {kwh23 = :,.0f} kwh and elCost23 = ${elCost23:,.2f} gasCost23 = ${gasCost23:,.2f}\
  \n 2022  {kwh22 = :,.0f} kwh and elCost22 = ${elCost22:,.2f} gasCost22 = ${gasCost22:,.2f}\
  \n 2021  {kwh21 = :,.0f} kwh and elCost21 = ${elCost21:,.2f} gasCost21 = ${gasCost21:,.2f}")
```

    Assuming HSPF=10.4 and costPerKwh = 0.27 and costPerTherm = 2.33   
     2023  kwh23 = 5,149 kwh and elCost23 = $1,390.24 gasCost23 = $1,386.35  
     2022  kwh22 = 5,885 kwh and elCost22 = $1,588.85 gasCost22 = $1,584.40  
     2021  kwh21 = 5,262 kwh and elCost21 = $1,420.62 gasCost21 = $1,416.64
    

The PREDICTED energy use using an HSPF 10.4 heat pump system at current energy prices is pretty much a wash; almost exactly the same cost as gas. Hopefully the new system will beat the predictions like apt3 did. Or Maybe the manual J calculations will be lower than the heatLoss@5F derived from historic fuel use. Either way it is a go for new system redesign. 


```python
print(f"Design a system for 12 Parley Vale sized to supply 70F inside temp \
  \nwhen heatLoss@5F ={heatLoss12p22:,.0f} Btu/hr")
```

    Design a system for 12 Parley Vale sized to supply 70F inside temp   
    when heatLoss@5F =33,124 Btu/hr
    

OMG, something is wrong, I currently have a 120,000 Btu boiler! Get over it. think about the boilers at Chestnut Ave. Those old oilfired boilers wer pumpin out...


```python
nozzleSize = .75 # gph
BtuOilBoiler = nozzleSize * BtuPerGal

print(f"Apt 1-4 boilers had {nozzleSize =} gph. @ {BtuPerGal =}. \
It was a {BtuOilBoiler:,.0f}Btu boiler \
    \nfor an apartment that needed {heatLoss:,} Btu on a 5F day")
```

    Apt 1-4 boilers had nozzleSize =0.75 gph. @ BtuPerGal =139000. It was a 104,250Btu boiler     
    for an apartment that needed 13,000 Btu on a 5F day
    

That old boiler was replaced with a 1.5 ton 18,000 Btu Heat Pump

Coefficient of performance

(8)$$COP = \frac{Btu}{kw*3412\frac{Btu}{kw}}$$ 

solve for kwh:



While COP is `power_out/power_in` at an instant in time only at a particular outdoor temperatures , we can use to as a rough measure of the relationship of enery_out/ energy_in over a heating season and compare btu_out/kw_in. Given a COP value and knowing the Btu/yr required, we can guess the electrical use for the year(`kw/yr`) and then the `cost/yr`

(9)$$kwh/yr = \frac{Btu/yr}{COP*3412Btu/kw}$$ 


```python
COP = 2
kwhyr = Btuyr22dd/(COP*3412)
costByCOP = kwhyr*costPerKwh
percOfCur = costByCOP/gasCost22
print(f"To create {Btuyr22dd :,.0f} Btu/yr at a COP of {COP:.1f} will require \
    \n   {kwhyr:,.0f} kw/yr at ${costPerKwh:1.2f}/kwh = ${costByCOP:,.2f}/yr \
    \n   which is {percOfCur-1:.0%} more than historic gas costs of ${gasCost22:,.2f}")
```

    To create 61,200,000 Btu/yr at a COP of 2.0 will require     
       8,968 kw/yr at $0.27/kwh = $2,421.45/yr     
       which is 53% more than historic gas costs of $1,584.40
    

## products



### Artic

### Artic 030ZA(BEH2)
    <timwallace@arcticheatpumps.com>
    Tim Wallace
    614.657.8284
    Arctic Heat Pumps
    Michigan and Massachusetts Sales Representative

I was just told the only time a heat exchanger would be necessary is turn of century 1900 registers or water based only registers.
![](./Artic%20030ZA(BEH2).png)

Hi Tim,

Thanks for the info on the Artic 030ZA(BEH2).

In looking at the house presently heated with 7 zones of hydronic, I have done a bit of analysis. I have been predicting {{Btuyr22dd}}

While COP is `power_out/power_in` at an instant in time only at a particular outdoor temperatures , we can use to as a rough measure of the relationship of enery_out/ energy_in over a heating season and compare btu_out/kw_in. Given a COP value and knowing the Btu/yr required, we can guess the electrical use for the year(`kw/yr`) and then the `cost/yr`

(9)$$kwh/yr = \frac{Btu/yr}{COP*3412Btu/kw}$$ 


```python
COP = 2
kwhyr = Btuyr22dd/(COP*3412)
costByCOP = kwhyr*costPerKwh
percOfCur = costByCOP/gasCost22
print(f"To create {Btuyr22dd :,.0f} Btu/yr at a COP of {COP:.1f} will require \
    \n   {kwhyr:,.0f} kw/yr at ${costPerKwh:1.2f}/kwh = ${costByCOP:,.2f}/yr \
    \n   which is {percOfCur-1:.0%} more than historic gas costs of ${gasCost22:,.2f}")

```

    To create 61,200,000 Btu/yr at a COP of 2.0 will require     
       8,968 kw/yr at $0.27/kwh = $2,421.45/yr     
       which is 53% more than historic gas costs of $1,584.40
    
