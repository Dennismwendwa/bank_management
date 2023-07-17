from django.db import models
import csv



def write_to_file(data):

    with open("admin_activity.txt", mode="a", encoding="utf-8") as file:
        file.write(data)

    print("data saved to file")

def write_to_bus_file(data):
    with open("business_file.txt", mode="a", encoding="utf-8") as file:
        file.write(data)

    print("saved to business file")

def write_to_csv(data):

    with open("admin_user_deposits.csv", mode="a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.write(data)

    print("saved to csv file")
