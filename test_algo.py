def MOON():
    card_number = "5551565655515623"
    # удаляем пробелы из номера карты
    card_number = card_number.replace(' ', '')

    if not card_number.isdigit() or len(card_number) != 16:
        return False

    sum = 0
    oddeven = 0

    for count in range(15, -1, -1):
        digit = int(card_number[count])

        if oddeven % 2 == 0:
            digit *= 2

        if digit > 9:
            digit -= 9

        sum += digit
        oddeven += 1

    return (sum % 10) == 0


print(MOON())
