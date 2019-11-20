def cvv_mask(cvv):
    """
    Mask to cvv number.
    :param cvv: Cvv number
    :return: Cvv masked with '*'
    """
    cvv_masked = "".join(map(lambda x: "*", cvv))
    return cvv_masked

def ccard_mask(cc):
    """
    Mask to credit card number
    :param cc: Credit card number
    :return: Credit card masked  e.g: ************4242
    """
    credit_card_masked = cc[-4:].rjust(len(cc), "*")
    return credit_card_masked
