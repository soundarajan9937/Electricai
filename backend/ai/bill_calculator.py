def calculate_bill(reading):

    try:
        reading = int(reading)
    except:
        return 0

    # Temporary demo calculation
    units = reading % 500

    if units <= 100:
        amount = units * 2

    elif units <= 300:
        amount = (100 * 2) + ((units - 100) * 4)

    else:
        amount = (100 * 2) + (200 * 4) + ((units - 300) * 6)

    return amount