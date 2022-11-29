import requests, json, colorama, time, ctypes, os, sys, re, threading, datetime, discord_webhook
from discord_webhook import DiscordWebhook, DiscordEmbed
from colorama import Fore, Back, Style
colorama.init()
ctypes.windll.kernel32.SetConsoleTitleW("Sellpass API | By Zqzai (xi#0011)")
os.system('cls')

loopNum = 0
threadLock = threading.Lock()
ordersSent = []

if os.path.exists("config.json") == False:
    with open("config.json", "w") as f:
        json.dump({"apikey": "", "shopid": "", "webhook": ""}, f, indent=4)
        f.close()

with open("config.json", "r") as f:
    config = json.load(f)
    f.close()

try:
    api = config["apikey"]
    if api == "":
        api = input(f"{Fore.GREEN}Please enter your API key, this will automatically be saved in the config.json file for you: ")
        config["apikey"] = api
        with open("config.json", "w") as f:
            json.dump(config, f)
            f.close()

    webhook = config["webhook"]
    if webhook == "":
        webhook = input(f"{Fore.GREEN}Please enter your webhook, this will automatically be saved in the config.json file for you: ")
        config["webhook"] = webhook
        with open("config.json", "w") as f:
            json.dump(config, f)
            f.close()

    shopid = config["shopid"]
    if shopid == "":
        shopid = input(f"{Fore.GREEN}Please enter your shopid, this will automatically be saved in the config.json file for you: ")
        config["shopid"] = shopid
        with open("config.json", "w") as f:
            json.dump(config, f)
            f.close()
except:
    print("Error loading config.json, please delete it and try again.")
    time.sleep(5)
    sys.exit()

if os.path.exists("oldCache.json") == False:
    with open("oldCache.json", "w") as f:
        f.write("{}")
        f.close()

if os.path.exists("newCache.json") == False:
    with open("newCache.json", "w") as f:
        f.write("{}")
        f.close()

headers = {
    "authorization": "Bearer " + api,
}

while True:
    startime = datetime.datetime.now()
    req = requests.get(f"https://dev.sellpass.io/self/{shopid}/invoices", headers=headers)

    orders = req.json()['data']

    with open("oldCache.json", "r") as f:
        oldCache = json.load(f)
        f.close()
        
    with open("newCache.json", "r") as f:
        newCache = json.load(f)
        f.close()

    with open("oldCache.json", "w") as f:
        json.dump(newCache, f, indent=4)
        f.close()

    with open("newCache.json", "w") as f:
        json.dump(orders, f, indent=4)
        f.close()

    for order in orders:
        def check():
            global loopNum
            if re.search(order["id"], str(oldCache)) == None:
                orderId = order["id"]
                orderEmail = order["customerInfo"]["customerForShop"]["customer"]["email"]
                customerId = order["customerInfo"]["customerForShop"]["customerId"]
                orderStatus = order["status"]
                # If ur editing this, and wanna use functions depending on whether the user has paid or not. Here you go :) (Thank me later)
                # THESE ARE THE STATUSES OF ORDERS AND THEIR MEANINGS:
                # New = 0,
                # Pending = 1,
                # PaymentReceived = 2,
                # Completed = 3,


                # Cancelled = 10,
                # Expired = 11,


                # PartiallyDelivered = 40,
                # NotDelivered = 41,


                # ActionFromSellerNeeded = 50,
                # Failed = 51
                # If you want to use the orderStatus variable, you can use it like this:
                # if orderStatus == 2:
                #     print("Order has been paid for!")
                # else:
                #     print("Order has not been paid for!")
                embed = DiscordEmbed(title="New Order Created", description=f"**❯** Order ID: {orderId}\n**❯** Customer ID: {customerId}\n**❯** Customer Email: {orderEmail}\n**❯** Order Status: {orderStatus}", color=0x2F3136)
                webhook = DiscordWebhook(url=webhook)
                webhook.add_embed(embed)
                if re.search(orderId, str(ordersSent)) == None:
                    webhook.execute()
                    ordersSent.append(orderId)
                    print(f"{Fore.GREEN}Sent new order {orderId} to discord!")
                else:
                    pass

        threading.Thread(target=check).start()

    endtime = datetime.datetime.now()
    totaltime = (endtime - startime).total_seconds().__round__(2)
    loopNum += 1
    print(f"{Fore.GREEN}Cycle {loopNum} completed in {totaltime}s, if no other messages are shown, no new orders were found.")
    time.sleep(1)