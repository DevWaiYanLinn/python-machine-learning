import csv
from prettytable import PrettyTable
import uuid
import os
import sys


def check_order(items):
    order_table = PrettyTable()
    order_table.field_names = ['Name', 'Quantity']
    for item in items.values():
        order_table.add_row([item['name'], item['quantity']])

    return order_table


def create_menu(items):
    menu_table = PrettyTable()
    menu_table.field_names = ['Name', 'Price']
    for item in items.values():
        menu_table.add_row([item['name'], item['price']])

    return menu_table


def create_bill(orders):
    bill_table = PrettyTable()
    bill_table.field_names = ['Name', 'Quantity', 'Price']
    sub_total = 0
    for item in orders.values():
        sub_total += item['price']
        bill_table.add_row([item['name'], item['quantity'], item['price']])

    bill_table.add_row(['Subtotal', ' ', f'{sub_total}$'])
    bill_table.add_row(['Total', ' ', f'{sub_total}$'])
    return [sub_total, bill_table]


def save_bill(orders):
    output_directory = './bills/'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    unique_id = str(uuid.uuid4())
    csv_file_path = os.path.join(output_directory, f'{unique_id}.csv')
    with open(csv_file_path, mode='w', newline='') as csv_bill:
        write_bill = csv.DictWriter(
            csv_bill, fieldnames=['name', 'price', 'quantity'])
        write_bill.writeheader()
        for item in orders.values():
            write_bill.writerow(item)


def new_order():
    order_items = {}

    def create_order(name, quantity, price):
        if name in order_items:
            order_items[name]['quantity'] = order_items[name]['quantity'] + quantity
            order_items[name]['price'] = price * order_items[name]['quantity']
        else:
            order_items[name] = {
                "name": name,
                "quantity": quantity,
                "price": price * quantity
            }
        return order_items

    def get_order():
        return order_items

    return [create_order, get_order]


def main():
    items = {}
    with open('menu.csv', mode='r') as csv_menu:
        read_menu = csv.DictReader(csv_menu)
        for item in read_menu:
            items[item['name']] = item

    menu = create_menu(items)

    print('Thank you for choosing MAGIC FOOD.')
    print('Here are the delicious dishes we offer:')
    print(menu)
    print('Is there something special you\'d like to try?.')
    create_order, get_order = new_order()
    while True:
        order = input()
        if order == 'finished':
            break
        elif order == 'check order':
            order_table = check_order(get_order())
            print(order_table)
            continue
        else:
            name, quantity = order.split(' x ')
            if name not in items:
                print(
                    f"I apologize, but the item({name}) you've requested is not currently available on our menu.")
                print('Is there something special you\'d like to try?')
                continue
            create_order(name, int(quantity), float(items[name]['price']))

    sub_total, bill_table = create_bill(get_order())
    save_bill(get_order())

    print('Total is ', f'{sub_total}$')
    need_bill = input('Do you need the bill now? : yes or no?. ')

    if need_bill == 'yes':
        print('\nYour bill is ready.')
        print(bill_table)

    print('Thank for dinning with us.')


def documentation():
    print('I would like you to read the documentation before the program is started.')
    print('If you want to order,', 'type:\nPizza x 1\nTaco x 2 ')
    print('If you check the order', 'type:\ncheck order')
    print('After finished the order', 'type:\nfinished')
    agree = input('Do you agree? yes or no. ')
    if agree:
        main()
    else:
        sys.exit(0)


documentation()
