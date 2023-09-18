import csv
from prettytable import PrettyTable
import uuid
import os
import sys
from matplotlib import pyplot as plt


def visualize_sales(items):
    item_names = list(items.keys())
    item_prices = [float(item['price']) for item in items.values()]
    plt.figure(figsize=(10, 6))
    plt.bar(item_names, item_prices, color='skyblue')
    plt.xlabel('Menu Item')
    plt.ylabel('Sales Price ($)')

    # Format y-axis tick labels as floats with two decimal places
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))

    plt.title('Menu Item Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the chart
    plt.show()



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
        bill_table.add_row([item['name'], item['quantity'],
                           "{:.2f}".format(item['price'])])

    bill_table.add_row(['Subtotal', ' ', f'{"{:.2f}".format(sub_total)}$'])
    bill_table.add_row(['Total', ' ', f'{"{:.2f}".format(sub_total)}$'])
    return ["{:.2f}".format(sub_total), bill_table]


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

    def remove_items(names):
        for name in names:
            if name in order_items:
                del order_items[name]

    def get_order():
        return order_items

    return [create_order, get_order, remove_items]


def main():
    items = {}
    with open('menu.csv', mode='r') as csv_menu:
        read_menu = csv.DictReader(csv_menu)
        for item in read_menu:
            items[item['name']] = item

    menu = create_menu(items)

    CYAN = "\033[96m"
    RESET = "\033[0m"

    print(CYAN + 'Thank you for choosing MAGIC FOOD.' + RESET)
    print(CYAN + 'Here are the delicious dishes we offer:' + RESET)
    print(menu)  # Assuming "menu" contains your menu items
    print(CYAN + 'Is there something special you\'d like to try?' + RESET)
    visualize_sales(items)
    create_order, get_order, remove_items = new_order()
    while True:
        order = input()
        if order == 'finished':
            break
        elif order == 'check order':
            order_table = check_order(get_order())
            print(order_table)
            continue
        elif order == 'remove items':
            print(
                'Please type a list of items separated by commas. For example: Pizza, Taco')
            names = [name for name in input().split(',')]
            remove_items(names)
            print(order_table)
            continue
        else:
            name, quantity = order.split(' x ')
            if name not in items:
                print(
                    f"{CYAN}I apologize, but the item({name}) you've requested is not currently available on our menu.{RESET}")
                print(CYAN + 'Is there something special you\'d like to try?' + RESET)
                continue
            create_order(name, int(quantity), float(items[name]['price']))

    sub_total, bill_table = create_bill(get_order())
    save_bill(get_order())

    print('Total is ', f'{sub_total}$')
    need_bill = input(
        CYAN + 'Do you need the bill now? : yes or no?. ' + RESET)

    if need_bill == 'yes':
        print(CYAN + '\nYour bill is ready.' + RESET)
        print(bill_table)

    print(CYAN + 'Thank for dinning with us.' + RESET)


def documentation():
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    print(RED + 'Welcome to our ordering system!' + RESET)
    print(RED + 'Before you start, please take a moment to read the instructions:' + RESET)
    print(GREEN + '- To place an order, type the items and quantities like this:' + RESET)
    print('  Example:')
    print('  Pizza x 1')
    print('  Taco x 2')
    print(GREEN + '- To remove items from your order, type: "remove items"' + RESET)
    print(GREEN + '- To check your current order, simply type: "check order"' + RESET)
    print(GREEN + '- Once you\'ve finished ordering, type: "finished"' + RESET)
    agree = input('Do you agree to these terms? Type "yes" or "no": ')
    if agree == 'yes':
        main()
    else:
        sys.exit(0)


documentation()
