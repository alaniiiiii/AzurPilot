import re

from module.base.filter import Filter

FILTER_REGEX = re.compile(
    '^(ship|equip|pt|gachaticket'
    '|meta|skinbox'
    '|array|chip|cat|pr|dr'
    '|augment'
    '|cube|medal|expbook'
    '|box|plate|coin|oil|food'
    ')'

    '(ur|ssr'
    '|core|change|enhance'
    '|general|gun|torpedo|antiair|plane)?'

    '(s[1-8]|t[1-6])?$'
)
FILTER_ATTR = ('group', 'sub_genre', 'tier')
FILTER = Filter(FILTER_REGEX, FILTER_ATTR)


def parse_filter_amount(filter_string):
    """
    Parse optional amount suffix from event shop filter.

    Examples:
        Cube:5 > Oil:2 -> {'cube': 5, 'oil': 2}
        EquipSSR > Cube -> {}
    """
    out = {}
    for part in str(filter_string).split('>'):
        part = part.strip()
        if ':' not in part:
            continue
        name, amount = part.rsplit(':', 1)
        name = name.strip()
        try:
            amount = int(amount.strip())
        except ValueError:
            continue
        if amount <= 0:
            continue
        result = FILTER_REGEX.search(name.replace(' ', '').lower())
        if result is None:
            continue
        normalized = ''.join(value or '' for value in result.groups())
        out[normalized] = amount
    return out


def strip_filter_amount(filter_string):
    """
    Remove optional amount suffix before passing filters to base Filter.
    """
    out = []
    for part in str(filter_string).split('>'):
        part = part.strip()
        if ':' in part:
            name, amount = part.rsplit(':', 1)
            try:
                int(amount.strip())
                part = name.strip()
            except ValueError:
                pass
        out.append(part)
    return ' > '.join(out)


EVENT_SHOP_PRESET_FILTER = {
    'all': """
        EquipUR > EquipSSR > Cube > GachaTicket
        > Array > Chip > CatT3 
        > Meta > SkinBox
        > Oil > Coin > Medal > ExpBookT1 > FoodT1
        > DR > PR
        > AugmentCore > AugmentEnhanceT2 > AugmentChangeT2 > AugmentChangeT1
        > CatT2 > CatT1 > PlateGeneralT3 > PlateT3 > BoxT4
        > ShipSSR
    """,
}
