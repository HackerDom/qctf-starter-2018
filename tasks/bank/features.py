NUM_FEATURES = {
    'credit_amount': (10 ** 5, 3 * 10 ** 6),
    'duration': (1, 5),
    'education': (1, 3),
    'married': (0, 1),
    'dependents': (0, 2),

    'has_overdue_debts': (0, 1),
    'missed_deadlines': (0, 1),
    'was_bankrupt': (0, 1),
}

CAT_FEATURES = {
    'purpose': ['real_estate', 'car', 'education', 'capital', 'other'],
}

CUM_FEATURES = {
    'income': ['employee_wage', 'state_wage', 'dividents', 'rent', 'other'],
    'expense': ['housing', 'car_service', 'taxes', 'alimony', 'credits', 'insurance', 'other'],
    'property': ['apartment', 'house', 'car'],
}


def form_to_feature_dict(form):
    fdict = {}

    for feature, (min, max) in NUM_FEATURES.items():
        value = int(form.get(feature, 0))
        if not (min <= value <= max):
            raise ValueError('`{}` is not in allowed range {}-{}'.format(feature, min, max))

        fdict[feature] = value

    for feature, cats in CAT_FEATURES.items():
        value = form[feature]
        if value not in cats:
            raise ValueError('`{}` is set to unknown category `{}`'.format(feature, value))

        for cat in cats:
            fdict[feature + ':' + cat] = int(cat == value)

    for feature, types in CUM_FEATURES.items():
        for type in types:
            fdict[feature + ':' + type] = 0

        for type, amount in zip(form.getlist(feature + '_type'),
                                form.getlist(feature + '_amount')):
            if type == 'unknown':
                continue
            if type not in types:
                raise ValueError('`{}_type` is set to unknown category `{}`'.format(feature, type))

            amount = int(amount)
            if amount < 0:
                raise ValueError('`{}_amount` may not be negative'.format(feature))

            fdict[feature + ':' + type] += amount

    return fdict


def feature_dict_to_array(fdict):
    return [x for _, x in sorted(fdict.items())]
