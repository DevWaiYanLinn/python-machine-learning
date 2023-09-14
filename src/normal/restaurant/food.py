import csv
from prettytable import PrettyTable
import uuid
import os


def create_menu(ITEM):
    menu_table = PrettyTable()
    menu_table.field_names = ['Name', 'Price']
    for item in ITEM.values():
        menu_table.add_row([item['name'], item['price']])

    return menu_table


def create_bill(orders):
    bill_table = PrettyTable()
    bill_table.field_names = ['Name', 'Quantity', 'Price']
    sub_total = 0
    for item in orders.values():
        sub_total += item['price']
        bill_table.add_row([item['name'], item['quantity'], item['price']])

    bill_table.add_row(['Subtotal', ' ',  f'{sub_total}$'])
    return [sub_total, bill_table]


def save_bill(orders):
    output_directory = './bills/'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    unique_id = str(uuid.uuid4())
    csv_file_path = os.path.join(output_directory, f'{unique_id}.csv')
    with open(csv_file_path, mode='w') as csv_bill:
        write_bill = csv.DictWriter(
            csv_bill, fieldnames=['name', 'price', 'quantity'])
        write_bill.writeheader()
        for item in orders.values():
            write_bill.writerow(item)


def new_order():
    order_items = {}

    def create_order(name, quantity, price):
        order_items[name] = {
            "name": name,
            "quantity": quantity,
            "price": float(price) * int(quantity)
        }
        return order_items

    def get_order():
        return order_items
    return [create_order, get_order]


def main():
    ITEM = {}
    with open('menu.csv', mode='r') as csv_menu:
        read_menu = csv.DictReader(csv_menu)
        for item in read_menu:
            ITEM[item['name']] = item

    menu = create_menu(ITEM)

    print('Thank you for choosing SORA FOOD.')
    print('Here are the delicious dishes we offer:')
    print(menu)
    [create_order, get_order] = new_order()
    print('Is there something special you\'d like to try?.')
    while True:
        order = input()
        if order == 'finished':
            break
        else:
            name, quantity = order.split(' x ')
            if name not in ITEM:
                print(
                    "I apologize, but the item you've requested is not currently available on our menu.")
                print('Is there something special you\'d like to try?')
                continue
            create_order(name, quantity, ITEM[name]['price'])

    sub_total, bill_table = create_bill(get_order())
    save_bill(get_order())

    print('Total is ', f'{sub_total}$')
    need_bill = input('Do you need the bill now? : yes or no?. ')

    if need_bill == 'yes':
        print(bill_table)

    print('Thank for dinning with us.')


main()
