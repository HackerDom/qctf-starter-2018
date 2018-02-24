import multiprocessing
import pickle
import random
import sys
from collections import defaultdict
from math import ceil, sqrt

import numpy as np
from scipy.stats import norm, skewnorm
from tqdm import tqdm

sys.path.append('..')
import features


INCOME_SECURITY = {
    'employee_wage': 0.8,
    'state_wage': 0.9,
    'dividents': 0.5,
    'rent': 0.6,
    'other': 0.1,
}

EXPENSE_SECURITY = {
    'housing': 0.8,
    'car_service': 0.5,
    'taxes': 0.8,
    'alimony': 0.8,
    'credits': 0.5,
    'insurance': 0.8,
    'other': 0.5,
}

PROPERTY_SECURITY = {
    'apartment': 0.7,
    'house': 0.5,
    'car': 0.3,
}


def calc_responsibility(fdict):
    result = 0.6
    if fdict['education'] >= 3 or \
            fdict['purpose:education'] or fdict['purpose:real_estate']:
        result += 0.1

    dependents = fdict['dependents']
    if dependents >= 2:
        result += 0.3
    elif dependents == 1:
        result += 0.2
    elif fdict['married']:
        result += 0.1

    for feature in ['has_overdue_debts', 'missed_deadlines', 'was_bankrupt']:
        if fdict[feature]:
            result *= 0.5

    return result


SIGMA_COEFF = 0.05


def calc_balance_distr(fdict, resp):
    balance_mean = 0
    balance_var = 0

    for cat in features.CUM_FEATURES['income']:
        value = fdict['income:' + cat]
        if value > 0:
            distr = skewnorm(-4, value, value * SIGMA_COEFF / INCOME_SECURITY[cat] / resp)
            balance_mean += distr.mean()
            balance_var += distr.var()

    for cat in features.CUM_FEATURES['expense']:
        value = fdict['expense:' + cat]
        if value > 0:
            distr = skewnorm(4, value, value * SIGMA_COEFF / EXPENSE_SECURITY[cat] / resp)
            balance_mean -= distr.mean()
            balance_var += distr.var()

    duration_in_months = 12 * fdict['duration']
    balance_mean *= duration_in_months
    balance_var *= duration_in_months ** 2

    for cat in features.CUM_FEATURES['property']:
        price = fdict['property:' + cat]
        if price > 0:
            distr = skewnorm(4, price, price * SIGMA_COEFF / PROPERTY_SECURITY[cat] / resp)
            balance_mean += distr.mean()
            balance_var += distr.var()

    return norm(balance_mean, sqrt(balance_var))


def cond_expect(norm_distr, a):
    """
    Let X = norm_distr(). This function returns E(X | X < a) * P{X < a}.

    To proof use:
    https://en.wikipedia.org/wiki/List_of_integrals_of_Gaussian_functions
    """

    mu, sigma = norm_distr.args
    return mu * norm_distr.cdf(a) - sigma ** 2 * norm_distr.pdf(a)


TARGET_INTEREST = 1.10
MAX_INTEREST = 10.00


def calc_interest_rate(fdict):
    resp = calc_responsibility(fdict)
    balance_distr = calc_balance_distr(fdict, resp)

    credit_amount = fdict['credit_amount']
    duration = fdict['duration']
    bank_wants = credit_amount * TARGET_INTEREST ** duration

    lo = TARGET_INTEREST
    hi = MAX_INTEREST
    for _ in range(15):
        middle = (lo + hi) / 2
        bank_asks = credit_amount * middle ** duration
        default_proba = balance_distr.cdf(bank_asks)
        bank_takes = cond_expect(balance_distr, bank_asks) + \
                     (1 - default_proba) * bank_asks

        if bank_takes < bank_wants:
            lo = middle
        else:
            hi = middle

    return ceil(lo * 1e3) / 1e3


def test_calc_interest_rate():
    fdict = {
        'credit_amount': 3 * 10 ** 6,
        'duration': 2,
        'education': 3,
        'married': 1,
        'dependents': 2,

        'purpose:real_estate': 1,

        'income:state_wage': 200000,
        'expense:housing': 28000,
        'expense:other': 9000,
    }

    print(calc_interest_rate(defaultdict(int, fdict)))


MAX_CUM_VALUE = {
    'income': 200000,
    'expense': 50000,
    'property': 5 * 10 ** 6,
}


def generate_input():
    fdict = {}

    for feature, (min, max) in features.NUM_FEATURES.items():
        fdict[feature] = random.randint(min, max)

    for feature, cats in features.CAT_FEATURES.items():
        value = random.choice(cats)

        for cat in cats:
            fdict[feature + ':' + cat] = 0
        fdict[feature + ':' + value] = 1

    for feature, cats in features.CUM_FEATURES.items():
        for cat in cats:
            if random.random() < 0.5:
                value = random.randint(1, MAX_CUM_VALUE[feature])
            else:
                value = 0

            fdict[feature + ':' + cat] = value

    return fdict


def generate_pair(_):
    fdict = generate_input()
    X_i = features.feature_dict_to_array(fdict)
    y_i = calc_interest_rate(fdict)
    return X_i, y_i


def generate_data(size):
    pool = multiprocessing.Pool()
    X = []
    y = []
    for X_i, y_i in tqdm(pool.imap_unordered(generate_pair, range(size)), total=size):
        X.append(X_i)
        y.append(y_i)

    return np.array(X), np.array(y)


DATA_FILENAME = 'data.pickle'


def main():
    data = generate_data(10 ** 6)

    with open(DATA_FILENAME, 'wb') as f:
        pickle.dump(data, f)
    print('[+] Saved to {}'.format(DATA_FILENAME))


if __name__ == '__main__':
    main()
