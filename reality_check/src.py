


# Fee  | Charged by | Paid to
# Stamp Duty | Revenue | Revenue
# Survey | Surveyor | Surveyor
# Solicitor Fee | Solicitor | Solicitor
# Land Registry Fee | Land Registry | Solicitor?
# Land Registry Fee for certified copy Folio | Land Registry | Solicitor?
# Land Registry Fee on Mortgage | Land Registry | Solicitor?
# Search Fee | ? | Solicitor
# Commissioner for Oaths | ? | ?
# Estate Agent Fee | Estate Agent | Estate Agent
# Valuation Fee | Valuer | Lender
# Local Property Tax | Revenue | Revenue
# Mortgage Protection Insurance | Insurer | Insurer
# Home Insurance | Insurer | Insurer

from collections import namedtuple
import pandas as pd


VAT = 0.23

FeeValue = namedtuple('FeeValue', ['name', 'value'])
FeeEstimate = namedtuple('FeeEstimate', ['name', 'min', 'mean', 'max'])


def get_property_tax(price):
    if price > 1000000:
        return FeeValue("Property Tax", 1800 + (price - 1000000) * 0.0025)
    else:
        valuation_midpoints = [50000] + list(range(125000, 975000, 50000))
        distances = [abs(e - price) for e in valuation_midpoints]
        closest_midpoint = distances.index(min(distances))
        return FeeValue("Property Tax", valuation_midpoints[closest_midpoint] * 0.0018)


def get_stamp_duty(price, isNewBuild):
    base_price = price * 0.865 if isNewBuild else price
    stamp_duty = base_price * 0.01 if base_price < 1000000 else base_price * 0.02  # Unsure if €1M threshold applies to price with or without VAT
    return FeeValue('Stamp Duty', stamp_duty)


def get_surveyor_fee():
    base_estimates = [250, 300, 1000]
    d = ["Survey Fee"] + list(map(lambda e: e + e * VAT, base_estimates))
    return FeeEstimate(*d)


def get_legal_fees(price):
    base_estimates = [900, price * 0.01, price * 0.02]
    vat_estimates = ['Solicitor Fee'] + list(map(lambda e: e + e * VAT, base_estimates))
    return FeeEstimate(*vat_estimates)


def get_land_registry_fee(price):
    fee = 0
    if price <= 50000:
        fee = 400
    elif price <= 200000:
        fee = 600
    elif price <= 400000:
        fee = 700
    else:
        fee = 800

    return FeeValue("Land Registry Fee", fee)


def get_agency_fees(price):
    base_estimates = [price * 0.01, price * 0.015, price * 0.02]
    vat_estimates = ["Estate Agency Fee"] + list(map(lambda e: e + e * VAT, base_estimates))
    return FeeEstimate(*vat_estimates)


def get_valuation_fee():
    base_estimates = [150, 200, 250]
    vat_estimates = ["Valuation Fee"] + list(map(lambda e: e + e * VAT, base_estimates))
    return FeeEstimate(*vat_estimates)


def estimate_transaction_fees(price, isNewBuild):
    transaction_fees = [get_stamp_duty(price, isNewBuild),
                        get_surveyor_fee(),
                        get_valuation_fee(),
                        get_legal_fees(price),
                        get_land_registry_fee(price),
                        FeeValue("Land Registry Fee for Certified Copy", 40),
                        FeeValue("Land Registry Fee on Mortgage", 175),
                        FeeEstimate("Search Fees", 100, 250, 500),
                        FeeValue("Commissioner For Oaths", 44)]
    data = []
    for fee in transaction_fees:
        if isinstance(fee, FeeValue):
            data.append({"name": fee.name, "min": fee.value, "mean": fee.value, "max": fee.value})
        else:
            data.append(fee._asdict())
    d = pd.DataFrame.from_dict(data)
    d.loc["Total"] = d.sum(numeric_only=True)

    return d